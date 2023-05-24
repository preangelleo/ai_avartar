from abc import ABC, abstractmethod


class Bot(ABC):
    @abstractmethod
    def handle_single_msg(self, msg):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
