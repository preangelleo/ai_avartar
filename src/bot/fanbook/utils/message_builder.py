import json
import logging
from typing import Optional

from src.bot.single_message import SingleMessage
from src.bot.fanbook.utils.constants import (
    PRIVATE_CHANNEL_TYPE,
)
import re
from src.utils.param_singleton import Params


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
        last_name=None,
        # 判断是私聊还是群聊
        is_private=channel_type == PRIVATE_CHANNEL_TYPE,
        msg_text=sanitize_msg_text(data_dict.get('text')),
        msg_document=None,
        msg_photo=None,
        msg_voice=None,
        msg_audio=None,
        msg_sticker=None,
        caption=None,
        is_mentioned=check_if_bot_is_mentioned(obj.get('data').get('mentions')),
        reply_to_message_text=None,
    )


def check_if_bot_is_mentioned(mentions: Optional[list]) -> bool:
    if not mentions:
        return False
    logging.debug(f'msg mentions: {mentions}')
    for mention in mentions:
        if mention.get('user_id') == Params().FANBOOK_BOT_NAME:
            return True
    return False


def sanitize_msg_text(msg_text: str) -> str:
    return re.sub(r'\$\{@![\d]+\}', '', msg_text).strip()
