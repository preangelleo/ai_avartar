from src.bot.bot_branch.payment_branch.crpto.utils import update_user_next_payment_date, markdown_tokentnxs, \
    generate_eth_address
from src.bot.bot_branch.bot_branch import BotBranch
from src.utils.utils import *


class CheckBillBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(CheckBillBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        # 从数据库中读出该 from_id 对应的收款 eth address
        try:
            next_payment_time_dict = update_user_next_payment_date(bot, msg.from_id, msg.user_title)
            if next_payment_time_dict:
                next_payment_time = next_payment_time_dict.get('next_payment_time', None)
                next_payment_time = next_payment_time.strftime("%Y-%m-%d %H:%M:%S")
                bot.send_msg(
                    f"{msg.user_nick_name}, 你下一次交公粮的时间应该是 {next_payment_time}, 你就是我最爱的人 💋💋💋 ...",
                    msg.chat_id)
            else:
                address = generate_eth_address(user_from_id=msg.from_id)
                bot.send_msg(
                    f"还没收到你的公粮呢, 是不是没按要求回复 Transaction Hash 给我啊 😥, 那可能很长时间我都无法给你确认。如果你不知道 Transaction Hash 是什么, 就点击你的充值地址链接 \n{markdown_tokentnxs(address)}\n然后在打开的第一个网页中间找到你打给我的这笔交易记录😆, 点开之后在新页面上半部分找到 Transaction Hash 右边的那个 0x 开头的一长串字符, 拷贝下来发给我就好啦 😘。\n\n如果实在不会搞, 你就要主动联系 @{bot.bot_owner_name} 帮你人工确认了 😦, 到时候你要把你的充值地址:\n\n{address}\n\n和你的 User ID: {msg.from_id}\n\n一起转发给他就好了。 🤩",
                    msg.chat_id, parse_mode='Markdown')
                bot.send_img(msg.chat_id, 'files/images/wallet_address_tokentxns.png',
                             description='第一张图, 这里能看到你的充值地址下的所有交易 😁',
                             )
                bot.send_img(msg.chat_id, 'files/images/wallet_address_transaction_hash.png',
                             description='第二张图, 这里可以找到我要的 Transaction_Hash 😁',
                             )
        except Exception as e:
            return logging.error(f"local_bot_msg_command() generate_eth_address() FAILED: \n\n{e}")
        return
