from abc import ABC, abstractmethod
from src.bot.single_message import SingleMessage


class BotBranch(ABC):
    @abstractmethod
    def handle_single_msg(self, msg: SingleMessage, bot):
        raise NotImplementedError
