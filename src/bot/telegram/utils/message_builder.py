import json
from src.bot.single_message import SingleMessage


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
        is_mentioned=False,
        reply_to_message_text=tg_msg['message'].get('reply_to_message', {}).get('text'),
        message_id=None,
    )
