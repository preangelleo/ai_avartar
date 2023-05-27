from src.bot.bot import Bot


class WebBot(Bot):
    def __init__(self, *args, **kwargs):
        super(WebBot, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    WebBot().run()
