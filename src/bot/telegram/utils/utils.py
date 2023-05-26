from urllib.parse import urlencode

import requests

from src.utils.param_singleton import Params
from src.utils.logging_util import logging
from src.third_party_api.openai_whisper import from_voice_to_text

TELEGRAME_BASE_URL = "https://api.telegram.org/bot" + Params().TELEGRAM_BOT_TOKEN + "/"


def get_send_msg_url():
    return TELEGRAME_BASE_URL + "sendMessage"


def get_send_audio_url():
    return TELEGRAME_BASE_URL + "sendAudio"


def get_send_img_url(chat_id, description):
    return TELEGRAME_BASE_URL + "sendPhoto?chat_id=" + str(chat_id) + "&caption=" + description


def get_send_file_url(chat_id, description):
    return TELEGRAME_BASE_URL + "sendDocument?chat_id=" + str(chat_id) + "&caption=" + description


def get_get_file_url():
    return TELEGRAME_BASE_URL + "getFile"


def tg_get_file_path(file_id):
    url = get_get_file_url()
    payload = {"file_id": file_id}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return
        return response.json()['result']
    except Exception as e:
        return print(f"ERROR: tg_get_file_path() failed: \n{e}")


# Get updates from telegram server
def local_bot_getUpdates(previous_update_id):
    method = "getUpdates?"
    _params = {
        "offset": previous_update_id,
        "timeout": 123,
        "limit": 10
        }
    params = urlencode(_params)
    URL = TELEGRAME_BASE_URL + method + params
    r = ''
    try: r = requests.get(URL)
    except Exception as e: logging.error(f"local_bot_getUpdates() failed: \n{e}")
    return r


def deal_with_voice_to_text(file_id, file_unique_id):
    print(f"DEBUG: deal_with_voice_to_text()")
    text = ''  # Create an empty text
    # Create local file name to store voice telegram message
    local_file_folder_name = f"files/audio/{file_unique_id}.ogg"
    # Get the file path of the voice message using the Telegram Bot API
    file_path_url = f"{TELEGRAME_BASE_URL}getFile?file_id={file_id}"
    try:
        file_path_response = requests.get(file_path_url).json()
    except Exception as e:
        return print(f"ERROR: deal_with_voice_to_text() download failed: \n{e}")

    file_path = file_path_response["result"]["file_path"]
    # Download the voice message to your Ubuntu folder
    voice_message_url = f"https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_TOKEN}/{file_path}"
    try:
        with open(local_file_folder_name, "wb") as f:
            response = requests.get(voice_message_url)
            f.write(response.content)
        text = from_voice_to_text(local_file_folder_name)
        if text: return text
    except Exception as e:
        print(f"ERROR: from_voice_to_text() 2 FAILED of: \n\n{e}")
    return


def clear_chat_history(bot, chat_id, message_id):
    message_id = int(message_id)
    # 删除之前的聊天记录 (message_id 从大到小直到 0)
    for i in range(message_id, message_id - 20, -1):
        try:
            response = requests.get(
                f'https://api.telegram.org/bot{Params().TELEGRAM_BOT_TOKEN}/deleteMessage?chat_id={chat_id}&message_id={str(i)}')
            if response.status_code == 200: bot.send_msg(
                f"成功删除用户 giiitte < chat_id: {chat_id} > 的聊天记录 message_id: {i}", bot.bot_owner_id)
        except:
            logging.error(f'Failed to delete User chat_id: {chat_id} message_id: {i}')
    return
