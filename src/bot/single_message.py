from src.utils.constants import DEAR_USER


class SingleMessage:
    def __init__(
        self,
        raw_msg,
        from_id,
        chat_id,
        username,
        first_name,
        last_name,
        is_private,
        msg_text,
        msg_document,
        msg_photo,
        msg_voice,
        msg_audio,
        msg_sticker,
        caption,
        reply_to_message_text,
    ):
        self.raw_msg = raw_msg
        self.from_id = str(from_id)
        self.chat_id = str(chat_id)
        self.username = username
        self.user_title = ' '.join(
            [v for v in [username, first_name, last_name] if 'User' not in v]
        )
        self.is_private = is_private
        # 如果是群聊就要在回复的前缀 亲爱的后面加上 user_title
        self.user_nick_name = (
            DEAR_USER if is_private else f'{DEAR_USER} @{self.user_title} '
        )
        self.first_name = first_name
        self.last_name = last_name
        self.msg_text = msg_text
        self.msg_document = msg_document
        self.msg_photo = msg_photo
        self.msg_voice = msg_voice
        self.msg_audio = msg_audio
        self.msg_sticker = msg_sticker
        self.caption = caption
        self.reply_to_message_text = reply_to_message_text

        # 如果是群聊但是没有 at 机器人, 则打印完消息后直接返回
        self.should_be_ignored = False
