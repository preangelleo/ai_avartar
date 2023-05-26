from dotenv import load_dotenv
import os


class Params:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        self.OPENAI_TOKEN = os.getenv('OPENAI_KEY')
        self.FAN_BOOK_BOT_TOKEN = os.getenv('FAN_BOOK_BOT_TOKEN')
