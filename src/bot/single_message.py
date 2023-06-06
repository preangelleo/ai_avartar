from src.utils.constants import DEAR_USER
from src.utils.logging_util import logging


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
        is_mentioned,
        reply_to_message_text,
    ):
        self.raw_msg = raw_msg
        self.from_id = str(from_id)
        self.chat_id = str(chat_id)
        self.username = username
        self.user_title = ' '.join([v for v in [username, first_name, last_name] if v is not None and 'User' not in v])
        self.is_private = is_private
        # 如果是群聊就要在回复的前缀 亲爱的后面加上 user_title
        self.user_nick_name = DEAR_USER if is_private else f'{DEAR_USER} @{self.user_title} '
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
        self.is_mentioned = is_mentioned

    @property
    def should_be_ignored(self) -> bool:
        if self.is_private:
            logging.info(f'bot is in private chat: {self.raw_msg}')
            return False
        if self.is_mentioned:
            logging.info(f'bot is mentioned in msg: {self.raw_msg}')
            return False
        return True
