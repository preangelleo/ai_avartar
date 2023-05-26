from src.bot.bot_branch.bot_branch import BotBranch
from src.utils.constants import DEAR_USER
from src.utils.utils import *


class BotOwnerBranch(BotBranch):
    def __init__(self):
        pass

    def handle_single_msg(self, msg, bot):
        msg_lower = msg.msg_text.lower()
        MSG_SPLIT = msg_lower.split()
        MSG_LEN = len(MSG_SPLIT)

        if MSG_SPLIT[0] in ['mybots'] or msg.msg_text in ['/mybots']:
            bot.send_msg(
                f"{msg.user_nick_name}, 你好可爱啊 🤨, /mybots 这个指令是 @BotFather 的, 发给我没用哈, 请点击 @BotFather 过去设置我的参数吧! 😘",
                msg.chat_id)
            return

        elif MSG_SPLIT[0][1:].isdigit():
            try:
                # 如果消息以@开头则@后面的内容是 from_id
                msg.from_id = MSG_SPLIT[0].replace('@', '').replace('/', '')
                if msg.from_id in get_unique_from_id_list():
                    # 如果消息以 @ or / 开头则 @ or / 后面的内容是 from_id, 如果后面还有内容, 则是要发给 from_id 的消息
                    if MSG_LEN > 1:
                        bot.send_msg(' '.join(MSG_SPLIT[1:]), msg.from_id)
                    # 如果后面没有内容, 则是要查询 from_id 的聊天历史记录，保存为 txt 文档并发给 BOT OWNER
                    else:
                        file_path = get_user_chat_history(msg.from_id)
                        if os.path.isfile(file_path): bot.send_file(msg.chat_id, file_path,
                                                                    description=f"Bot 和 {msg.from_id} 之间的的聊天记录")
                else:
                    bot.send_msg(f"{msg.user_nick_name}, msg.from_id {msg.from_id} 没有聊天记录, 😘", msg.chat_id)
            except Exception as e:
                logging.error(f"local_bot_msg_command() get_user_chat_history() FAILED: \n\n{e}")
            return

        # 用 vip 命令设置用户成为 VIP, 当 msg_lower 以 /vip, vip, /vip_, vip_, /v, v, /v_, v_ 开头时, 会触发这个命令, 而 msg_lower 中的数字部分是 from_id
        elif msg_lower.startswith('/vip') or msg_lower.startswith('vip') or msg_lower.startswith(
                '/v') or msg_lower.startswith('v'):
            user_from_id = msg.msg_text.replace('/', '').replace('vip', '').replace('v', '').replace('_',
                                                                                                         '').strip()
            # 判断 from_id 是否是数字
            if user_from_id and user_from_id.isdigit():
                # return bot.send_msg(f"{user_nick_name}, 你要设置谁为 VIP, 请在命令后面的空格后再加上一个 from_id, 比如: \n\nvip 123456789\n\n这样就是把 from_id 为 123456789 的用户设置为 VIP 了😘。如果你不知道对方的 chat_id, 请对方发送 /vip 或者 /v 给我申请成为 VIP, 我会转达他的申请给你并附带对方的 chat_id, 届时如果你同意, 可以根据提示确认。\n\nP.S. /vip 也可以缩写为 /v", chat_id)
                # 判断 from_id 是否在数据库中
                if msg.from_id in get_unique_from_id_list():
                    r = set_user_as_vip(user_from_id)
                    if r:
                        # 通知 user_from_id 他已经被设置为 VIP
                        bot.send_msg(f"{msg.user_nick_name}, 我已经把你设置为 VIP 了, 你可以跟我永久免费聊天了. 😘",
                                     user_from_id)
                        return bot.send_msg(
                            f"msg.from_id: {user_from_id} 已被成功设置为 VIP, 可以享受永久免费聊天了。如果需要改变他的 VIP 状态, 随时可以回复或点击: \n\n/remove_vip_{user_from_id}",
                            msg.chat_id)

        # Remove user from VIP list
        elif msg_lower.startswith('/remove_vip') or msg_lower.startswith('remove_vip'):
            user_from_id = msg.msg_text.replace('/', '').replace('remove_vip', '').replace('_', '').strip()

            if user_from_id and user_from_id.isdigit():
                r = remove_user_from_vip_list(user_from_id)
                if r:
                    return bot.send_msg(f"msg.from_id: {user_from_id} 已被成功移出 VIP 列表!", msg.chat_id)
                else:
                    return bot.send_msg(f"msg.from_id: {user_from_id} 本来就不在 VIP 列表中哈。", msg.chat_id)

            vip_list_with_hint_text = get_vip_list_except_owner_and_admin()

            if vip_list_with_hint_text:
                text_format = '\n'.join(vip_list_with_hint_text)
                vip_count = len(vip_list_with_hint_text)
                if vip_count < 11:
                    return bot.send_msg(
                        f"您一共有 {vip_count} 位 VIP 用户:\n\n{text_format}\n\n点击上面的 /remove_vip_xxxxxxxx 即可将相应的用户从 VIP 列表中移除 😘",
                        msg.chat_id)
                else:
                    # 将 text_format 保存为 txt 文件并发送给 chat_id
                    SAVE_FOLDER = 'files/vip_list'
                    # 检查 SAVE_FOLDER 是否存在, 不存在则创建
                    if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)
                    file_name = f"{SAVE_FOLDER}/vip_list.txt"
                    execution_help_info = f"您一共有 {vip_count} 位 VIP 用户, 拷贝用户名下面的 /remove_vip_xxxxxxxx 指令然后发给我即可将相应的用户从 VIP 列表中移除"
                    with open(file_name, 'w') as f:
                        f.write(f"{execution_help_info}\n\n{text_format}")
                    bot.send_file(msg.chat_id, file_name, description=f"您的 {vip_count} 位 VIP 用户列表")

            return

        # 发送最新的 user_commands 给用户
        elif MSG_SPLIT[0] in ['group_send_commands_list', 'gscl', '/group_send_commands_list', '/gscl']:
            group_send_message_info = f"{DEAR_USER}, /commands 列表更新咯 😙: \n{user_commands}"
            bot.send_msg_to_all(msg, group_send_message_info, bot_owner_chat_id = msg.chat_id)
            bot.send_msg(bot_owner_commands, msg.chat_id)
            return

        elif MSG_SPLIT[0] in ['blacklist', 'bl', '/blacklist', '/bl']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要把谁加入黑名单, 请在命令后面的空格后再加上一个 msg.from_id, 比如: \n\nblacklist 123456789\n\n这样就是把 msg.from_id 为 123456789 的用户加入黑名单了. 😘 \n\nP.S. /blacklist 也可以缩写为 /bl",
                msg.chat_id)

            msg.from_id_to_blacklist = MSG_SPLIT[1]
            try:
                r = set_user_blacklist(msg.from_id_to_blacklist)
                if r:
                    bot.send_msg(
                        f"{msg.user_nick_name}, 我已经把你拉黑了, 如果你想解除黑名单, 请转发本消息给 @@{Params().TELEGRAM_USERNAME}\n\n申请解除黑名单: \n\nremove_from_blacklist {msg.from_id_to_blacklist}",
                        msg.from_id_to_blacklist)
                    bot.send_msg(f"msg.from_id: {msg.from_id_to_blacklist} 已被成功加入黑名单并已经发消息告知.",
                                 msg.chat_id)
            except Exception as e:
                logging.error(f"local_bot_msg_command() set_user_blacklist() FAILED: \n\n{e}")
            return

        elif MSG_SPLIT[0] in ['remove_from_blacklist', 'rbl', '/remove_from_blacklist', '/rbl']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要解除黑名单, 请在命令后面的空格后再加上一个 msg.from_id, 比如: \n\nremove_from_blacklist 123456789\n\n这样就是把 msg.from_id 为 123456789 的用户从黑名单中移除了. 😘 \n\nP.S. /remove_from_blacklist 也可以缩写为 /rbl",
                msg.chat_id)

            msg.from_id_to_remove = MSG_SPLIT[1]
            try:
                r = remove_user_blacklist(msg.from_id_to_remove)
                if r:
                    bot.send_msg(f"{msg.user_nick_name}, 我已经把你从黑名单中移除了, 你可以继续跟我聊天了. 😘",
                                 msg.from_id_to_remove)
                    bot.send_msg(f"msg.from_id: {msg.from_id_to_remove} 已被成功移出黑名单!", msg.chat_id)
            except Exception as e:
                logging.error(f"local_bot_msg_command() remove_user_blacklist() FAILED: \n\n{e}")
            return

        elif MSG_SPLIT[0] in ['set_free_talk_limit', 'sftl', '/set_free_talk_limit', '/sftl']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要设置免费用户每月的免费对话次数, 请在命令后面的空格后再加上一个整数, 比如: \n\nset_free_talk_limit 10\n\n这样就是设置免费用户每月的免费对话次数为 10 次了. 😘 \n\nP.S. /set_free_talk_limit 也可以缩写为 /sftl\n\n重要: 如果 BOT OWNER 把 free_talk_limit 设置为 1, 则意味着该服务只限 VIP、Owner 以及 Paid 用户使用, Free 用户不可用。如果需要邀请朋友成为 VIP, 那么 free_talk_limit 至少应该是 2, 这样新用户才能点击 /start 并发送 /vip 两个指令完成申请。如果 free_talk_limit 设置为 0, 那么除了已有的 VIP 和 Bot Owner 以及 Paid user 之外, 未来任何人都无法和 Bot 做任何交互。如果希望连付费用户都拒之门外, 那么请用 /set_monthly_fee 指令将月费设置为一个巨大的数字。Bot 刚启动的时候, 默认只有一个 Onwer 身份, 没有默认的 VIP, 所有的 VIP 都是 Owner 自己手动添加获批准的。",
                msg.chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数
            try:
                free_talk_limit = int(MSG_SPLIT[1])
            except:
                return bot.send_msg(f"{msg.user_nick_name}, 你输入的 {MSG_SPLIT[1]} 不是整数, 请重新输入哈.",
                                    msg.chat_id)

            # free_talk_limit = 3 if not free_talk_limit or free_talk_limit < 3 else free_talk_limit
            # free_talk_limit 不能是 0，否则目标 VIP 用户无法 /start 并发送 /vip 给 BOT 申请成为 VIP

            Params().update_free_user_free_talk_per_month(free_talk_limit)

            try:
                update_owner_parameter('MAX_CONVERSATION_PER_MONTH', MSG_SPLIT[1])
            except Exception as e:
                return logging.error(f"local_bot_msg_command() update_owner_parameter() FAILED: \n\n{e}")

            return bot.send_msg(
                f"{msg.user_nick_name}, 我已经把免费用户每月的免费对话次数设置为 {MSG_SPLIT[1]} 次了, 系统参数表也更新了, 请放心, 参数立刻生效 😘",
                msg.chat_id)

        elif MSG_SPLIT[0] in ['set_monthly_fee', 'smf', '/set_monthly_fee', '/smf']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要设置每月的收费金额, 请在命令后面的空格后再加上一个整数, 比如: \n\nset_monthly_fee 10\n\n这样就是设置每月的收费金额为 10 美元了. 😘 \n\nP.S. /set_monthly_fee 也可以缩写为 /smf\n\n重要: 如果 BOT OWNER 不希望任何付费用户来使用你的 Bot, 仅限 Owner 以及定向邀请或批准的 VIP 用户 (白名单), 那么请将月费金额设置成天文数字, 并用 /set_free_talk_limit 指令将每月每个用户的免费聊天次数设置为 0 ",
                msg.chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数
            try:
                int(MSG_SPLIT[1])
            except:
                return bot.send_msg(f"{msg.user_nick_name}, 你输入的 {MSG_SPLIT[1]} 不是整数, 请重新输入哈.",
                                    msg.chat_id)

            try:
                update_owner_parameter('MONTHLY_FEE', MSG_SPLIT[1])
            except Exception as e:
                return logging.error(f"local_bot_msg_command() update_owner_parameter() FAILED: \n\n{e}")

            return bot.send_msg(
                f"{msg.user_nick_name}, 我已经把每月的收费金额设置为 {MSG_SPLIT[1]} 美元了, 系统参数表也更新了, 但是需要后台重启服务才能生效, 请联系 @laogege6 帮你重启吧 😘",
                msg.chat_id)

        elif MSG_SPLIT[0] in ['set_refill_teaser', 'srt', '/set_refill_teaser', '/srt']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要设置用户充值提醒的内容, 请在命令后面的空格后再加上你希望使用的充值引导内容, 比如: \n\nset_refill_teaser 亲爱的, 你的免费对话次数已经用完了, 请充值后继续使用哦. 😘\n\n这样就是设置好了。\n\nP.S. /set_refill_teaser 也可以缩写为 /srt , 如果你想查看当正在使用的充值引导内容, 请点击 /check_refill_teaser 或者 /crt",
                msg.chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数

            Params().update_refill_teaser(MSG_SPLIT[1:])

            try:
                update_owner_parameter('REFILL_TEASER', Params().refill_teaser)
            except Exception as e:
                bot.send_msg(
                    f"REFILL_TEASER 设置失败, 请转发本消息给 {Params().BOTCREATER_TELEGRAM_HANDLE} 请他检查一下原因。\n\n{e}",
                    msg.chat_id)

            return bot.send_msg(
                f"{msg.user_nick_name}, 设置好啦, 以后提醒用户充值的时候, 我会用以下内容:\n\n{Params().refill_teaser}\n\n提醒: 任何时候你都可以点击 \n/check_refill_teaser\n或发送 check_refill_teaser \n来查看当前的充值提醒内容。",
                msg.chat_id)

        elif MSG_SPLIT[0] in ['check_refill_teaser', 'crt', '/check_refill_teaser', '/crt']:
            return bot.send_msg(
                f"{msg.user_nick_name}, 以下是当前正在使用的的提醒用户充值的 REFILL_TEASER:\n\n{Params().refill_teaser}",
                msg.chat_id)

        elif MSG_SPLIT[0] in ['group_send_image', 'gsi', '/group_send_image', '/gsi']:
            bot.send_msg(
                f"{msg.user_nick_name}, 你要群发图片, 请直接将图片拖拽给我或者发给我, 但是切记发送前一定要在图片 caption 里填写 /group_send_image 或者简写 /gsi , 这样我才知道这张图片是要求我依次轮询发给所有用户的。",
                msg.chat_id)
            bot.send_img(msg.chat_id, 'files/images/group_send_image_pc.png', description='电脑上是这样色儿的 😚',
                         )
            bot.send_img(msg.chat_id, 'files/images/group_send_image_phone.PNG', description='手机上是这样色儿的 😉',
                         )
            return

        elif MSG_SPLIT[0] in ['group_send_message', 'gsm', '/gsm', '/group_send_message']:
            if MSG_LEN == 1: return bot.send_msg(
                f"{msg.user_nick_name}, 你要群发消息, 请在命令后面的空格后再加上一个字符串, 比如: \n\ngroup_send_message 亲爱的, 我又升级了, 我可以直接读以太坊地址了, 吼吼, 发个钱包地址来看看吧 😘\n\n这样我就会逐条发送给每个用户。\n\nP.S. /group_send_message 也可以缩写为 /gsm",
                msg.chat_id)
            message_content = ' '.join(MSG_SPLIT[1:])
            bot.send_msg_to_all(msg, message_content, bot_owner_chat_id = msg.chat_id)
            return

        # 使用 send_file_to_all 将文件发送给所有用户
        elif MSG_SPLIT[0] in ['group_send_file', 'gsf', '/group_send_file', '/gsf']:
            bot.send_msg(
                f"{msg.user_nick_name}, 你要群发文件, 请直接将文件拖拽给我或者发给我, 但是切记发送前一定要在文件 caption 里填写 /group_send_file 或者简写 /gsf , 这样我才知道这个文件是要求我依次轮询发给所有用户的。不知道 caption 怎么填写可以参考 /group_send_image 的帮助图片哈, 都一样的 😋",
                msg.chat_id)
            return

        # 使用 send_audio_to_all 将 audio 文件发送给所有用户
        elif MSG_SPLIT[0] in ['group_send_audio', 'gsa', '/group_send_audio', '/gsa']:
            bot.send_msg(
                f"{msg.user_nick_name}, 你要群发语音文件 (mp3 或者 wav), 请直接将文件拖拽给我或者发给我, 但是切记发送前一定要在文件 caption 里填写 /group_send_audio 或者简写 /gsa , 这样我才知道这个Audio文件是要求我依次轮询发给所有用户的。不知道 caption 怎么填写可以参考 /group_send_image 的帮助图片哈, 都一样的 😋",
                msg.chat_id)
            return
