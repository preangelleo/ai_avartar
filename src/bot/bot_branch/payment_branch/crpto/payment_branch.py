from src.bot.bot_branch.bot_branch import BotBranch
from src.bot.bot_branch.payment_branch.crpto.utils import (
    generate_eth_address,
    generate_eth_address_qrcode,
)
from src.utils.logging_util import logging


class PaymentBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(PaymentBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        # 从数据库中读出该 from_id 对应的收款 eth address
        try:
            address = generate_eth_address(user_from_id=msg.from_id)
            bot.send_msg(
                f"{msg.user_nick_name}你真好, 要来交公粮咯, 真是爱死你了 😍😍😍。这是收粮地址: \n\n{address}\n\n只能交 ERC20 的 USDT/USDC 哦, 别的我不认识。交后直接回复 0x 开头的 66 位 Transaction_Hash, 像下面这样的:\n\n0xd119eaf8c4e8abf89dae770e11b962f8034c0b10ba2c5f6164bd7b780695c564\n\n这样我自己就能查收, 而且查起来比较快, 到账后我会通知你哒 🙂\n\nP.S. 这个地址是专门为你生成的,所有转账到这个地址的 USDC/USDT 都将会视为是你交的公粮。\n\n如果你不回复 Transaction_Hash, 那可能很长时间我都无法给你确认哦。回复后如果五分钟内没有收到确认, 可以点击 \n/check_payment \n提醒我再查看一下哈 😎",
                msg.chat_id,
            )
        except Exception as e:
            return logging.error(
                f"local_bot_msg_command() generate_eth_address() FAILED: \n\n{e}"
            )

        try:
            qrcode_file_path = generate_eth_address_qrcode(eth_address=address)
            if qrcode_file_path:
                bot.send_img(msg.chat_id, qrcode_file_path)
        except Exception as e:
            logging.error(
                f"local_bot_msg_command() generate_eth_address_qrcode() FAILED: \n\n{e}"
            )
        return
