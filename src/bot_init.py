import json

from bot.bot_branch.payment_branch.crpto.utils import generate_eth_address
from src.utils.utils import *

if __name__ == '__main__':
    print(f"TELEGRAM_BOT initialing for {Params().TELEGRAM_USERNAME}...")

    make_a_choise = input(
        f"这是系统从镜像 IMAGE 文件启动后的首次初始化还是代码更新后的初始化？\n首次初始化要输入 'first_time_initiate'; \n代码更新后的初始化请直接按回车键: ")
    is_first_time_initiate = True if make_a_choise == 'first_time_initiate' else False

    print(f"\nSTEP 1: 创建所有数据库表单 ...")
    with Params().Session() as session:
        Base.metadata.create_all(bind=Params().engine)

    print(f"\nSTEP 2: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ...")
    if is_first_time_initiate:
        confirm = input(
            f"确认要清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表吗？请输入 'yes' 确认: ")
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
    owner_parameters_dict = get_owner_parameters()
    for parameter_name, parameter_value in owner_parameters_dict.items(): print(f"{parameter_name}: {parameter_value}")

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

    print(f"\nTELEGRAM_BOT initialing for {Params().TELEGRAM_USERNAME} finished!")





