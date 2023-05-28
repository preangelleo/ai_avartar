import threading
import time

from src.bot.bot_branch.audio_branch.telegram_audio_branch import TelegramAudioBranch
from src.bot.bot_branch.bot_owner_branch.bot_owner_branch import BotOwnerBranch
from src.bot.bot_branch.coinmarketcap_branch.coinmarketcap_branch import CoinMarketCapBranch
from src.bot.bot_branch.document_branch.telegram_document_branch import TelegramDocumentBranch
from src.bot.bot_branch.english_teacher_branch.english_teacher_branch import EnglishTeacherBranch
from src.bot.bot_branch.improper_branch.improper_branch import ImproperBranch
from src.bot.bot_branch.payment_branch.crpto.check_bill_branch import CheckBillBranch
from src.bot.bot_branch.payment_branch.crpto.payment_branch import PaymentBranch
from src.bot.bot_branch.photo_branch.telegram_photo_branch import TelegramPhotoBranch
from src.bot.bot_branch.text_branch.text_branch import TextBranch
from src.bot.bot_branch.voice_branch.telegram_voice_branch import TelegramVoiceBranch
from src.bot.single_message import build_from_telegram_msg
from src.bot.telegram.utils.utils import *
from src.bot.bot import Bot
from src.utils.logging_util import logging
from src.utils.param_singleton import Params


# Define a thread class for processing a single message
class MessageThread(threading.Thread):
    avatar_uid_lock = threading.Lock()
    avatar_UID = -2

    def __init__(self, bot, tg_msg):
        threading.Thread.__init__(self)
        self.bot = bot
        self.tg_msg = tg_msg

    def run(self):
        self.bot.handle_single_msg(build_from_telegram_msg(tg_msg=self.tg_msg))


class TelegramBot(Bot):

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__(*args, **kwargs)

    def send_msg(self, msg: str, chat_id, parse_mode=None):
        if not msg:
            return False
        if not chat_id:
            logging.error(f"Missing chat_id: msg_object={msg}, chat_id={chat_id}, parse_mode={parse_mode}")
            return

        url = get_send_msg_url()
        payload = {
            "text": msg,
            "parse_mode": parse_mode or '',
            "disable_web_page_preview": True,
            "disable_notification": True,
            "reply_to_message_id": None,
            "chat_id": chat_id
        }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            requests.post(url, json=payload, headers=headers)
        except Exception as e:
            return print(f"ERROR: send_msg() failed for:\n{e}\n\nOriginal message:\n{msg}")
        logging.debug(f"send_msg(): {msg}")
        return True

    def send_audio(self, audio_path, chat_id):
        if not audio_path or not chat_id: return
        print(f"DEBUG: send_audio()")

        url = get_send_audio_url()
        # send the audio message to the user
        try:
            with open(audio_path, 'rb') as audio_file:
                requests.post(url, data={'chat_id': chat_id}, files={'audio': audio_file})
        except Exception as e:
            print(f"ERROR : send_audio() failed : {e}")
        return

    def send_img(self, chat_id, file_path, description=''):
        if not file_path or not chat_id: return
        try:
            files = {'photo': open(file_path, 'rb')}
        except Exception as e:
            return print(f"ERROR: send_img() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
        url = get_send_img_url(chat_id, description)
        r = ''
        try:
            r = requests.post(url, files=files)
        except Exception as e:
            print(f"ERROR : send_img() failed : \n{e}")
        return r

    def send_file(self, chat_id, file_path, description=''):
        if not file_path or not chat_id: return
        try:
            files = {'document': open(file_path, 'rb')}
        except Exception as e:
            return print(f"ERROR: send_file() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
        url = get_send_file_url(chat_id, description)
        r = ''
        try:
            r = requests.post(url, files=files)
        except Exception as e:
            print(f"ERROR : send_file() failed : \n{e}")
        return r

    # Telegram bot iterate new update messages
    def check_local_bot_updates(self):
        r = local_bot_getUpdates(MessageThread.avatar_UID + 1)
        if not r or r.status_code != 200: return
        updates = r.json().get('result', [])
        if not updates: return

        if MessageThread.avatar_UID != updates[0]['update_id']:
            with MessageThread.avatar_uid_lock:
                MessageThread.avatar_UID = updates[0]['update_id']
        else:
            return

        for tg_msg in updates:
            # Create a separate thread for processing each message
            message_thread = MessageThread(self, tg_msg)
            message_thread.start()

    def run(self):
        logging.debug(f"@{self.bot_name} started...")
        i = 0
        while True:
            i += 1
            # Create an instance of the update thread
            update_thread = threading.Thread(target=self.check_local_bot_updates)
            # Start the update thread
            update_thread.start()
            time.sleep(1)


if __name__ == '__main__':
    TelegramBot(
        bot_name=Params().TELEGRAM_BOT_NAME,
        bot_owner_name=Params().TELEGRAM_BOTOWNER_NAME,
        bot_owner_id=Params().TELEGRAM_BOTOWNER_CHAT_ID,
        bot_creator_id=Params().TELEGRAM_BOTCREATER_CHAT_ID,
        document_branch_handler=TelegramDocumentBranch(),
        photo_branch_handler=TelegramPhotoBranch(),
        voice_branch_handler=TelegramVoiceBranch(),
        audio_branch_handler=TelegramAudioBranch(),
        improper_branch_handler=ImproperBranch(),
        text_branch_handler=TextBranch(),
        payment_branch_handler=PaymentBranch(),
        check_bill_branch_handler=CheckBillBranch(),
        bot_owner_branch_handler=BotOwnerBranch(),
        english_teacher_branch_handler=EnglishTeacherBranch(),
        coinmarketcap_branch_handler=CoinMarketCapBranch(),
    ).run()
