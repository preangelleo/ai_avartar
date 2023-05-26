from urllib.parse import urlencode

import requests

from src.utils.param_singleton import Params
from src.utils.logging_util import logging

TELEGRAME_BASE_URL = "https://api.telegram.org/bot" + Params().TELEGRAM_BOT_RUNNING + "/"


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
