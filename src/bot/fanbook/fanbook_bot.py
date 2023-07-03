import time

from src.utils.logging_util import logging
from src.bot.fanbook.utils.message_builder import build_from_fanbook_msg

import requests
from src.bot.bot import Bot
import sentry_sdk
import json
import base64
import websockets
import asyncio
import httpx
from src.bot.fanbook.utils.constants import (
    FANBOOK_BOT_NAME,
    FANBOOK_BOT_OWNER_NAME,
    FANBOOK_BOT_OWNER_ID,
    FANBOOK_BOT_CREATOR_ID,
    FANBOOK_GET_ME_URL,
    FANBOOK_SEND_MSG_URL,
    HEAT_BEAT_INTERVAL,
    FANBOOK_CLIENT_ID,
    DEVICE_ID,
    FANBOOK_VERSION,
    GET_USER_TOKEN_TIMEOUT_COUNT,
    TEST_BOT_ID,
    FANBOOK_BOT_ID,
    FANBOOK_SEND_IMAGE_URL,
)
from src.bot.bot_branch.no_op_branch.no_op_branch import NoOpBranch
from prometheus_client import start_http_server

from src.utils.metrics import SEND_MSG_LATENCY_METRICS, SEND_IMAGE_LATENCY_METRICS
from src.utils.param_singleton import Params


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
        self.super_str = base64.b64encode(self.header_map.encode('utf8')).decode('utf8')  # noqa  # noqa
        self.addr = f'wss://gateway-bot.fanbook.mobi/websocket?id={self.user_token}&dId={DEVICE_ID}&v={FANBOOK_VERSION}&x-super-properties={self.super_str}'  # noqa

    def get_user_token(self):
        response = requests.get(FANBOOK_GET_ME_URL, timeout=GET_USER_TOKEN_TIMEOUT_COUNT)
        return response.json()['result']['user_token']

    async def handle_push(self, obj):
        is_bot = obj.get('data', {}).get('author', {}).get('bot')
        from_id = obj.get('data', {}).get('user_id')
        logging.debug(f'handle_push(): is_bot: {is_bot}, is_test_bot: {from_id == TEST_BOT_ID}')

        # Ignore self message and allow test message from test_bot.
        if is_bot and (from_id == FANBOOK_BOT_ID or from_id != TEST_BOT_ID):
            return
        channel_id = obj.get('data', {}).get('channel_id')
        author = obj.get('data', {}).get('author', {}).get('nickname')
        if not channel_id or not author:
            return

        logging.info(f'handle_push(): {obj}')
        with sentry_sdk.start_transaction(op="handle_push", name="handle_single_msg"):
            msg = build_from_fanbook_msg(obj)
            asyncio.create_task(self.handle_single_msg(msg))

    def send_msg(self, msg: str, chat_id, parse_mode=None):
        headers = {'Content-type': 'application/json'}
        payload = {'chat_id': int(chat_id), 'text': msg, 'desc': msg}

        send_msg_start = time.perf_counter()
        response = requests.post(FANBOOK_SEND_MSG_URL, data=json.dumps(payload), headers=headers)
        SEND_MSG_LATENCY_METRICS.labels(len(msg) // 10 * 10).observe(time.perf_counter() - send_msg_start)
        logging.debug(f'send_msg(): {response.json()}')
        return response.json()

    async def send_msg_async(self, msg: str, chat_id, parse_mode=None, reply_to_message_id=None):
        headers = {'Content-type': 'application/json'}
        payload = {
            'chat_id': int(chat_id),
            'text': msg,
            'desc': msg,
        }
        if reply_to_message_id:
            payload['reply_to_message_id'] = int(reply_to_message_id)

        async with httpx.AsyncClient() as client:
            send_msg_start = time.perf_counter()
            response = await client.post(FANBOOK_SEND_MSG_URL, data=json.dumps(payload), headers=headers)
            SEND_MSG_LATENCY_METRICS.labels(len(msg) // 10 * 10).observe(time.perf_counter() - send_msg_start)

        logging.info(f'send_msg(): {response.json()}')
        return response.json()

    async def send_img_async(self, chat_id, file_path: str, reply_to_message_id=None, description=''):
        headers = {'Content-type': 'application/json'}
        url = file_path.replace('files/', f'http://{Params().UBUNTU_SERVER_IP_ADDRESS}:81/')
        logging.info(f"local_bot_img_command() prepare to send image {url}")
        payload = {
            'chat_id': int(chat_id),
            'photo': {"Url": url},
        }
        if reply_to_message_id:
            payload['reply_to_message_id'] = int(reply_to_message_id)

        async with httpx.AsyncClient() as client:
            send_img_start = time.perf_counter()
            response = await client.post(FANBOOK_SEND_IMAGE_URL, data=json.dumps(payload), headers=headers)
            SEND_IMAGE_LATENCY_METRICS.observe(time.perf_counter() - send_img_start)

        logging.info(f'send_img(): {response.json()}')
        return response.json()

    async def send_ping(self, ws):
        while True:
            await asyncio.sleep(HEAT_BEAT_INTERVAL)
            await ws.send("{'type':'ping'}")

    async def handle_heart_beat(self, ws):
        asyncio.create_task(self.send_ping(ws))

    async def handle_websocket_connection(self):
        try:
            async with websockets.connect(self.addr) as ws:
                await self.handle_heart_beat(ws)
                while True:
                    try:
                        message = await ws.recv()
                        obj = json.loads(message)
                        if obj.get('action') == 'error':
                            if len(obj.get('data', [])) != 0:
                                logging.error("Received error: %s", message)
                        elif obj.get('action') == 'push':
                            asyncio.create_task(self.handle_push(obj))
                        else:
                            logging.error("Received message: %s", message)
                    except json.JSONDecodeError as e:
                        logging.error("JSONDecodeError: Invalid JSON format in the received message. Error: %s", e)
                    except ConnectionError as e:
                        logging.error('WebSocket connection closed unexpectedly. Error: %s', e)
                        break
        except Exception as e:
            logging.error('Unexpected error in WebSocket connection handling. Error: %s', e)
        finally:
            if not ws.closed:
                await ws.close()
                logging.info('WebSocket connection closed.')

    def run(self):
        logging.debug(f"@{self.bot_name} started...")
        asyncio.get_event_loop().run_until_complete(self.handle_websocket_connection())


if __name__ == '__main__':
    # Start the prometheus_client server at port 8000
    start_http_server(8000)
    # Start sentry monitor
    sentry_sdk.init(
        dsn="https://9201c284873c436dbae2c576b8319f7f@o4505276925214720.ingest.sentry.io/4505276928491520",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )
    FanbookBot(
        bot_name=FANBOOK_BOT_NAME,
        bot_owner_id=FANBOOK_BOT_OWNER_ID,
        bot_creator_id=FANBOOK_BOT_CREATOR_ID,
        bot_owner_name=FANBOOK_BOT_OWNER_NAME,
        # TODO(kezhang@): You should either implement these 4 branch for Fanbook or replace them with NoOpBranch
        document_branch_handler=None,
        photo_branch_handler=None,
        voice_branch_handler=None,
        audio_branch_handler=None,
        improper_branch_handler=NoOpBranch(),
        text_branch_handler=NoOpBranch(),
        payment_branch_handler=NoOpBranch(),
        check_bill_branch_handler=NoOpBranch(),
        bot_owner_branch_handler=NoOpBranch(),
        english_teacher_branch_handler=NoOpBranch(),
        coinmarketcap_branch_handler=NoOpBranch(),
    ).run()
