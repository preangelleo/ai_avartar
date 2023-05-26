import random

from src.bot.bot_branch.bot_branch import BotBranch
from utils.prompt_template import emoji_list_for_unhappy
from src.utils.utils import *


class ImproperBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(ImproperBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        # 从 emoji_list_for_unhappy 随机选出一个 emoji 回复
        reply = random.choice(emoji_list_for_unhappy)
        bot.send_msg(reply, msg.chat_id)
        if set_user_blacklist(msg.from_id):
            blacklisted_alert = f"User: {msg.user_title}\nFrom_id: {msg.from_id}\n已被拉黑, 因为他发了: \n\n{msg.msg_text}\n\n如需解除黑名单, 请回复:\nremove_from_blacklist {msg.from_id}"
            bot.send_msg(blacklisted_alert, bot.bot_owner_id)
            return logging.info(f"BLACKLISTED: {blacklisted_alert}")
