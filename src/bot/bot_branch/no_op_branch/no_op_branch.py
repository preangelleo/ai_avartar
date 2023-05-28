from src.bot.bot_branch.bot_branch import BotBranch
from src.utils.logging_util import logging


class NoOpBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(NoOpBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        logging.info("entering NoOpBranch.handle_single_msg()")
        pass
