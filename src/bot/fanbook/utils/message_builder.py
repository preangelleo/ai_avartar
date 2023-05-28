import json
from src.bot.single_message import SingleMessage
from src.bot.fanbook.utils.constants import (
    PRIVATE_CHANNEL_TYPE,
)

def build_from_fanbook_msg(obj):
    data_str = obj.get('data').get('content')
    data_dict = json.loads(data_str)
    channel_type = obj.get('data').get('channel_type')
    return SingleMessage(
        raw_msg=obj,
        from_id=obj.get('data').get('user_id'),
        chat_id=obj.get('data').get('channel_id'),
        username=obj.get('data').get('author').get('username'),
        first_name=obj.get('data').get('author').get('nickname'),
        # there is no last name or firstname in fanbook
        last_name=obj.get('data').get('author').get('nickname'),
        # 判断是私聊还是群聊
        is_private=channel_type == PRIVATE_CHANNEL_TYPE,
        msg_text=data_dict.get('text'),
        msg_document=None,
        msg_photo=None,
        msg_voice=None,
        msg_audio=None,
        msg_sticker=None,
        caption=None,
        reply_to_message_text=None,
    )
