from abc import ABC

from src.bot.bot_branch.bot_branch import BotBranch


class PhotoBranch(BotBranch, ABC):
    def __init__(self, *args, **kwargs):
        super(PhotoBranch, self).__init__(*args, **kwargs)
