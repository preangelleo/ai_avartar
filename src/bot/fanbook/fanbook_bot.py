from src.bot.bot_branch.bot_owner_branch.bot_owner_branch import BotOwnerBranch
from src.bot.bot_branch.coinmarketcap_branch.coinmarketcap_branch import CoinMarketCapBranch
from src.bot.bot_branch.english_teacher_branch.english_teacher_branch import EnglishTeacherBranch
from src.bot.bot_branch.improper_branch.improper_branch import ImproperBranch
from src.bot.bot_branch.payment_branch.crpto.check_bill_branch import CheckBillBranch
from src.bot.bot_branch.payment_branch.crpto.payment_branch import PaymentBranch
from src.bot.bot_branch.text_branch.text_branch import TextBranch
import requests
from src.bot.bot import Bot
import json
import base64
import threading
from websocket._core import create_connection
import time
from constants import (
    FAN_BOOK_GET_ME_URL,
    FAN_BOOK_SEND_MSG_URL,
    HEAT_BEAT_INTERVAL,
    FANBOOK_CLIENT_ID,
    DEVICE_ID,
    FANBOOK_VERSION,
    GET_USER_TOKEN_TIMEOUT_COUNT,
)


class FanbookBot(Bot):
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

    def handle_single_msg(self, message):
        s = message.decode('utf8')
        obj = json.loads(s)
        if obj.get('action') == 'push':
            self.handle_push(obj)

    def handle_push(self, obj):
        is_bot = obj.get('data').get('author').get('bot')
        if is_bot:
            return

        channel_id = obj.get('data').get('channel_id')
        author = obj.get('data').get('author').get('nickname')
        if not channel_id or not author:
            return

        self.send_message('hello', channel_id)

    def send_message(self, message, chat_id):
        headers = {'Content-type': 'application/json'}
        payload = {'chat_id': int(chat_id), 'text': message, 'desc': message}

        response = requests.post(
            FAN_BOOK_SEND_MSG_URL, data=json.dumps(payload), headers=headers
        )
        print(response.json())
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
                evt_data = ws.recv()
                self.handle_single_msg(evt_data)
        except ConnectionError:
            print('WebSocketClosed')
        except Exception as e:
            print('WebSocketError: ', e)

    def run(self):
        self.handle_websocket_connection()


if __name__ == '__main__':
    FanbookBot(
        document_branch_handler=None,
        photo_branch_handler=None,
        voice_branch_handler=None,
        audio_branch_handler=None,
        improper_branch_handler=ImproperBranch(),
        text_branch_handler=TextBranch(),
        payment_branch_handler=PaymentBranch(),
        check_bill_branch_handler=CheckBillBranch(),
        bot_owner_branch_handler=BotOwnerBranch(),
        english_teacher_branch_handler=EnglishTeacherBranch(),
        coinmarketcap_branch_handler=CoinMarketCapBranch(),
    ).run()
