from abc import ABC, abstractmethod
from src.bot.single_message import SingleMessage
from src.bot.bot import Bot


class BotBranch(ABC):
    @abstractmethod
    def handle_single_msg(self, msg, bot):
        """
        Handle a single msg for a given branch

        :type msg: SingleMessage
        :type bot: Bot
        """
        raise NotImplementedError
