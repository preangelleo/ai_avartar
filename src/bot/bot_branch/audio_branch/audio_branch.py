from abc import ABC

from src.bot.bot_branch.bot_branch import BotBranch


class AudioBranch(BotBranch, ABC):
    def __init__(self):
        super(BotBranch, self).__init__()
