import random
import re
import string

from bot.bot_branch.payment_branch.crpto.utils import get_transactions_info_by_hash_tx, \
    read_and_send_24h_outgoing_trans
from src.bot.bot_branch.bot_branch import BotBranch

from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.chains.question_answering import load_qa_chain

from src.utils.constants import default_system_prompt_file, default_dialogue_tone_file

from src.third_party_api.elevenlabs import *
from src.utils.utils import *
from third_party_api.chatgpt import chat_gpt_regular, chat_gpt_full, chat_gpt_write_story


def create_news_and_audio_from_bing_search(bot, query, chat_id):
    filepath = bing_search(query, mkt='en-US')

    snippet_total = [f"Today's top news about {query}\n\n"]
    with open(filepath, 'r') as file:
        i = 1
        for line in file:
            if 'SNIPPET: ' in line:
                snippet_total.append(line.replace('-', '').replace('SNIPPET: ', f'{str(i)}. '))
                i += 1

    snippet_text_filepath = filepath.replace('.txt', '_snippet.txt')
    with open(snippet_text_filepath, 'w') as file:
        for line in snippet_total:
            file.write(line + '\n')

    filepath_news_mp3 = create_news_podcast(snippet_text_filepath, prompt='')
    filepath_news_txt = filepath_news_mp3.replace('.mp3', '.txt')
    with open(filepath_news_txt, 'r') as f:
        text_contents = f.read()

    bot.send_msg(text_contents, chat_id)

    # filepath_news_txt_cn = filepath_news_txt.replace('.txt', '_cn.txt')
    text_cn = chat_gpt_regular(f"{translate_report_prompt}{text_contents}", Params().OPENAI_API_KEY, Params().OPENAI_MODEL)

    # 将中文文本添加至英文文本的末尾
    with open(filepath_news_txt, 'a') as file:
        file.write(text_cn)
    # with open(filepath_news_txt_cn, 'w') as file: file.write(text_cn)
    bot.send_msg(text_cn, chat_id)
    bot.send_file(chat_id, filepath_news_txt, description='中英文内容 Text 文件')

    filepath_news_mp3_cn = filepath_news_mp3.replace('.mp3', '_cn.mp3')
    filepath_news_mp3_cn = microsoft_azure_tts(text_cn, 'zh-CN-YunxiNeural', filepath_news_mp3_cn)

    merged_audio = merge_audio_files([filepath_news_mp3, filepath_news_mp3_cn])
    bot.send_audio(merged_audio, chat_id)

    # 基于 text_contents 写一段 英文 Tweet 和一段中文 Tweet
    tweet_content = chat_gpt_regular(f"{tweet_pre_prompt_for_report}{text_contents}")
    bot.send_msg(tweet_content, chat_id)

    return


# 定义一个TTS 函数, 判断输入的内容是中文还是英文, 然后调用不同的 TTS API 创建并返回filepath, 如果提供了 chat_id, 则将 filepath send_audio 给用户
def create_audio_from_text(bot, text, chat_id=''):
    if not text: return
    filepath = f"files/audio/{chat_id}_{text[:10]}.mp3" if chat_id else f"files/audio/no_chat_id_{text[:10]}.mp3"

    if is_english(text):
        new_filepath = microsoft_azure_tts(text, 'en-US-JennyNeural', filepath)
    else:
        new_filepath = microsoft_azure_tts(text, 'zh-CN-YunxiNeural', filepath)
    if new_filepath and os.path.isfile(new_filepath):
        bot.send_audio(new_filepath, chat_id)
        return new_filepath



class TextBranch(BotBranch):
    def __init__(self):
        super(TextBranch, self).__init__()

    def handle_single_msg(self, msg, bot):
        # 如果 at 了机器人, 则将机器人的名字去掉
        msg_text = msg.msg_text.replace(f'@{Params().TELEGRAM_BOT_NAME}', '')
        logging.info(f"IGNORE: {msg.user_title} {msg.from_id}: {msg_text}" if msg.should_be_ignored else f"LEGIT: {msg.user_title} {msg.from_id}: {msg_text}")

        msg_lower = msg_text.lower()
        MSG_SPLIT = msg_lower.split()
        MSG_LEN = len(MSG_SPLIT)

        if msg_text.lower().startswith('http'):

            if len(msg_text) < 10 or not '/' in msg_text or not '.' in msg_text: return
            if 'youtube' in msg_text: bot.send_msg("{msg.user_nick_name}我看不了 Youtube 哈, 你发个别的链接给我吧 😂",
                                               msg.chat_id)

            if '/tx/0x' in msg_text:
                hash_tx = msg_text.split('/tx/')[-1]
                if len(hash_tx) != 66: return
                bot.send_msg(
                    f"{msg.user_nick_name}, 你发来的以太坊交易确认链接, 我收到了, 我现在就去研究一下交易信息哈 😗: \n\n{hash_tx}",
                    msg.chat_id)
                try:
                    r = get_transactions_info_by_hash_tx(bot, hash_tx, msg.chat_id, msg.user_title, chain='eth')
                    if r: bot.send_msg(r, msg.chat_id)
                except Exception as e:
                    logging.error(f"local_bot_msg_command() get_transactions_info_by_hash_tx() FAILED: \n\n{e}")
                return

            if 'address/0x' in msg_text:
                eth_address = msg_text.split('address/')[-1]
                eth_address = eth_address.split('#')[0]
                if len(eth_address) != 42: return
                bot.send_msg(
                    f"{msg.user_nick_name}, 你发来的以太坊地址, 我收到了, 我现在就去看一下这个地址上面的 ETH, USDT, USDC 余额哈 😗: \n\n{eth_address}",
                    msg.chat_id)
                # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
                try:
                    # 将 msg_text 转换为 CheckSum 格式
                    eth_address = Web3.to_checksum_address(eth_address)
                    balance = check_address_balance(eth_address)
                    if balance: bot.send_msg(
                        f"{msg.user_nick_name}, 你发的 ETH 地址里有: \n\nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}\n\nChecksum Address:\n{eth_address}",
                        msg.chat_id)
                except Exception as e:
                    return logging.error(f"local_bot_msg_command() check_address_balance() FAILED: \n\n{e}")
                return

            try:
                loader = UnstructuredURLLoader(urls=[MSG_SPLIT[0]])
                documents = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents(documents)

                db = Chroma.from_documents(texts, Params().embeddings)
                retriever = db.as_retriever()

                bot.qa = RetrievalQA.from_chain_type(llm=Params().llm, chain_type="stuff", retriever=retriever)

                query = ' '.join(MSG_SPLIT[
                                 1:]) if MSG_LEN > 1 else "请提炼总结一下此人的 Profile。只需回复内容, 不需要任何前缀标识。" if 'linkedin' in msg_lower else "请为该页面写一个精简但有趣的中文 Tweet。只需回复内容, 不需要任何前缀标识。"
                if 'linkedin' in msg_lower:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。这是个 Linkedin 的链接, 我估计你是想了解这个人的背景, 我先帮你提炼一下哈. ",
                        msg.chat_id)
                else:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。我先假设你是想把这个链接转发到 Twitter, 所以我先帮你写个 Tweet 吧 😁",
                        msg.chat_id)

                reply = bot.qa.run(query)

                try:
                    bot.send_msg(f"{reply}\n{MSG_SPLIT[0]}", msg.chat_id)
                except Exception as e:
                    bot.send_msg(f"ERROR: {msg.chat_id} URL读取失败: \n{e}", msg.chat_id)

            except Exception as e:
                bot.send_msg(f"对不起{msg.user_nick_name}, 你发来的链接我看不了 💦", msg.chat_id)
            return

        # 用户可以通过 save_chat_history /from_id 指令来保存聊天记录
        elif MSG_SPLIT[0] in ['save_chat_history', '/save_chat_history', 'sch', '/sch'] or msg_text == f"/{msg.from_id}":
            file_path = get_user_chat_history(msg.from_id)
            help_info = f'{msg.user_nick_name} 你可以随时发送 /{msg.from_id} 或者 /Save_Chat_History (or /sch) 给我来保存咱俩的聊天记录哈. 😘'
            if os.path.isfile(file_path):
                bot.send_file(msg.chat_id, file_path, description=f"咱俩之间的聊天记录 😁")
            else:
                bot.send_msg(
                    f"{msg.user_nick_name}, 我没有找到你的聊天记录, , 你应该从来没跟我好好聊过吧 😅\n\nP.S. {help_info}",
                    msg.chat_id)
            return

        # Welcome and help
        elif MSG_SPLIT[0] in help_list:
            bot.send_msg(avatar_first_response, msg.chat_id)
            if msg_text in ['/start', 'help', '/help', 'start']:
                if msg_text in ['/start']: insert_new_from_id_to_user_priority_table(msg.from_id)

                bot.send_img(msg.chat_id, Params().avatar_command_png, description=f'任何时候回复 /help 都可以看到这张图片哦 😁',
                         )
                command_help_info = f"这里是我的一些命令, 只要你发给我的消息开头用了这个命令 (后面必须有个空格) , 然后命令之后的内容我就会专门用这个命令针对的功能来处理。下面是一些有趣的命令, 你可以点击了解他们分别是干什么的, 该怎么使用。\n\n{user_commands}\n\n除了这些命令, 我还可以处理一些特殊的文字内容, 比如你发来一个 Crypto 的 Token 名 (不超过 4 个字符), 比如: \n/BTC /ETH /DOGE /APE 等等, \n我都可以帮你查他们的价格和交易量等关键信息; 如果你发来一个单独的英文字母 (超过 4 个字符) 那我会当你的字典, 告诉你这个英文单词的词频排名、发音、以及中文意思, 比如: \n/opulent /scrupulous /ostentatious \n除此之外, 你还可以直接发 /ETH 钱包地址或者交易哈希给我, 我都会尽量帮你读出来里面的信息, {msg.user_nick_name}你不妨试试看呗。\n\n最后, 请记住, 随时回复 /start 或者 /help 就可以看到这个指令集。"
                bot.send_msg(command_help_info, msg.chat_id)
                if msg.chat_id in Params().BOT_OWNER_LIST:
                    bot.send_msg(f"\n{msg.user_nick_name}, 以下信息我悄悄地发给你, 别人都不会看到也不会知道的哈 😉:",
                             msg.chat_id)
                    bot.send_img(msg.chat_id, Params().avatar_png)
                    bot.send_msg(avatar_change_guide, msg.chat_id)
                    bot.send_file(msg.chat_id, default_system_prompt_file)
                    bot.send_msg(about_system_prompt_txt, msg.chat_id)
                    bot.send_file(msg.chat_id, default_dialogue_tone_file)
                    bot.send_msg(about_dialogue_tone_xls, msg.chat_id)
                    bot.send_msg(change_persona, msg.chat_id)
                    bot_owner_command_help_info = f"作为 Bot Onwer, 你有一些特殊的管理命令用来维护我, 请点击查看各自的功能和使用方式吧:\n\n{bot_owner_commands}\n\n最后, 请记住, 随时回复 /start 或者 /help 就可以看到这个指令集。"
                    bot.send_msg(bot_owner_command_help_info, msg.chat_id)
                else:
                    bot.send_msg(Params().avatar_create, msg.chat_id)
                return

        elif msg_text in ['/more_information', 'more_information']:
            return bot.send_msg(Params().avatar_more_information, msg.chat_id)

        elif MSG_SPLIT[0] in ['whoami', '/whoami'] or msg_lower in ['who am i']:
            fn_and_ln = ' '.join([n for n in [msg.first_name, msg.last_name] if 'User' not in n])
            bot.send_msg(f"你是 {fn_and_ln} 呀, 我的宝贝! 😘\n\nmsg.chat_id:\n{msg.chat_id}\n电报链接:\nhttps://t.me/{msg.username}",
                     msg.chat_id)
            return

        # 用户主动发起申请成为 vip (永久免费)用户
        elif msg_lower in ['apply_for_vip', '/apply_for_vip', 'vip', '/vip']:
            insert_new_from_id_to_user_priority_table(msg.from_id)
            # 通知用户申请发送成功
            bot.send_msg(f"{msg.user_nick_name}, 你的 VIP 申请已经发送给 @{Params().TELEGRAM_USERNAME} 了, 请耐心等待老板审批哦 😘",
                     msg.chat_id)
            # 给 bot onwer 发送申请消息
            return bot.send_msg(
                f"user: @{msg.user_title}\nmsg.chat_id: {msg.from_id}\n\n申请成为 VIP 用户:\n\n点击 /vip_{msg.from_id} 同意\n\n如果不能点击就拷贝上面这个指令直接回复给我。",
                Params().BOTOWNER_CHAT_ID)

        # 提交用户自己的 elevenlabs_api_key
        elif msg_text.startswith('/elevenlabs_api_key') or msg_text.startswith('elevenlabs_api_key'):
            elevenlabs_api_key = msg_text.replace('/', '').replace('elevenlabs_api_key', '').strip()
            if not elevenlabs_api_key: return bot.send_msg(eleven_labs_apikey_retrieve_guide, msg.chat_id)
            r = check_and_save_elevenlabs_api_key(bot, elevenlabs_api_key, msg.from_id)
            if r: generate_clone_voice_audio_with_eleven_labs(bot, eleven_labs_english_tranning_text, msg.from_id,
                                                              msg.user_title, folder='files/audio/clone_voice')
            return


            # /clone_my_voice 命令, 用来引导用户克隆自己的声音, 发来一段英文朗读 voice 文件
        elif MSG_SPLIT[0] in ['clone_my_voice', '/clone_my_voice']:
            r = update_elevenlabs_user_ready_to_clone(msg.from_id, msg.user_title)
            if r: bot.send_msg(elevenlabs_clone_voice_guide, msg.chat_id)
            return

        # close_clone_voice
        elif MSG_SPLIT[0] in ['close_clone_voice', '/close_clone_voice']:
            return update_elevenlabs_user_ready_to_clone_to_0(bot, msg.from_id, msg.user_title)

        # update_elevenlabs_user_ready_to_clone_to_0(from_id) if msg_text in ['/confirm_my_voice', 'confirm_my_voice'] else None
        elif MSG_SPLIT[0] in ['confirm_my_voice', '/confirm_my_voice']:
            r = update_elevenlabs_user_ready_to_clone_to_0(bot, msg.from_id, msg.user_title, cmd='confirm_my_voice')
            if r: generate_clone_voice_audio_with_eleven_labs(bot, eleven_labs_english_tranning_text, msg.from_id,
                                                              msg.user_title, folder='files/audio/clone_voice')
            return

            # /speak_my_voice 命令, 用来引导用户用自己的声音朗读英文
        elif MSG_SPLIT[0] in ['speak_my_voice', '/speak_my_voice', '/smv', 'smv']:
            if MSG_LEN == 1: return bot.send_msg(speak_my_voice_guide, msg.chat_id)
            content = ' '.join(msg_text.split()[1:]).strip()
            if is_english(content):
                generate_clone_voice_audio_with_eleven_labs(bot, content, msg.from_id, msg.user_title,
                                                            folder='files/audio/clone_voice')
            else:
                bot.send_msg(
                    f"{msg.user_nick_name}, 你发的不是英文, 目前用你克隆的声音尚且只能朗读英文哦 😁, 如果需要朗读中文, 可以用 /make_voice 指令后面加上这段内容再发给我。",
                    msg.chat_id)
            return

        # /write_story
        elif MSG_SPLIT[0] in ['write_story', '/write_story', '/ws', 'ws']:
            if MSG_LEN == 1: bot.send_msg(write_story_guide, msg.chat_id)
            story_prompt_from_user = 'None' if MSG_LEN == 1 else ' '.join(MSG_SPLIT[1:])
            return chat_gpt_write_story(bot, msg.chat_id, msg.from_id, story_prompt_from_user, gpt_model=Params().OPENAI_MODEL)

        # /read_story
        elif MSG_SPLIT[0] in ['read_story', '/read_story', '/rs', 'rs']:
            title, story = get_gpt_story(msg.from_id)
            generated_with_my_clone_voice = False
            if is_english(story): generated_with_my_clone_voice = generate_clone_voice_audio_with_eleven_labs(bot,
                                                                                                              story,
                                                                                                              msg.from_id,
                                                                                                              msg.user_title,
                                                                                                              folder='files/audio/clone_voice')
            if not generated_with_my_clone_voice: create_audio_from_text(bot, story, msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['password', '/password']:
            # 生成一个长度为 1 位的随机英文字符
            password_prefix = ''.join(random.sample(string.ascii_letters, 1))
            # 生成一个长度为 16 位的随机密码, 不包括特殊字符
            password_temp = ''.join(random.sample(string.ascii_letters + string.digits, 15))
            password = password_prefix + password_temp
            # 生成一个长度为 18 位的随机密码, 包括特殊字符, 开头一定要用英文字符, 特殊字符只能在中间, 数字放在结尾
            special_password_temp = ''.join(random.sample(string.ascii_letters + string.digits + '@$-%^&_*', 17))
            special_password = password_prefix + special_password_temp
            bot.send_msg(
                f"{msg.user_nick_name}, 我为你生成了两个密码:\n\n16位不包含特殊字符密码: \n{password}\n\n18位包含特殊字符密码是: \n{special_password}\n\n请记住你的密码, 你可以把它们复制下来, 然后把这条消息删除, 以免被别人看到哈 😘",
                msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['midjourney', '/midjourney', 'mid', '/mid', 'midjourneyprompt', '/midjourneyprompt']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要创作 Midjourney Prompt, 请在命令后面的空格后再加上你要作画的几个关键词, 比如: \n\nmidjourney 德牧, 未来世界, 机器人\n\n这样我就会用这几个关键词来创作 Midjourney Prompt。\n\nP.S. /midjourney 也可以缩写为 /mid",
                msg.chat_id)
            prompt = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(
                f'收到, {msg.user_nick_name}, 等我 1 分钟. 我马上用 「{prompt}」来给你创作一段富有想象力的 Midjourney Prompt, 并且我还会用 Stable Diffusion 画出来给你参考 😺, 不过 SD 的模型还是不如 MJ 的好, 所以你等下看到我发来的 SD 图片之后, 还可以拷贝 Prompt 到 MJ 的 Discord Bot 那边再创作一下. 抱歉我不能直接连接 MJ 的 Bot, 否则我就直接帮你调用 MJ 接口画好了. 😁',
                msg.chat_id)

            try:
                beautiful_midjourney_prompt = create_midjourney_prompt(prompt)
                if beautiful_midjourney_prompt:
                    try:
                        prompt = beautiful_midjourney_prompt.split('--')[0]
                        if not prompt: return

                        file_list = stability_generate_image(prompt)
                        if file_list:
                            for file in file_list:
                                try:
                                    bot.send_img(msg.chat_id, file, prompt)
                                except:
                                    bot.send_msg(prompt, msg.chat_id)
                    except Exception as e:
                        logging.error(f"stability_generate_image() FAILED: \n\n{e}")

            except Exception as e:
                bot.send_msg(f"ERROR: local_bot_msg_command() create_midjourney_prompt() FAILED: \n\n{e}", msg.chat_id)
            return

            # 发送 feedback 给 bot owner
        elif MSG_SPLIT[0] in ['feedback', '/feedback', '/owner', 'owner']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要给我的老板反馈信息或者提意见, 请在命令后面的空格后再加上你要反馈的信息, 比如: \n\nfeedback 你好, 我是你的粉丝, 我觉得你的机器人很好用, 但是我觉得你的机器人还可以加入xxx功能, 这样就更好用了。\n\n这样我就会把你的反馈信息转发给我老板哈 😋。另外 /feedback 和 /owner 通用\n\n当然, 你也可以跟他私聊哦 @{Params().TELEGRAM_USERNAME}",
                msg.chat_id)
            feedback = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(
                f"收到, {msg.user_nick_name}, 我马上把你的反馈信息转发给我老板哈 😋。你要反馈的信息如下:\n\n{feedback}",
                msg.chat_id)
            feed_back_info = f"来自 @{msg.user_title} /{msg.from_id} 的反馈信息:\n\n{feedback}\n\n如需回复, 请用 /{msg.from_id} 加上你要回复的内容即可。如果点击或发送 /{msg.from_id} 但后面没有任何内容, 我会把 @{msg.user_title} 和我的聊天记录以 TXT 文档形式发给你参考。"
            for owner_chat_id in set(Params().BOT_OWNER_LIST):
                bot.send_msg(feed_back_info, owner_chat_id)
            return

        # image generate function
        elif MSG_SPLIT[0] in ['img', 'ig', 'image', '/img', '/ig', '/image']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要创作图片, 请在命令的空格后再后面加上你的图片描述 (英文会更好) , 比如: \n\nimage 一只可爱的德牧在未来世界游荡\n\n这样我就会用这个创意创作图片。\n\nP.S. /image 也可以缩写为 /img 或者 /ig",
                msg.chat_id)
            prompt = ' '.join(MSG_SPLIT[1:])
            try:
                file_list = stability_generate_image(prompt)
                if file_list:
                    for file in file_list:
                        try:
                            bot.send_img(msg.chat_id, file, prompt)
                        except:
                            logging.error(f"local_bot_msg_command() bot.send_img({file}) FAILED")

            except Exception as e:
                logging.error(f"stability_generate_image() {e}")
            # NSFW content detected. Try running it again, or try a different prompt.
            return

        # chatpdf function
        elif MSG_SPLIT[0] in ['pdf', 'doc', 'txt', 'docx', 'ppt', 'pptx', 'url', 'urls', '/pdf', '/doc', '/txt',
                              '/docx', '/ppt', '/pptx', '/url', '/urls']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要针对刚刚发给我的 PDF 内容进行交流, 请在命令后面的空格后加上你的问题, 比如: \n\npdf 这个 PDF 里介绍的项目已经上市了吗\n\n这样我就知道这个问题是针对刚才的 PDF 的。\n\nP.S. /pdf 也可以换做 /doc 或者 /txt 或者 /docx 或者 /ppt 或者 /pptx 或者 /url 或者 /urls , 不管你刚才发的文档是什么格式的, 这些指令都是一样的, 通用的 (可以混淆使用, 我都可以分辨) 😎",
                msg.chat_id)
            query = ' '.join(MSG_SPLIT[1:])
            try:
                if bot.qa is not None:
                    reply = bot.qa.run(f"{query}\n Please reply with the same language as above prompt.")
                    bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"对不起{msg.user_nick_name}, 我没查到你要的信息. 😫", msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['revise', 'rv', '/revise', '/rv']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 请在命令后面的空格后加上你要改写的内容, 比如: \n\nrevise 这里贴上你要改写的内容。\n\n这样我就会把上面你贴给我的内容用更优雅地方式改写好。中文就改写为中文；英文改写后还是英文。这不是翻译, 是校对和改写。\n\nP.S. /revise 也可以换做 /rv",
                msg.chat_id)
            prompt = ' '.join(MSG_SPLIT[1:])
            try:
                reply = chat_gpt_regular(
                    f"Please help me to revise below text in a more native and polite way, reply with the same language as the text:\n{prompt}",
                    chatgpt_key=Params().OPENAI_API_KEY, use_model=Params().OPENAI_MODEL)
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"对不起{msg.user_nick_name}, 刚才我的网络断线了, 没帮你修改好. 你可以重发一次吗? 😭", msg.chat_id)
            return

            # emoji translate function
        elif MSG_SPLIT[0] in ['emoji', 'emj', 'emo', '/emoji', '/emj', '/emo']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想把你发给我的内容翻译成 emoji, 请在命令后面的空格后加上你的内容, 比如: \n\nemoji 今晚不回家吃饭了, 但是我会想你的。\n\n这样我就会把上面你贴给我的内容用 emoji 来描述。\n\nP.S. /emoji 也可以换做 /emj 或者 /emo",
                msg.chat_id)
            prompt = ' '.join(MSG_SPLIT[1:])
            try:
                new_prompt = f"You know exactly what each emoji means and where to use. I want you to translate the sentences I wrote into suitable emojis. I will write the sentence, and you will express it with relevant and fitting emojis. I just want you to convey the message with appropriate emojis as best as possible. I dont want you to reply with anything but emoji. My first sentence is ( {prompt} ) "
                emj = chat_gpt_regular(new_prompt)
                if emj:
                    try:
                        bot.send_msg(emj, msg.chat_id)
                    except Exception as e:
                        logging.error(f"emoji bot.send_msg() {e}")
            except Exception as e:
                logging.error(f"emoji translate chat_gpt() {e}")
            return

        # translate chinese to english and then generate audio with my voice
        elif MSG_SPLIT[0] in ['ts', 'translate', 'tl', '/ts', '/translate', '/tl', 'tr', '/tr']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想把你发给我的中文内容翻译成英文, 请在命令后面的空格后加上你要翻译的内容, 比如: \n\ntranslate 明天我要向全世界宣布我爱你。\n\n这样我就会把上面你发给我的内容翻译成英文。\n\nP.S. /translate 也可以换做 /ts 或者 /tl",
                msg.chat_id)

            prompt = ' '.join(MSG_SPLIT[1:])

            user_prompt = '''Dillon Reeves, a seventh grader in Michigan, is being praised as a hero for preventing his school bus from crashing after his bus driver lost consciousness. Reeves was seated about five rows back when the driver experienced "some dizziness" and passed out, causing the bus to veer into oncoming traffic. Reeves jumped up from his seat, threw his backpack down, ran to the front of the bus, grabbed the steering wheel and brought the bus to a stop in the middle of the road. Warren police and fire departments responded to the scene within minutes and treated the bus driver, who is now stable but with precautions and is still undergoing testing and observation in the hospital. All students were loaded onto a different bus to make their way home. Reeves' parents praised their son and called him \'our little hero.\''''
            assistant_prompt = '''Dillon Reeves 是一名来自 Michigan 的七年级学生, 因为在校车司机失去意识后成功阻止了校车发生事故而被称为英雄。当时, 司机出现了"一些眩晕"并昏倒, 导致校车偏离行驶道驶入迎面驶来的交通流中。当时 Reeves 坐在车子后面大约五排的位置, 他迅速从座位上站起来, 扔掉背包并跑到车前, 抓住方向盘, 让校车在道路中间停了下来。Warren 警察和消防部门在几分钟内赶到现场, 对校车司机进行救治。司机目前已经稳定下来, 但仍需密切观察并在医院接受检查。所有学生后来被安排上另一辆校车回家。Reeves 的父母赞扬了儿子, 并称他是"我们的小英雄".'''

            try:
                reply = chat_gpt_full(prompt, system_prompt=translation_prompt, user_prompt=user_prompt,
                                      assistant_prompt=assistant_prompt, dynamic_model=Params().OPENAI_MODEL,
                                      chatgpt_key=Params().OPENAI_API_KEY)
            except Exception as e:
                return bot.send_msg(f"{msg.user_nick_name}对不起, 刚才断线了, 你可以再发一次吗 😂", msg.chat_id)

            try:
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                logging.error(f"translate bot.send_msg() FAILED:\n\n{e}")
            return

        elif MSG_SPLIT[0] in ['wolfram', 'wolframalpha', 'wa', 'wf', '/wolfram', '/wolframalpha', '/wa', '/wf']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想用 WolframAlpha 来帮你做科学运算, 请在命令后面的空格后加上你要计算的方程式, 比如: \n\nwolfram 5x + 9y =33; 7x-5y = 12\n\n这样我就知道去用 WolframAlpha 解题。\n\nP.S. /wolfram 也可以换做 /wa 或者 /wf",
                msg.chat_id)
            query = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(f"好嘞, 我帮你去 WolframAlpha 去查一下 「{query}」, 请稍等 1 分钟哦 😁", msg.chat_id)
            try:
                reply = Params().wolfram.run(query)
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"抱歉{msg.user_nick_name}, 没查好, 要不你再发一次 😐", msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['wikipedia', 'wiki', 'wp', 'wk', '/wikipedia', '/wiki', '/wp', '/wk']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想用 Wikipedia 来帮你查资料, 请在命令后面的空格后加上你要查的内容, 比如: \n\nwikipedia Bill Gates\n\n这样我就会用 Wikipedia 去查。\n\nP.S. /wikipedia 也可以换做 /wiki 或者 /wp 或者 /wk",
                msg.chat_id)
            query = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(
                f"收到, {msg.user_nick_name}. 我会去 Wikipedia 帮你查一下 「{query}」, 由于 Wikipedia 查询结果内容较多, 等下查好了直接发个 txt 文件给你.",
                msg.chat_id)
            try:
                reply = Params().wikipedia.run(query)
                # logging.debug(f"wikipedia.run() reply: \n\n{reply}\n\n")
                SAVE_FOLDER = 'files/wikipedia/'
                # Remove special character form query string to save as file name
                query = re.sub('[^A-Za-z0-9]+', '', query)
                # Remove space from query string to save as file name
                query = query.replace(' ', '')
                file_path = f"{SAVE_FOLDER}{query}.txt"
                # Save reply to a text file under SAVE_FOLDER and name as query
                with open(file_path, 'w') as f:
                    f.write(reply)
                # Send the text file to the user
                bot.send_file(msg.chat_id, file_path)
            except Exception as e:
                bot.send_msg(f"抱歉{msg.user_nick_name}, 没查好, 要不你再发一次 😐", msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['twitter', 'tw', 'tweet', 'tt', '/twitter', '/tw', '/tweet', '/tt']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想让我把一段文章内容精简成一个可以发 Twitter 的一句话, 请在命令后面的空格后加上你要发推的内容, 比如: \n\ntwitter 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。”\n\n这样我就要 Twitter 去发推。\n\nP.S. /twitter 也可以换做 /tw 或者 /tweet 或者 /tt",
                msg.chat_id)
            msg_text = ' '.join(MSG_SPLIT[1:])
            prompt = f"请为以下内容写一个精简有趣的中文 Tweet. 只需回复内容, 不需要任何前缀标识。\n\n{msg_text}"
            try:
                reply = chat_gpt_regular(prompt)
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"抱歉{msg.user_nick_name}, 刚断网了, 没弄好, 要不你再发一次 😐", msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['summarize', '/summarize', 'smrz', '/smrz']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 如果你想让我帮你总结一段文字, 请在命令后面的空格后加上你要总结的内容, 比如: \n\nsummarize 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。\n\n这样我就会用精简的语言来帮你总结一下。\n\nP.S. /summarize 也可以换做 /smrz",
                msg.chat_id)
            msg_text = ' '.join(MSG_SPLIT[1:])
            prompt = f"请用精简有力的语言总结以下内容, 并提供中英文双语版本:\n\n{msg_text}"
            try:
                reply = chat_gpt_regular(prompt)
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"抱歉{msg.user_nick_name}, 刚断网了, 没弄好, 要不你再发一次 😐", msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['bing', '/bing']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想用 Bing 搜索引擎来搜索关键词并让我按照搜索结果写一篇中英文报道, 请在命令后面的空格后加上你要搜索关键词, 比如: \n\nbing Pinecone just raised 100 million\n\n这样我就会用 Bing 去搜索并基于搜索结果创作科技新闻报道。我会按顺序一次发给你:\n\n1) 英文报道; \n2) 中文报道; \n3) 英文和中文语音播报; \n4) Twitter 精简短内容!",
                msg.chat_id)
            query = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(
                f"好嘞 {msg.user_nick_name}, 我帮你去 Bing 搜索一下 「{query}」, 然后再基于搜索结果帮你写一篇英文报道、一篇中文报道、一个推特短语还有一段英文+中文的语音 Podcast, 请稍等 2 分钟哦 😁",
                msg.chat_id)
            try:
                create_news_and_audio_from_bing_search(bot, query, msg.chat_id)
            except Exception as e:
                logging.error(f"create_news_and_audio_from_bing_search() failed: {e}")
            return

            # chatpdf function
        elif (MSG_SPLIT[0] in ['outlier', 'oi', 'outlier-investor', 'outlierinvestor', 'ol', '/outlier', '/oi',
                               '/outlier-investor', '/outlierinvestor',
                               '/ol'] or '投资异类' in msg_text or '/投资异类' in msg_text) and Params().TELEGRAM_BOT_NAME.lower() in [
            'leowang_bot']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想让了解我写的《投资异类》里的内容, 请在命令后面的空格后加上你想了解的内容, 比如: \n\n投资异类 天使投资人最喜欢什么样的创业者\n\n这样我就会去《投资异类》里查找相关内容并提炼总结给你。\n\nP.S. /投资异类 也可以换做 /outlier 或者 /oi 或者 /outlier-investor 或者 /outlierinvestor 或者 /ol",
                msg.chat_id)
            query = ' '.join(MSG_SPLIT[1:])
            bot.send_msg("WoW, 你想了解我写的《投资异类》啊, 真是感动. 稍等 1 分钟, 你问的问题我认真写给你, 哈哈哈 😁",
                     msg.chat_id)
            try:
                index_name = 'outlier-investor'
                # docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

                docsearch = Pinecone.from_existing_index(index_name, Params().embeddings)

                chain = load_qa_chain(Params().llm, chain_type="stuff")
                docs = docsearch.similarity_search(query)
                reply = chain.run(input_documents=docs, question=query)
                bot.send_msg(reply, msg.chat_id)
            except Exception as e:
                bot.send_msg(f"{msg.user_nick_name}对不起, 我想不起来我书里还有这个内容了, 让你失望了. ", msg.chat_id)
                logging.error(f"local_bot_msg_command() chatpdf(投资异类) FAILED: \n\n{e}")

            return

        elif MSG_SPLIT[0] in ['avatar', '/avatar', 'my_avatar', 'myavatar'] or msg_lower in ['my avatar']:
            bot.send_img(msg.chat_id, Params().avatar_png)
            return

        elif MSG_SPLIT[0] in ['clear_memory', 'clm', '/clear_memory', '/clm']:
            if MSG_LEN >= 2 and msg.chat_id in Params().BOT_OWNER_LIST and MSG_SPLIT[1] == 'all':
                try:
                    with Params().Session() as session:
                        stmt = sqlalchemy.update(ChatHistory).values(msg_text=None)
                        session.execute(stmt)
                        session.commit()
                        bot.send_msg(f"{msg.user_nick_name}, 我已经删除所有用户的聊天记录, 大家可以重新开始跟我聊天了。😘",
                                 msg.chat_id)
                except Exception as e:
                    logging.error(f"local_bot_msg_command() clear_chat_history() FAILED:\n\n{e}")
                return

                # Delete chat records in avatar_chat_history with from_id = from_id
            try:
                with Params().Session() as session:
                    stmt = sqlalchemy.update(ChatHistory).values(msg_text=None).where(ChatHistory.msg.from_id == msg.from_id)
                    session.execute(stmt)
                    session.commit()
                    bot.send_msg(f"{msg.user_nick_name}, 我已经删除你的聊天记录, 你可以重新开始跟我聊天了。😘", msg.chat_id)
            except Exception as e:
                logging.error(f"local_bot_msg_command() clear_chat_history() FAILED:\n\n{e}")
            return

        # 为用户输入的内容生成音频并发送
        elif MSG_SPLIT[0] in ['make_voice', '/make_voice', 'generate_audio', '/generate_audio', 'gv', '/gv',
                              'make_audio', '/make_audio', 'ma', '/ma', 'mv', '/mv', 'ga', '/ga', 'generate_voice',
                              '/generate_voice']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你如果想让我把一段文字内容转换成语音, 请在命令后面的空格后加上你要转换的内容, 比如: \n\nmake_voice 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。\n\n这样我就知道你要我把这段文字转换成语音了。😚 \n\n/make_voice 可以简写为 /mv 哈",
                msg.chat_id)
            content = ' '.join(MSG_SPLIT[1:])
            bot.send_msg(f"好嘞 {msg.user_nick_name}, 我帮你把以下内容转换成语音, 请稍等 1 分钟哦 😁\n\n{content}", msg.chat_id)
            try:
                create_audio_from_text(bot, content, msg.chat_id)
            except Exception as e:
                logging.error(f"create_audio_from_text() failed: {e}")
            return

        elif MSG_SPLIT[0] in ['commands', '/commands', 'command', '/command', 'cmd', '/cmd']:
            bot.send_msg(user_commands, msg.chat_id)
            if msg.chat_id in Params().BOT_OWNER_LIST: bot.send_msg(bot_owner_commands, msg.chat_id, parse_mode='',
                                                   )
            return

        # 查询以太坊地址余额
        elif (msg_lower.startswith('0x') and len(msg_text) == 42) or (
                msg_lower.startswith('/0x') and len(msg_text) == 43):
            msg_text = msg_text.replace('/', '')
            # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
            try:
                # 将 msg_text 转换为 CheckSum 格式
                eth_address = Web3.to_checksum_address(msg_text)
                balance = check_address_balance(eth_address)
                if balance: bot.send_msg(
                    f"{msg.user_nick_name}, 你发的 ETH 地址里有: \n\nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}\n\nChecksum Address:\n{eth_address}",
                    msg.chat_id)
            except Exception as e:
                return logging.error(f"local_bot_msg_command() check_address_balance() FAILED: \n\n{e}")
            try:
                read_and_send_24h_outgoing_trans(bot, eth_address, msg.chat_id)
            except Exception as e:
                return logging.error(f"read_and_send_24h_outgoing_trans() FAILED: \n\n{e}")
            return

        # 查询以太坊链上交易 Transaction Hash
        elif (msg_lower.startswith('0x') and len(msg_text) == 66) or (
                msg_lower.startswith('/0x') and len(msg_text) == 67):
            hash_tx = msg_text.replace('/', '')
            try:
                r = get_transactions_info_by_hash_tx(bot, hash_tx, msg.chat_id, msg.user_title, chain='eth')
                if r: bot.send_msg(r, msg.chat_id)
            except Exception as e:
                logging.error(f"local_bot_msg_command() get_transactions_info_by_hash_tx() FAILED: \n\n{e}")
            return
