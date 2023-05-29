import json
import sqlalchemy
from src.utils.param_singleton import Params
from src.bot.bot_branch.payment_branch.crpto.utils import generate_eth_address
from src.database.mysql import *
from src.utils.utils import (
    insert_system_prompt_from_file,
    get_system_prompt,
    insert_dialogue_tone_from_file,
    get_dialogue_tone,
)


# initiate the avatar_user_priority table, set BOT_OWNER_ID as the owner, set BOT_OWNER_ID as the admin,
# set BOT_OWNER_ID as the vip, set BOT_OWNER_ID as the paid, set BOT_OWNER_ID as the active, set BOT_OWNER_ID as the
# deleted, set BOT_OWNER_ID as the priority 100, set BOT_OWNER_ID as the free_until 2099-12-31 23:59:59
def initialize_user_priority_table():
    print(f"DEBUG: initialize_user_priority_table()")
    # Create a new session
    with Params().Session() as session:
        for from_id in bot.bot_admin_id_list:
            # Query the table 'avatar_user_priority' to check if the from_id exists
            from_id_exists = session.query(
                sqlalchemy.exists().where(UserPriority.user_from_id == from_id)
            ).scalar()
            if from_id_exists:
                # Update the key_value
                session.query(UserPriority).filter(
                    UserPriority.user_from_id == from_id
                ).update(
                    {
                        UserPriority.is_admin: 1,
                        UserPriority.is_owner: 1,
                        UserPriority.is_vip: 1,
                        UserPriority.is_paid: 1,
                        UserPriority.is_active: 1,
                        UserPriority.priority: 100,
                        UserPriority.free_until: datetime(2099, 12, 31, 23, 59, 59),
                    }
                )
            else:
                # Insert the from_id and key_value
                new_user_priority = UserPriority(
                    user_from_id=from_id,
                    is_admin=1,
                    is_owner=1,
                    is_vip=1,
                    is_paid=1,
                    is_active=1,
                    priority=100,
                    free_until=datetime(2099, 12, 31, 23, 59, 59),
                    update_time=datetime.now(),
                )
                session.add(new_user_priority)
            # Commit the session
            session.commit()
    return True


def initialize_owner_parameters_table():
    print(f"DEBUG: initialize_owner_parameters_table()")

    # Create a new session
    with Params().Session() as session:
        # 清空 avatar_owner_parameters 表
        session.query(OwnerParameter).delete()
        session.commit()
        print(f"avatar_owner_parameters 表已清空!")
        # Read .env to get the owner's parameters
        with open('.env', 'r') as f:
            for line in f.readlines():
                print(f"DEBUG: line = {line}")
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parameter_name, parameter_value = line.split('=', 1)
                parameter_name = parameter_name.strip()
                parameter_value = parameter_value.strip()

                # Insert the owner's parameters into the table 'avatar_owner_parameters'
                new_owner_parameter = OwnerParameter(
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                    update_time=datetime.now(),
                )
                session.add(new_owner_parameter)
                session.commit()
    return


if __name__ == '__main__':
    print(f"TELEGRAM_BOT initialing for {bot.bot_owner_name}...")

    make_a_choise = input(
        f"这是系统从镜像 IMAGE 文件启动后的首次初始化还是代码更新后的初始化？\n首次初始化要输入 'first_time_initiate'; \n代码更新后的初始化请直接按回车键: "
    )
    is_first_time_initiate = True if make_a_choise == 'first_time_initiate' else False

    print(f"\nSTEP 1: 创建所有数据库表单 ...")
    with Params().Session() as session:
        Base.metadata.create_all(bind=Params().engine)

    print(
        f"\nSTEP 2: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ..."
    )
    if is_first_time_initiate:
        confirm = input(
            f"确认要清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表吗？请输入 'yes' 确认: "
        )
        if confirm == 'yes':
            with Params().Session() as session:
                session.query(ChatHistory).delete()
                session.query(EthWallet).delete()
                session.query(CryptoPayments).delete()
                session.query(UserPriority).delete()
                session.query(SystemPrompt).delete()
                session.query(DialogueTone).delete()
                session.commit()

    print(f"\nSTEP 3: 更新 Bot Owner 的系统参数 ...")
    initialize_owner_parameters_table()

    print(f"\nSTEP 4: 读取并打印出 Bot Owner 的系统参数 ...")
    owner_parameters_dict = Params().get_owner_parameters()
    for parameter_name, parameter_value in owner_parameters_dict.items():
        print(f"{parameter_name}: {parameter_value}")

    if is_first_time_initiate:
        print(f"\nSTEP 5: 将 System Prompt 写入数据库表单 ...")
        insert_system_prompt_from_file(file_path='files/system_prompt.txt')

    print(f"\nSTEP 6: 读取并打印出 System Prompt ...")
    system_prompt = get_system_prompt()
    print(f"System Prompt: \n\n{system_prompt}")

    if is_first_time_initiate:
        print(f"\nSTEP 7: 将 Dialogue Tone 写入数据库表单 ...")
        # 读取 files/dialogue_tone.xls 并插入到 avatar_dialogue_tone 表中
        insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')

    print(f"\nSTEP 8: 读取并打印出 Dialogue Tone ...")
    msg_history = get_dialogue_tone()
    # print msg_history in json format indented
    print(json.dumps(msg_history, indent=2, ensure_ascii=False))

    print(f"\nSTEP 9: 测试生成 eth address ...")
    user_from_id = '2118900665'
    address = generate_eth_address(user_from_id)
    print(f"{user_from_id} ETH Address: {address}")

    print(f"\nSTEP 10: 初始化用户状态列表 ...")
    initialize_user_priority_table()

    print(f"\nTELEGRAM_BOT initialing for {bot.bot_owner_name} finished!")
