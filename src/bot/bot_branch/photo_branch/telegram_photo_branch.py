from src.bot.telegram.utils.utils import tg_get_file_path
from src.bot.bot_branch.photo_branch.photo_branch import PhotoBranch
from src.utils.utils import *


class TelegramPhotoBranch(PhotoBranch):
    def __init__(self):
        super(TelegramPhotoBranch, self).__init__()

    def handle_single_msg(self, msg, bot):
        logging.debug(f"photo in tg message")
        tg_msg = msg.raw_msg

        description = ''
        # 读出 Photo 的caption, 如果有的话
        caption = msg.caption
        if caption and caption.split()[0].lower() in ['group_send_image', 'gsi',
                                                      'group send image'] and msg.chat_id in Params().BOT_OWNER_LIST:
            group_send_image = True
            description = ' '.join(caption.split()[1:])
            bot.send_msg(
                f'{msg.user_nick_name}我收到了你发来的图片, 请稍等 1 分钟, 我马上把这张图片发给所有人 😁...',
                msg.chat_id)
        else:
            group_send_image = False
            bot.send_msg(
                f'{msg.user_nick_name}我收到了你发来的图片, 请稍等 1 分钟, 我找副眼镜来仔细看看这张图的内容是什么 😺...',
                msg.chat_id)
        try:
            # specify the folder path where you want to save the received images
            SAVE_FOLDER = 'files/images/tg_received/'
            file_id = tg_msg.get('message').get('photo')[-1].get('file_id')
            logging.debug(f"photo file_id: {file_id}")
            # use the Telegram bot API to get the file path
            file_path = tg_get_file_path(file_id)
            file_path = file_path.get('file_path', '')
            if not file_path: return
            logging.debug(f"photo file_path: {file_path}")
        except Exception as e:
            logging.error(f"TelegramDocumentBranch.handle_single_msg failed: \n{e}")
            return

        # construct the full URL for the file
        file_url = f'https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_RUNNING}/{file_path}'
        # get the content of the file from the URL
        try:
            file_content = requests.get(file_url).content
            # save the file to the specified folder with the same file name as on Telegram
            file_name = file_path.split('/')[-1]
            save_path = os.path.join(SAVE_FOLDER, file_name)
            logging.debug(f"photo save_path: {save_path}")
            with open(save_path, 'wb') as f:
                f.write(file_content)
        except Exception as e:
            logging.error(f"photo get file_content failed: \n\n{e}")
            return

        if group_send_image: return bot.send_img_to_all(msg, save_path, description, msg.chat_id)

        img_caption = replicate_img_to_caption(save_path)
        if 'a computer screen' in img_caption: return

        img_caption = img_caption.replace('Caption: ', '')
        bot.send_msg(
            f'宝贝我看清楚了, 这张图的内容是 {img_caption}, 请再稍等 1 分钟, 我马上根据这张图片写一个更富有想象力的 Midjourney Prompt, 你可以用 Midjourney 的 Discord bot 生成更漂亮的图片 😁...',
            msg.chat_id)

        beautiful_midjourney_prompt = create_midjourney_prompt(img_caption)
        if beautiful_midjourney_prompt:
            bot.send_msg(beautiful_midjourney_prompt, msg.chat_id)
            save_avatar_chat_history(img_caption, msg.chat_id, msg.from_id, msg.username, msg.first_name, msg.last_name)
            store_reply = beautiful_midjourney_prompt.replace("'", "")
            store_reply = store_reply.replace('"', '')
            with Params().Session() as session:
                # Create a new chat history record
                new_record = ChatHistory(
                    first_name='ChatGPT',
                    last_name='Bot',
                    username=Params().TELEGRAM_BOT_NAME,
                    from_id=msg.from_id,
                    chat_id=msg.chat_id,
                    update_time=datetime.now(),
                    msg_text=store_reply,
                    black_list=0
                )
                # Add the new record to the session
                session.add(new_record)
                # Commit the session
                session.commit()
        return
