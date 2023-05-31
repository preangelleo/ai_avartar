from langchain.chains import RetrievalQA
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

import requests

from src.bot.telegram.utils.utils import tg_get_file_path
from src.bot.bot_branch.document_branch.document_branch import DocumentBranch
from src.utils.logging_util import logging
from src.utils.param_singleton import Params
from src.utils.utils import (
    insert_dialogue_tone_from_file,
    insert_system_prompt_from_file,
)


class TelegramDocumentBranch(DocumentBranch):
    def __init__(self, *args, **kwargs):
        super(TelegramDocumentBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        tg_msg = msg.raw_msg

        try:
            file_name = tg_msg['message']['document'].get('file_name', '')
            if not file_name:
                return
            if file_name in ['dialogue_tone.xls', 'system_prompt.txt'] and msg.chat_id not in bot.bot_admin_id_list:
                return

            file_id = tg_msg['message']['document']['file_id']

            file_path = tg_get_file_path(file_id)
            file_path = file_path.get('file_path', '')
            if not file_path:
                return

            logging.debug(f"document file_path: {file_path}")
            SAVE_FOLDER = 'files/'

            save_file_path = f'{SAVE_FOLDER}{file_name}'
            file_url = f'https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_TOKEN}/{file_path}'
            with open(save_file_path, 'wb') as f:
                f.write(requests.get(file_url).content)

            caption = tg_msg['message'].get('caption', '')
            if caption and caption.split()[0].lower() in [
                'group_send_file',
                'gsf',
                'group send file',
            ]:
                bot.send_msg(
                    f'{msg.user_nick_name}我收到了你发来的文件, 请稍等 1 分钟, 我马上把这个文件发给所有人 😁...',
                    msg.chat_id,
                )
                bot.send_file_to_all(msg, save_file_path)
                return

            loader = ''
            if file_name.endswith('.pdf'):
                loader = PyPDFLoader(save_file_path)
            if file_name.endswith('.txt') and file_name != 'system_prompt.txt':
                loader = TextLoader(save_file_path, encoding='utf8')
            if file_name.endswith('.docx') or file_name.endswith('.doc'):
                loader = UnstructuredWordDocumentLoader(save_file_path)
            if file_name.endswith('.pptx') or file_name.endswith('.ppt'):
                loader = UnstructuredPowerPointLoader(save_file_path)

            if loader:
                documents = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents(documents)

                db = Chroma.from_documents(texts, Params().embeddings)
                retriever = db.as_retriever()

                qa = RetrievalQA.from_chain_type(llm=Params().llm, chain_type="stuff", retriever=retriever)

                bot.send_msg(
                    f"{msg.user_nick_name}, 我收到你发来的 {file_name[-4:].upper()} 文档了, 如果想要了解本文档的相关内容, 可以使用 doc 命令前缀加上你的问题, 我会帮你通过矢量数据进行语义搜索, 找到答案。注意, doc 命令后面需要有空格哦 🙂. 现在我先帮你简单看一下这个文档是说什么的. 请稍等 1 分钟哈。🤩",
                    msg.chat_id,
                )

                query = "请简单介绍一下这个文档讲了什么。"
                r = qa.run(query)
                if r:
                    bot.send_msg(r, msg.chat_id)
                # translate_if_is_english(r, tg_msg['message']['chat']['id'])
            elif file_name == 'dialogue_tone.xls':
                r = insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')
                if r:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 我收到你发来的 dialogue_tone.xls 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新文件的指示来应对聊天风格哈, 放心, 我很聪明的 🙂!",
                        msg.chat_id,
                    )
                else:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 我收到你发来的 dialogue_tone.xls 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨",
                        msg.chat_id,
                    )
            elif file_name == 'system_prompt.txt':
                r = insert_system_prompt_from_file(file_path='files/system_prompt.txt')
                if r:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 我收到你发来的 system_prompt.txt 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新的 System Prompt 要求来定位我自己, 放心, 我很聪明的 🙂!",
                        msg.chat_id,
                    )
                else:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 我收到你发来的 system_prompt.txt 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨",
                        msg.chat_id,
                    )
        except Exception as e:
            bot.send_msg(f"对不起{msg.user_nick_name}, 你发来的文件我处理不了😮‍💨", msg.chat_id)
        return
