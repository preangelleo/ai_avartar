from src.bot.single_message import build_from_fanbook_msg, SingleMessage
from src.utils.logging_util import logging

import requests
from src.bot.bot import Bot
import json
import base64
import threading
from websocket._core import create_connection
import time
from src.bot.fanbook.utils.constants import (
    FAN_BOOK_BOT_NAME,
    FAN_BOOK_GET_ME_URL,
    FAN_BOOK_SEND_MSG_URL,
    HEAT_BEAT_INTERVAL,
    FANBOOK_CLIENT_ID,
    DEVICE_ID,
    FANBOOK_VERSION,
    GET_USER_TOKEN_TIMEOUT_COUNT,
)
from third_party_api.chatgpt import local_chatgpt_to_reply
from utils.utils import save_avatar_chat_history


class FanbookBot(Bot):
    def send_audio(self, audio_path, chat_id):
        # TODO(kezhang@): implement or leave it as None if you don't want to support this in fanbook
        pass

    def send_img(self, chat_id, file_path, description=''):
        # TODO(kezhang@): implement or leave it as None if you don't want to support this in fanbook
        pass

    def send_file(self, chat_id, file_path, description=''):
        # TODO(kezhang@): implement or leave it as None if you don't want to support this in fanbook
        pass

    def __init__(self, *args, **kwargs):
        super(FanbookBot, self).__init__(*args, **kwargs)
        self.fanbook_client_id = FANBOOK_CLIENT_ID
        self.header_map = json.dumps(
            {
                'device_id': DEVICE_ID,
                'version': FANBOOK_VERSION,
                'platform': 'bot',
                'channel': 'office',
                'build_number': '1',
            }
        )
        self.user_token = self.get_user_token()
        self.super_str = base64.b64encode(
            self.header_map.encode('utf8')
        ).decode(  # noqa
            'utf8'
        )  # noqa
        self.addr = f'wss://gateway-bot.fanbook.mobi/websocket?id={self.user_token}&dId={DEVICE_ID}&v={FANBOOK_VERSION}&x-super-properties={self.super_str}'  # noqa

    def get_user_token(self):
        response = requests.get(
            FAN_BOOK_GET_ME_URL, timeout=GET_USER_TOKEN_TIMEOUT_COUNT
        )
        return response.json()['result']['user_token']

    def handle_push(self, obj):
        is_bot = obj.get('data').get('author').get('bot')
        if is_bot:
            return
        channel_id = obj.get('data').get('channel_id')
        author = obj.get('data').get('author').get('nickname')
        if not channel_id or not author:
            return

        logging.info(f'handle_push(): {obj}')
        self.handle_single_msg(build_from_fanbook_msg(obj))

    def handle_single_msg(self, msg: SingleMessage):
        # TODO: slowly migrate and test functions from bot.py
        try:
            save_avatar_chat_history(
                msg.msg_text,
                msg.chat_id,
                msg.from_id,
                msg.username,
                msg.first_name,
                msg.last_name,
            )
        except Exception as e:
            return logging.error(f'save_avatar_chat_history() failed: {e}')

        reply = local_chatgpt_to_reply(self, msg.msg_text, msg.from_id, msg.chat_id)

        if reply:
            try:
                self.send_msg(reply, msg.chat_id)
            except Exception as e:
                logging.error(f'local_chatgpt_to_reply() send_msg() failed : {e}')

    def send_msg(self, msg: str, chat_id, parse_mode=None):
        headers = {'Content-type': 'application/json'}
        payload = {'chat_id': int(chat_id), 'text': msg, 'desc': msg}

        response = requests.post(
            FAN_BOOK_SEND_MSG_URL, data=json.dumps(payload), headers=headers
        )
        logging.debug(f'send_msg(): {response.json()}')
        return response.json()

    def send_ping(self, ws):
        while True:
            time.sleep(HEAT_BEAT_INTERVAL)
            ws.send("{'type':'ping'}")

    def handle_heart_beat(self, ws):
        ping_thread = threading.Thread(target=self.send_ping, args=(ws,))
        ping_thread.daemon = True
        ping_thread.start()

    def handle_websocket_connection(self):
        ws = create_connection(self.addr)
        self.handle_heart_beat(ws)
        try:
            while True:
                s = ws.recv().decode('utf8')
                obj = json.loads(s)
                if obj.get('action') == 'push':
                    self.handle_push(obj)
        except ConnectionError:
            logging.error('WebSocketClosed')
        except Exception as e:
            logging.error('WebSocketError: ', e)

    def run(self):
        self.handle_websocket_connection()


if __name__ == '__main__':
    FanbookBot(
        bot_name=FAN_BOOK_BOT_NAME,
        # TODO(kezhang@): You should either implement these 4 branch for Fanbook or replace them with NoOpBranch
        document_branch_handler=None,
        photo_branch_handler=None,
        voice_branch_handler=None,
        audio_branch_handler=None,
        improper_branch_handler=None,
        text_branch_handler=None,
        payment_branch_handler=None,
        check_bill_branch_handler=None,
        bot_owner_branch_handler=None,
        english_teacher_branch_handler=None,
        coinmarketcap_branch_handler=None,
        bot_owner_id='',
        bot_creator_id='',
    ).run()
