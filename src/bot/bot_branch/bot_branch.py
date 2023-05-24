from abc import ABC, abstractmethod


class BotBranch(ABC):
    @abstractmethod
    def handle_single_msg(self, msg):
        raise NotImplementedError
