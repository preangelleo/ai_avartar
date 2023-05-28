from src.utils.constants import DEAR_USER
import json


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


def build_from_telegram_msg(tg_msg):
    # Handle any file if available
    return SingleMessage(
        raw_msg=tg_msg,
        from_id=tg_msg['message']['from']['id'],
        chat_id=tg_msg['message']['chat']['id'],
        username=tg_msg['message']['from'].get('username', 'User'),
        first_name=tg_msg['message']['from'].get('first_name', 'User_first_name'),
        last_name=tg_msg['message']['from'].get('last_name', 'User_last_name'),
        # 判断是私聊还是群聊
        is_private=(tg_msg['message']['chat']['type'] == 'private'),
        msg_text=tg_msg['message'].get('text'),
        msg_document=tg_msg['message'].get('document'),
        msg_photo=tg_msg['message'].get('photo'),
        msg_voice=tg_msg['message'].get('voice'),
        msg_audio=tg_msg['message'].get('audio'),
        msg_sticker=tg_msg['message'].get('sticker', {}).get('emoji'),
        caption=tg_msg['message'].get('caption', ''),
        reply_to_message_text=tg_msg['message'].get('reply_to_message', {}).get('text'),
    )


def build_from_fanbook_msg(obj):
    data_str = obj.get('data').get('content')
    data_dict = json.loads(data_str)
    return SingleMessage(
        raw_msg=obj,
        from_id=obj.get('data').get('user_id'),
        chat_id=obj.get('data').get('channel_id'),
        username=obj.get('data').get('author').get('username'),
        first_name=obj.get('data').get('author').get('nickname'),
        # there is no last name or firstname in fanbook
        last_name=obj.get('data').get('author').get('nickname'),
        # 判断是私聊还是群聊
        is_private=None,
        msg_text=data_dict.get('text'),
        msg_document=None,
        msg_photo=None,
        msg_voice=None,
        msg_audio=None,
        msg_sticker=None,
        caption=None,
        reply_to_message_text=None,
    )
