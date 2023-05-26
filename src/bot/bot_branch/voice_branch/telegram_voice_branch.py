from src.bot.bot_branch.voice_branch.voice_branch import VoiceBranch
from third_party_api.elevenlabs import elevenlabs_user_ready_to_clone, update_elevenlabs_user_original_voice_filepath
from src.utils.utils import *


class TelegramVoiceBranch(VoiceBranch):
    def __init__(self):
        super(VoiceBranch, self).__init__()

    def handle_single_msg(self, msg, bot):
        tg_msg = msg.raw_msg
        if msg.is_private and elevenlabs_user_ready_to_clone(msg.from_id):
            file_id = tg_msg['message']['voice'].get('file_id', '')
            file_unique_id = tg_msg['message']['voice'].get('file_unique_id', '')
            if not file_id or not file_unique_id: return

            ''' 音频文件返回结果示例:
            {"update_id": 843018592,
            "message": {
                "message_id": 150,
                "from": {
                "id": 2118900665,
                "is_bot": false,
                "first_name": "Old_Bro_Leo",
                "username": "laogege6",
                "language_code": "zh-hans",
                "is_premium": true
                },
                "chat": {
                "id": 2118900665,
                "first_name": "Old_Bro_Leo",
                "username": "laogege6",
                "type": "private"
                },
                "date": 1684825362,
                "voice": {
                "duration": 4,
                "mime_type": "audio/ogg",
                "file_id": "AwACAgUAAxkBAAOWZGxlEhJjAWMFPocIIpypGREQ8LUAAm8HAAJNs2FXtj9HUXJQ0SMvBA",
                "file_unique_id": "AgADbwcAAk2zYVc",
                "file_size": 17656
                }}}
            '''

            clone_folder = 'files/audio/clone_voice'
            if not os.path.isdir(clone_folder): os.mkdir(clone_folder)

            user_folder = f"{clone_folder}/{msg.from_id}"
            if not os.path.isdir(user_folder): os.mkdir(user_folder)

            user_original_voice_folder = f"{user_folder}/original_voice"
            if not os.path.isdir(user_original_voice_folder): os.mkdir(user_original_voice_folder)

            # Create local file name to store voice telegram message
            local_file_folder_name = f"{user_original_voice_folder}/{file_unique_id}.ogg"
            # Get the file path of the voice message using the Telegram Bot API
            file_path_url = f"https://api.telegram.org/bot{Params().TELEGRAM_BOT_RUNNING}/getFile?file_id={file_id}"
            file_path_response = requests.get(file_path_url).json()

            file_path = file_path_response["result"]["file_path"]
            # Download the voice message to your Ubuntu folder
            voice_message_url = f"https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_RUNNING}/{file_path}"

            with open(local_file_folder_name, "wb") as f:
                response = requests.get(voice_message_url)
                f.write(response.content)

            original_voice_filepath = local_file_folder_name.replace('.ogg', '.mp3')
            command = f"ffmpeg -n -i {local_file_folder_name} {original_voice_filepath}"
            subprocess.run(command, shell=True)
            if os.path.exists(local_file_folder_name): os.remove(local_file_folder_name)

            if update_elevenlabs_user_original_voice_filepath(original_voice_filepath, msg.from_id,
                                                              msg.user_title): return bot.send_msg(
                f"{msg.user_nick_name} 我收到了你发来的英文素材, 已经保存下来了, 如果你觉得没问题就点击或者发送:\n\n/confirm_my_voice \n\n然后我就可以用这段素材帮你克隆你的声音样本咯, 以后你随时可以调用 /speak_my_voice 指令来用你这个声音阅读任何英文内容 😁...、\n\n如果不满意就重新念一段, 我会耐心等着你读完的...",
                msg.chat_id)

        bot.send_msg(
            f'{msg.user_nick_name}我收到了你发来的语音, 稍等我 1 分钟, 我马上戴上耳机听一下你说的什么 😁...',
            msg.chat_id)
        msg.msg_text = deal_with_voice_to_text(
            file_id=tg_msg['message']['voice'].get('file_id'),
            file_unique_id=tg_msg['message']['voice'].get('file_unique_id'))
