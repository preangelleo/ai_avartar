from abc import ABC

from src.bot.bot_branch.bot_branch import BotBranch


class VoiceBranch(BotBranch, ABC):
    def __init__(self, *args, **kwargs):
        super(VoiceBranch, self).__init__(*args, **kwargs)
