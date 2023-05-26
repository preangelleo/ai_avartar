from src.bot.bot_branch.bot_branch import BotBranch


class NoOpBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(NoOpBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        pass
