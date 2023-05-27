from src.bot.bot import Bot


class WechatBot(Bot):
    def __init__(self, *args, **kwargs):
        super(WechatBot, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    WechatBot().run()
