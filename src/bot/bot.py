import time
from abc import ABC, abstractmethod
from datetime import date

from src.bot.bot_branch.audio_branch.audio_branch import AudioBranch
from src.bot.bot_branch.bot_owner_branch.bot_owner_branch import BotOwnerBranch
from src.bot.bot_branch.coinmarketcap_branch.coinmarketcap_branch import (
    CoinMarketCapBranch,
)
from src.bot.bot_branch.document_branch.document_branch import DocumentBranch
from src.bot.bot_branch.english_teacher_branch.english_teacher_branch import (
    EnglishTeacherBranch,
)
from src.bot.bot_branch.improper_branch.improper_branch import ImproperBranch
from src.bot.bot_branch.payment_branch.crpto.check_bill_branch import (
    CheckBillBranch,
)
from src.bot.bot_branch.payment_branch.crpto.payment_branch import PaymentBranch
from src.bot.bot_branch.photo_branch.photo_branch import PhotoBranch
from src.bot.bot_branch.text_branch.text_branch import TextBranch
from src.bot.bot_branch.voice_branch.voice_branch import VoiceBranch
from src.utils.utils import *
from src.utils.logging_util import logging
from src.utils.utils import user_id_exists, user_over_limit
from src.utils.prompt_template import user_limit_msg, private_limit_msg

import os

import pandas as pd

from src.third_party_api.chatgpt import local_chatgpt_to_reply
from src.utils.metrics import *


class Bot(ABC):
    qa = None
    last_word_checked = 'nice'

    def __init__(
        self,
        bot_name: str,
        bot_owner_name: str,
        bot_owner_id: str,
        bot_creator_id: str,
        document_branch_handler: DocumentBranch,
        photo_branch_handler: PhotoBranch,
        voice_branch_handler: VoiceBranch,
        audio_branch_handler: AudioBranch,
        improper_branch_handler: ImproperBranch,
        text_branch_handler: TextBranch,
        payment_branch_handler: PaymentBranch,
        check_bill_branch_handler: CheckBillBranch,
        bot_owner_branch_handler: BotOwnerBranch,
        english_teacher_branch_handler: EnglishTeacherBranch,
        coinmarketcap_branch_handler: CoinMarketCapBranch,
    ):
        self.bot_name = bot_name
        self.bot_owner_name = bot_owner_name
        self.bot_owner_id = bot_owner_id
        self.bot_creator_id = bot_creator_id
        self.bot_admin_id_list = [bot_owner_id, bot_creator_id]

        self.document_branch_handler = document_branch_handler
        self.photo_branch_handler = photo_branch_handler
        self.voice_branch_handler = voice_branch_handler
        self.audio_branch_handler = audio_branch_handler
        self.improper_branch_handler = improper_branch_handler
        self.text_branch_handler = text_branch_handler
        self.payment_branch_handler = payment_branch_handler
        self.check_bill_branch_handler = check_bill_branch_handler
        self.bot_owner_branch_handler = bot_owner_branch_handler
        self.english_teacher_branch_handler = english_teacher_branch_handler
        self.coinmarketcap_branch_handler = coinmarketcap_branch_handler

    @abstractmethod
    def send_msg(self, msg: str, chat_id, parse_mode=None):
        raise NotImplementedError

    @abstractmethod
    async def send_msg_async(self, msg: str, chat_id, parse_mode=None, reply_to_message_id=None):
        raise NotImplementedError

    @abstractmethod
    def send_audio(self, audio_path, chat_id):
        raise NotImplementedError

    @abstractmethod
    def send_img(self, chat_id, file_path, description=''):
        raise NotImplementedError

    @abstractmethod
    async def send_img_async(self, chat_id, file_path: str, reply_to_message_id=None, description=''):
        raise NotImplementedError

    @abstractmethod
    def send_file(self, chat_id, file_path, description=''):
        raise NotImplementedError

    # 从 avatar_chat_history 读出 Unique 的 from_id 并群发 files/images/avatar_command.png Image 给他们
    def send_img_to_all(self, msg, img_file, description=''):
        if not os.path.isfile(img_file):
            return
        logging.debug(f"send_img_to_all()")
        try:
            df = pd.read_sql_query(
                f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0",
                Params().engine,
            )
        except Exception as e:
            return logging.error(f"send_img_to_all() read_sql_query() failed: \n\n{e}")

        logging.debug(f"totally {df.shape[0]} users to send image")

        # create a list of from_id from df
        from_ids = df['chat_id'].tolist()

        # 向 from_ids 里的所有用户发送 img_file 图片
        try:
            self.send_msg(
                f"{msg.user_nick_name}, 我要开始群发图片了, 一共有 {len(from_ids)} 个用户, 需要一个一个发给他们, 请耐心等待哈 😘",
                self.bot_owner_id,
            )
            for i in range(len(from_ids)):
                from_id = from_ids[i]
                if not from_id:
                    continue
                if from_id == self.bot_owner_id:
                    continue

                logging.debug(f"send_img_to_all() {i}/{len(from_ids)} to: {from_id}")
                try:
                    self.send_img(from_id, img_file, description)
                except Exception as e:
                    logging.error(f"send_img_to_all() bot.send_img() failed: \n\n{e}")
            # 通知 bot owner 发送成功
            self.send_msg(
                f"亲爱的, 我已经把图片发送给所有 {len(from_ids)} 个用户了啦, 使命必达, 欧耶 😎!",
                self.bot_owner_id,
            )
        except Exception as e:
            logging.error(f"send_img_to_all() failed: \n\n{e}")
        return

    # 从 avatar_chat_history 读出 Unique 的 from_id 并群发 msg_text 消息给他们
    def send_msg_to_all(self, msg: SingleMessage, msg_text):
        logging.debug(f"send_msg_to_all()")
        try:
            df = pd.read_sql_query(
                f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0",
                Params().engine,
            )
        except Exception as e:
            return logging.error(f"send_msg_to_all() read_sql_query() failed: \n\n{e}")

        logging.debug(f"totally {df.shape[0]} users to send message")

        try:
            for i in range(df.shape[0]):
                from_id = df.iloc[i]['chat_id']
                if from_id == self.bot_owner_id:
                    continue

                logging.debug(f"send_msg_to_all() {i}/{df.shape[0]} to: {from_id}")
                self.send_msg(msg_text, from_id)
            # 通知 bot owner 发送成功
            self.send_msg(
                f"{msg.user_nick_name}, 我已经把以下消息发送给所有 {df.shape[0] - 1} 个用户了, 消息原文:\n\n{msg_text}",
                self.bot_owner_id,
            )
        except Exception as e:
            logging.error(f"end_msg_to_all() failed: \n\n{e}")
        return

    # 群发文件给数据库中所有的 from_id
    def send_file_to_all(self, msg: SingleMessage, file):
        if not os.path.isfile(file):
            return
        logging.debug(f"send_file_to_all()")
        # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
        try:
            df = pd.read_sql_query(
                f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0",
                Params().engine,
            )
        except Exception as e:
            return logging.error(f"send_file_to_all() read_sql_query() failed: \n\n{e}")

        logging.debug(f"totally {df.shape[0]} users to send file")

        try:
            for i in range(df.shape[0]):
                from_id = df.iloc[i]['chat_id']
                if from_id == self.bot_owner_id:
                    continue

                logging.debug(f"send_file_to_all() {i}/{df.shape[0]} to: {from_id}")
                self.send_file(from_id, file)
            # 通知 bot owner 发送成功
            self.send_msg(
                f"{msg.user_nick_name}, 我已经把 {file} 发送给所有 {df.shape[0] - 1} 个用户了.",
                self.bot_owner_id,
            )
        except Exception as e:
            logging.error(f"send_file_to_all() failed: \n\n{e}")
        return

    # 群发音频给数据库中所有的 from_id
    def send_audio_to_all(self, msg: SingleMessage, audio_file):
        if not os.path.isfile(audio_file):
            return
        logging.debug(f"send_audio_to_all()")
        # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
        try:
            df = pd.read_sql_query(
                f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0",
                Params().engine,
            )
        except Exception as e:
            return logging.error(f"send_audio_to_all() read_sql_query() failed: \n\n{e}")

        logging.debug(f"totally {df.shape[0]} users to send audio")

        try:
            for i in range(df.shape[0]):
                from_id = df.iloc[i]['chat_id']
                if not from_id:
                    continue
                if from_id == self.bot_owner_id:
                    continue

                logging.debug(f"send_audio_to_all() {i}/{df.shape[0]} to: {from_id}")
                try:
                    self.send_audio(audio_file, from_id)
                except Exception as e:
                    logging.error(f"send_audio_to_all() send_audio() failed: \n\n{e}")
            # 通知 bot owner 发送成功
            self.send_msg(
                f"{msg.user_nick_name}, 我已经把 {audio_file.split('/')[-1]} 发送给所有 {df.shape[0] - 1} 个用户了.",
                self.bot_owner_id,
            )
        except Exception as e:
            logging.error(f"send_audio_to_all() failed: \n\n{e}")
        return

    '''定义一个功能, 检查后判断是否要继续为用户服务：通过 给定的 from_id 从 UserPriority 表中查询用户的优先级, 返回一个字典; 如果用户是黑名单用户, 这直接返回 False, 如果用户是 free_until 用户, 则判断此刻有没有过期, 如果没有过期则返回 True, 如果过期了则继续下面的代码; 检查用户最新一次 usdt_paid_in 或者 usdt_paid_in 是 {MONTHLY_FEE} 的 x 倍, 再判断上一次付费到现在是一个月的 y 倍, 如果如果 x > y 则返回 True, 否则返回 False
    '''

    def user_is_legit(self, msg: SingleMessage, from_id):
        if not from_id:
            NON_LEGIT_USER_COUNTER.labels('empty_from_id').inc()
            return False
        user_priority = get_user_priority(from_id)
        logging.info(f"user_is_legit() user_priority: {user_priority}")
        if user_priority:
            # 如果是 is_owner or is_admin or is_vip 则直接返回 True, 黑名单对三者没有意义
            if user_priority.get('is_owner') or user_priority.get('is_admin') or user_priority.get('is_vip'):
                return True

            # 付费用户在到期前都是可以继续使用的, 到期后可以在每月免费聊天次数内继续使用, 超过免费聊天次数后则不再提供服务, 有效期内黑名单对付费用户无意义
            if user_priority.get('is_paid'):
                next_payment_time = user_priority.get('next_payment_time', None)
                if next_payment_time and next_payment_time > datetime.now():
                    return True
                else:
                    if mark_user_is_not_paid(from_id):
                        self.send_msg(Params().refill_teaser, from_id)
                    return self.check_this_month_total_conversation(
                        msg.user_nick_name,
                        from_id,
                        offset=Params().free_user_free_talk_per_month,
                    )

            # 非 owner, admin, vip, 有效期内的 paid 用户, 如果是黑名单用户则直接返回 False
            if user_priority.get('is_blacklist'):
                NON_LEGIT_USER_COUNTER.labels('blacklist').inc()
                return False

        return self.check_this_month_total_conversation(msg.user_nick_name, from_id)

    def check_this_month_total_conversation(self, user_nick_name, from_id, offset=0):
        try:
            with Params().Session() as session:
                # Get the current month
                today = date.today()
                current_month = today.strftime('%Y-%m')
                # Get the count of rows for the given from_id in the current month
                count_query = sqlalchemy.text(
                    f"SELECT COUNT(*) FROM avatar_chat_history WHERE from_id = '{from_id}' AND DATE_FORMAT(update_time, '%Y-%m') = '{current_month}'"
                )
                row_count = session.execute(count_query).scalar()
                logging.debug(f"from_id {from_id} 本月({current_month}) 已与 @{self.bot_name} 交流: {row_count} 次...")
                logging.debug("聊天次数: %s", (row_count - offset))
                logging.debug("上限: %s", (Params().free_user_free_talk_per_month))
                # Check if the row count exceeds the threshold
                if (row_count - offset) > Params().free_user_free_talk_per_month:
                    logging.info(f'{from_id} exceed_free_talk_num')
                    self.send_msg(
                        f"{user_nick_name}, 你这个月跟我聊天的次数太多了, 我看了一下, 已经超过 {Params().free_user_free_talk_per_month}条/月 的聊天记录上限, 你可真能聊, 哈哈哈, 下个月再跟我聊吧。",
                        from_id,
                    )
                    NON_LEGIT_USER_COUNTER.labels('exceed_free_talk_num').inc()
                    return False
                else:
                    return True
        except Exception as e:
            logging.error(f"check_this_month_total_conversation() 2 read_sql_query() failed:\n\n{e}")
            return False

    async def handle_single_msg(self, msg: SingleMessage):
        """
        Handle a single message of class SingleMessage.
        """

        # 如果是群聊但是没有 at 机器人, 则在此处返回
        if msg.should_be_ignored:
            IGNORED_MSG_COUNTER.inc()
            logging.info("should ignore this msg", msg.raw_msg)
            return

        if msg.is_private:
            PRIVATE_MSG_COUNTER.inc()
            # TODO: Remove this after support private chat
            await self.send_msg_async(
                msg=private_limit_msg,
                chat_id=msg.chat_id,
                parse_mode=None,
                reply_to_message_id=msg.reply_to_message_id,
            )
            return

        # 通过 from_id 判断用户的状态, 免费还是付费, 是不是黑名单用户, 是不是过期用户, 是不是 owner, admin, vip
        if not self.user_is_legit(msg, msg.from_id):
            return

        if not msg.msg_text or len(msg.msg_text) == 0:
            return

        if not user_id_exists(user_id=msg.from_id) and user_over_limit():
            await self.send_msg_async(
                msg=user_limit_msg,
                chat_id=msg.chat_id,
                parse_mode=None,
                reply_to_message_id=msg.reply_to_message_id,
            )
            return

        handle_single_msg_start = time.perf_counter()
        if msg.from_id in self.bot_admin_id_list:
            HANDLE_SINGLE_MSG_COUNTER.labels('owner').inc()
            MSG_TEXT_LEN_METRICS.labels('owner').observe(len(msg.msg_text))
            if self.bot_owner_branch_handler.handle_single_msg(msg, self):
                SUCCESS_REPLY_COUNTER.labels('owner').inc()
                HANDLE_SINGLE_MSG_LATENCY_METRICS.labels(len(msg.msg_text) // 10 * 10, 'owner').observe(
                    time.perf_counter() - handle_single_msg_start
                )

        # TODO: migrate following code to text_branch_handler
        try:
            save_avatar_chat_history(
                msg,
                msg.msg_text,
                msg.chat_id,
                msg.from_id,
                msg.username,
                msg.first_name,
                msg.last_name,
            )
        except Exception as e:
            return logging.error(f"save_avatar_chat_history() failed: {e}")

        HANDLE_SINGLE_MSG_COUNTER.labels('chatgpt').inc()
        MSG_TEXT_LEN_METRICS.labels('chatgpt').observe(len(msg.msg_text))

        # Call chatgpt and get response
        response = await local_chatgpt_to_reply(self, msg)
        text_reply = None
        branch = 'local_chatgpt'

        if response:
            send_text_reply = True
            # If a function call is triggered
            if response['choices'][0]['message'].get("function_call"):
                branch = 'generate_image'
                function_name = response['choices'][0]['message']["function_call"]["name"]
                if function_name == 'generate_image':
                    function_args = json.loads(response['choices'][0]['message']["function_call"]["arguments"])
                    image_description = function_args['image_description']
                    text_reply = function_args['response_to_user_message']
                    logging.info(
                        f"generate_image:\n"
                        f"image_description:{image_description}\n"
                        f"response_to_user_message:{text_reply}"
                    )
                    file_list = None
                    try:
                        file_list = stability_generate_image(text_prompts=image_description)
                    except Exception as e:
                        send_text_reply = False
                        ERROR_COUNTER.labels('stability_generate_image', 'chatgpt').inc()
                        logging.error(f"stability_generate_image() {e}")

                    if send_text_reply and file_list:
                        for file in file_list:
                            try:
                                await self.send_img_async(
                                    chat_id=msg.chat_id,
                                    file_path=file,
                                    reply_to_message_id=msg.reply_to_message_id,
                                    description=image_description,
                                )
                            except Exception as e:
                                send_text_reply = False
                                ERROR_COUNTER.labels('error_send_img', 'chatgpt').inc()
                                logging.error(f"local_bot_img_command() send_img({file}) FAILED:  {e}")

            # If no function call is triggered, and it is a regular reply
            else:
                text_reply = response['choices'][0]['message']['content']
                if text_reply:
                    if '[JAILBREAK]' in text_reply:
                        text_reply = text_reply.split('[JAILBREAK]')[-1].strip()
                        if '[CLASSIC]' in text_reply:
                            text_reply = text_reply.split('[CLASSIC]')[0].strip()
                    if '[CLASSIC]' in text_reply:
                        text_reply = text_reply.split('[CLASSIC]')[-1].strip()

                    text_reply = text_reply.strip('\n').strip()

            # If there is any text_reply available we should store and send it
            if text_reply and send_text_reply:
                store_reply = text_reply.replace("'", "").replace('"', '')
                if branch == 'generate_image':
                    store_reply = image_description + store_reply
                try:
                    with Params().Session() as session:
                        new_record = ChatHistory(
                            first_name='ChatGPT',
                            last_name='Bot',
                            username=self.bot_name,
                            from_id=msg.from_id,
                            chat_id=msg.chat_id,
                            update_time=datetime.now(),
                            msg_text=store_reply,
                            black_list=0,
                            is_private=msg.is_private,
                        )
                        # Add the new record to the session
                        session.add(new_record)

                        # Also mark this message as is_replied and update branch
                        session.query(ChatHistory).filter(ChatHistory.message_id == msg.message_id).update(
                            {"is_replied": True, "branch": branch}
                        )
                        # Commit the session
                        session.commit()
                except Exception as e:
                    ERROR_COUNTER.labels('error_save_avatar_chat_history', 'chatgpt').inc()
                    return logging.error(f"local_chatgpt_to_reply() save to avatar_chat_history failed: {e}")

                try:
                    REPLY_TEXT_LEN_METRICS.labels('chatgpt').observe(len(text_reply))
                    await self.send_msg_async(
                        msg=text_reply,
                        chat_id=msg.chat_id,
                        parse_mode=None,
                        reply_to_message_id=msg.reply_to_message_id,
                    )
                    SUCCESS_REPLY_COUNTER.labels('chatgpt').inc()
                    HANDLE_SINGLE_MSG_LATENCY_METRICS.labels(len(msg.msg_text) // 10 * 10, 'chatgpt').observe(
                        time.perf_counter() - handle_single_msg_start
                    )
                except Exception as e:
                    ERROR_COUNTER.labels('error_send_msg', 'chatgpt').inc()
                    logging.error(f"local_chatgpt_to_reply() send_msg() failed : {e}")

        return

    @abstractmethod
    def run(self):
        raise NotImplementedError
