import json
from src.utils.param_singleton import Params
from src.database.mysql import *
from src.utils.utils import (
    insert_system_prompt_from_file,
    get_system_prompt,
    insert_dialogue_tone_from_file,
    get_system_prompt_and_dialogue_tone,
)


if __name__ == '__main__':
    print(f"\nSTEP 1: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ...")
    with Params().Session() as session:
        session.query(ChatHistory).delete()
        session.query(EthWallet).delete()
        session.query(CryptoPayments).delete()
        session.query(UserPriority).delete()
        session.query(SystemPrompt).delete()
        session.query(DialogueTone).delete()
        session.commit()

    print(f"\nSTEP 2: 将 System Prompt 写入数据库表单 ...")
    insert_system_prompt_from_file(file_path='files/system_prompt.txt')

    print(f"\nSTEP 3: 读取并打印出 System Prompt ...")
    system_prompt = get_system_prompt()
    print(f"System Prompt: \n\n{system_prompt}")

    print(f"\nSTEP 4: 将 Dialogue Tone 写入数据库表单 ...")
    # 读取 files/dialogue_tone.xls 并插入到 avatar_dialogue_tone 表中
    insert_dialogue_tone_from_file(file_path='files/dialogue_tone.csv')

    print(f"\nSTEP 5: 读取并打印出 Dialogue Tone ...")
    msg_history = get_system_prompt_and_dialogue_tone()
    # print msg_history in json format indented
    print(json.dumps(msg_history, indent=2, ensure_ascii=False))
