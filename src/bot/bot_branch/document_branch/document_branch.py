from abc import ABC

from src.bot.bot_branch.bot_branch import BotBranch


class DocumentBranch(BotBranch, ABC):
    def __init__(self, *args, **kwargs):
        super(DocumentBranch, self).__init__(*args, **kwargs)
