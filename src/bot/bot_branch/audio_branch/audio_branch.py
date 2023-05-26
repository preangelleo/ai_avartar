from abc import ABC

from src.bot.bot_branch.bot_branch import BotBranch


class AudioBranch(BotBranch, ABC):
    def __init__(self, *args, **kwargs):
        super(AudioBranch, self).__init__(*args, **kwargs)
