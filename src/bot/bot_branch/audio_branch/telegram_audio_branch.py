from src.bot.telegram.utils.utils import tg_get_file_path
from src.bot.bot_branch.audio_branch.audio_branch import AudioBranch
from src.utils.utils import *


class TelegramAudioBranch(AudioBranch):
    def __init__(self):
        super(AudioBranch, self).__init__()

    def handle_single_msg(self, msg, bot):
        tg_msg = msg.raw_msg

        audio_caption = msg.caption
        if audio_caption and audio_caption.split()[0].lower() in ['group_send_audio',
                                                                  'gsa'] and msg.chat_id in Params().BOT_OWNER_LIST:
            file_name = tg_msg['message']['audio'].get('file_name', '')
            file_id = tg_msg['message']['audio']['file_id']
            file_path = tg_get_file_path(file_id)
            file_path = file_path.get('file_path', '')
            if not file_path:
                return

            SAVE_FOLDER = 'files/tg_received'
            save_file_path = f'{SAVE_FOLDER}/{file_name}'
            file_url = f'https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_RUNNING}/{file_path}'
            with open(save_file_path, 'wb') as f:
                f.write(requests.get(file_url).content)

            bot.send_msg(
                f'{msg.user_nick_name}我收到了你发来的语音, 请稍等 1 分钟, 我马上把这个语音发给所有人 😁...',
                msg.chat_id)
            bot.send_audio_to_all(msg, save_file_path, bot_owner_chat_id=msg.chat_id)
