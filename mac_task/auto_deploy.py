## 这是需要在我的 Mac 本地运行的Python脚本，用于自动化部署<AI 分身>Bot和网站

# from main import *
import os, sys, json, shutil, random, string, subprocess
from dotenv import load_dotenv
load_dotenv()

# TODO: Customize the path
OPERATION_USER = os.getenv('OPERATION_USER')

root_folder = '/Users/lgg' if OPERATION_USER == 'LEO' else '/home/lgg' if OPERATION_USER == 'YUNDUN' else '/root'
second_folder = 'coding/preangelleo' if OPERATION_USER == 'LEO' else '/home/lgg' if OPERATION_USER == 'YUNDUN' else '/root'

vairables_file_name = 'user_input_variables.txt'
working_folder = f'{root_folder}/Downloads'
user_variables_file = f'{working_folder}/{vairables_file_name}'
archive_folder = f'{working_folder}/Create_AI_Avatar/Users_Archive' if OPERATION_USER == 'LEO' else '/home/lgg' if OPERATION_USER == 'YUNDUN' else '/root'
coding_folder = f'{root_folder}/{second_folder}/ai_avartar' 
configuration_file_name = 'configuration.json'
mac_aliases = f'{root_folder}/.bash_aliases'
on_going_file_name = 'on_going_process.json'

bot_owner_chat_id_json = f'{root_folder}/{second_folder}/ai_avartar/tg/files/bot_owner_chat_id.json'
ubuntu_bash_aliases = '/root/.bash_aliases'
source_aliases_for_ubuntu = f"{coding_folder}/tg/.bash_aliases"

if __name__ == '__main__':
    # 判断用户提供的变量文件是否存在
    if not os.path.exists(user_variables_file): exit(f"ERROR: {user_variables_file} 不存在, 请用户提供该文件并放入 Downloads 文件夹整后再运行.")

    print(f"SETP 1: 从 {user_variables_file} 读出用户个性化变量...")
    Transaction_hash = ''
    with open(user_variables_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line: continue
            elif line.startswith('#'): continue
            elif line.startswith('USER_AVATAR_NAME'): USER_AVATAR_NAME = line.split('=')[1].strip().strip('"').strip("'").lower()
            elif line.startswith('OPENAI_API_KEY'): OPENAI_API_KEY = line.split('=')[1].strip().strip('"').strip("'")
            elif line.startswith('BOT_USERNAME'): BOT_USERNAME = line.split('=')[1].strip().strip('"').strip("'").lower()
            elif line.startswith('BOT_TOKEN'): BOT_TOKEN = line.split('=')[1].strip().strip('"').strip("'")
            elif line.startswith('BOTOWNER_CHAT_ID'): BOTOWNER_CHAT_ID = line.split('=')[1].strip().strip('"').strip("'")
            elif line.startswith('USER_TELEGRAM_LINK'): USER_TELEGRAM_LINK = line.split('=')[1].strip().strip('"').strip("'")
            elif line.startswith('Transaction_hash'): Transaction_hash = line.split('=')[1].strip().strip('"').strip("'")

    is_paied_bot_owner = 0
    if not Transaction_hash:
        confirm_not_paid = input(f"WARNING: 未检测到 Transaction_hash, 请确认是否已经支付了服务费或者可以提供免费服务? (y/n)")
        if confirm_not_paid.lower() in ['y', 'yes']: 
            is_paied_bot_owner = 1
            pass
        else: exit(f"ERROR: 退出程序, 请重新运行并输入正确的选项.")
    else: is_paied_bot_owner = 1

    UBUNTU_SERVER_IP_ADDRESS=input("请输入目标服务器的 IP 地址: ")
    # 判断输入的 IP 地址是否合法
    if not UBUNTU_SERVER_IP_ADDRESS or not UBUNTU_SERVER_IP_ADDRESS.replace('.', '').isdigit(): exit(f"ERROR: 退出程序, IP 地址格式不正确, 请重新运行并输入正确的选项.")
    # 自动生成一个没有字符串的 20 为密码
    UBUNTU_SERVER_ROOT_PASSWORD = ''.join(random.sample(string.ascii_letters + string.digits, 20))

    DOMAIN_NAME=''
    DB_HOST='localhost'
    DB_PORT=3306
    DB_USER='master'
    DB_PASSWORD='QqBZX1yV' # GPTDAO 的 IMAGE 里面的默认密码
    DB_NAME='avatar'
    BOTCREATER_CHAT_ID=2118900665
    REPLICATE_KEY='c72192ecb136caafa562ff2ccf1035ef93d649b5'
    STABILITY_API_KEY='sk-HPE9SpQxqOCstzT36dnGfbN5sl5NkXeYgfAJmflBHdVqQOGK'
    OPENAI_MODEL='gpt-3.5-turbo'
    WOLFRAM_ALPHA_APPID='WA4937-6U5K7UXR74'
    MAX_CONVERSATION_PER_MONTH=1000 # 默认每个用户每月与 Bot 的聊天上限
    PINECONE_FREE='80e14cc4-21bf-4f34-9a9b-73197c82b868'
    PINECONE_FREE_ENV='us-west1-gcp-free'
    INFURA_KEY='d9c26bef583c4fbe9a4f4399b8129b28'
    CMC_PA_API='bbac788f-ab81-41c8-88f5-bd930b14f886'
    FINNHUB_API='cb2o472ad3i3uh8vhpng'
    ETHERSCAN_API='NFPJHR4T6UFT6ENWPAAZI6489V4PS73221'
    MORALIS_API='oYa3si8DJ41gaQWoggoNEfEQ5lrmuRTTodYUi7NpMiu8q73cfeo5XwHGS5CVuxLX'
    MORALIS_ID='4aeb95005e52ca251121e7af'
    MORALIS_APP_ID='LuqQgGIT8g5KPSx7KcnWOJKQUxoFXkrIHdv2GFDQ'
    DEBANK_API='66851eb001290da8bdc25434cb78c5bc495da2dd'
    MONTHLY_FEE=20
    BING_SEARCH_API='411a9fd2a8e9487a90073880cb14a5b9'
    SPEECH_KEY='1c7e1fa0721844649a2eee2bc162426b'
    SPEECH_REGION='westus2'

    VARIABLES_DIC = {
        "USER_AVATAR_NAME": USER_AVATAR_NAME,
        "DOMAIN_NAME": DOMAIN_NAME,
        "UBUNTU_SERVER_IP_ADDRESS": UBUNTU_SERVER_IP_ADDRESS,
        "UBUNTU_SERVER_ROOT_PASSWORD": UBUNTU_SERVER_ROOT_PASSWORD,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "DB_PASSWORD": DB_PASSWORD,
        "BOT_USERNAME": BOT_USERNAME,
        "BOT_TOKEN": BOT_TOKEN,
        "BOTOWNER_CHAT_ID": BOTOWNER_CHAT_ID,
        "USER_TELEGRAM_LINK": USER_TELEGRAM_LINK,
        "OPENAI_MODEL": OPENAI_MODEL,
        "REPLICATE_KEY": REPLICATE_KEY,
        "STABILITY_API_KEY": STABILITY_API_KEY,
        "WOLFRAM_ALPHA_APPID": WOLFRAM_ALPHA_APPID,
        "PINECONE_FREE": PINECONE_FREE,
        "PINECONE_FREE_ENV": PINECONE_FREE_ENV,
        "MAX_CONVERSATION_PER_MONTH": MAX_CONVERSATION_PER_MONTH,
        "INFURA_KEY": INFURA_KEY,
        "CMC_PA_API": CMC_PA_API,
        "FINNHUB_API": FINNHUB_API,
        "ETHERSCAN_API": ETHERSCAN_API,
        "MORALIS_API": MORALIS_API,
        "MORALIS_ID": MORALIS_ID,
        "MORALIS_APP_ID": MORALIS_APP_ID,
        "DEBANK_API": DEBANK_API,
        "MONTHLY_FEE": MONTHLY_FEE,
        "DB_HOST": DB_HOST,
        "DB_PORT": DB_PORT,
        "DB_USER": DB_USER,
        "DB_NAME": DB_NAME,
        "BOTCREATER_CHAT_ID": BOTCREATER_CHAT_ID,
        "BING_SEARCH_API": BING_SEARCH_API, 
        "SPEECH_KEY": SPEECH_KEY,
        "SPEECH_REGION": SPEECH_REGION,
        "Transaction_hash": Transaction_hash,
        "is_paied_bot_owner": is_paied_bot_owner
    }

    # 检查用户输入的变量是否完整
    for k, v in VARIABLES_DIC.items():
        if not v and k not in ['DOMAIN_NAME', 'Transaction_hash']: 
            print(f"ERROR: {k} 为空, 请在 {user_variables_file} 中填写完整后再运行.")
            exit()

    # 打印出完整的用户输入的变量
    print(f"SETP 2: 变量完整:\n\n{json.dumps(VARIABLES_DIC, indent=2)}\n\n继续自动执行以下代码:\n\n")


    USER_AVATAR_NAME = USER_AVATAR_NAME.replace('_', '')
    # 在 users_archive 文件夹中创建用户的文件夹
    print(f"SETP 3: 在 {archive_folder} 文件夹中创建用户的文件夹...")
    user_folder = f'{archive_folder}/{USER_AVATAR_NAME}'
    # 判断文件夹是否已经纯在, 如果存在则询问用户是否删除原文件夹并重新创建, 否则退出程序
    if os.path.exists(user_folder):
        user_input_2 = input(f"WARNING: {user_folder} 已经存在, 请确认是否要删除并重新创建? (y/n)")
        if user_input_2.lower() in ['y', 'yes']:  shutil.rmtree(user_folder)
        else: exit(f"ERROR: 退出程序, 请重新运行并输入正确的选项.")

    if not os.path.exists(user_folder): os.mkdir(user_folder)

    # 将 VARIABLES_DIC 以 json 格式保存到 {user_folder}/{configuration_file_name}
    print(f"SETP 4: 将 VARIABLES_DIC 以 json 格式保存到 {user_folder}/{configuration_file_name}...")
    with open(f'{user_folder}/{configuration_file_name}', 'w') as f: json.dump(VARIABLES_DIC, f, indent=2)

    user_tg_bot_folder = f'{user_folder}/tg'

    print(f"SETP 7: 复制 {coding_folder}/tg 为 {user_tg_bot_folder}...")
    shutil.copytree(f'{coding_folder}/tg', user_tg_bot_folder)

    print(f"SETP 8: 打开 {user_tg_bot_folder}/.env, 为其中的变量赋值...")
    avatar_tg_bot_env_file = f'{user_tg_bot_folder}/.env'
    with open(avatar_tg_bot_env_file) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if not line: continue
            elif line.startswith('#'): continue
            elif line.startswith('USER_AVATAR_NAME'): lines[i] = f'USER_AVATAR_NAME={USER_AVATAR_NAME}\n'
            elif line.startswith('UBUNTU_SERVER_IP_ADDRESS'): lines[i] = f'UBUNTU_SERVER_IP_ADDRESS={UBUNTU_SERVER_IP_ADDRESS}\n'
            elif line.startswith('DOMAIN_NAME'): lines[i] = f'DOMAIN_NAME={DOMAIN_NAME}\n'
            elif line.startswith('DB_PASSWORD'): lines[i] = f'DB_PASSWORD={DB_PASSWORD}\n'
            elif line.startswith('OPENAI_API_KEY'): lines[i] = f'OPENAI_API_KEY={OPENAI_API_KEY}\n'
            elif line.startswith('BOT_TOKEN'): lines[i] = f'BOT_TOKEN={BOT_TOKEN}\n'
            elif line.startswith('BOTOWNER_CHAT_ID'): lines[i] = f'BOTOWNER_CHAT_ID={BOTOWNER_CHAT_ID}\n'
            elif line.startswith('OPENAI_MODEL'): lines[i] = f'OPENAI_MODEL={OPENAI_MODEL}\n'
            elif line.startswith('BOT_USERNAME'): lines[i] = f'BOT_USERNAME={BOT_USERNAME}\n'
            elif line.startswith('REPLICATE_KEY'): lines[i] = f'REPLICATE_KEY={REPLICATE_KEY}\n'
            elif line.startswith('STABILITY_API_KEY'): lines[i] = f'STABILITY_API_KEY={STABILITY_API_KEY}\n'
            elif line.startswith('WOLFRAM_ALPHA_APPID'): lines[i] = f'WOLFRAM_ALPHA_APPID={WOLFRAM_ALPHA_APPID}\n'
            elif line.startswith('USER_TELEGRAM_LINK'): lines[i] = f'USER_TELEGRAM_LINK={USER_TELEGRAM_LINK}\n'
            elif line.startswith('PINECONE_FREE'): lines[i] = f'PINECONE_FREE={PINECONE_FREE}\n'
            elif line.startswith('PINECONE_FREE_ENV'): lines[i] = f'PINECONE_FREE_ENV={PINECONE_FREE_ENV}\n'
            elif line.startswith('MAX_CONVERSATION_PER_MONTH'): lines[i] = f'MAX_CONVERSATION_PER_MONTH={MAX_CONVERSATION_PER_MONTH}\n'
            elif line.startswith('INFURA_KEY'): lines[i] = f'INFURA_KEY={INFURA_KEY}\n'
            elif line.startswith('CMC_PA_API'): lines[i] = f'CMC_PA_API={CMC_PA_API}\n'
            elif line.startswith('FINNHUB_API'): lines[i] = f'FINNHUB_API={FINNHUB_API}\n'
            elif line.startswith('ETHERSCAN_API'): lines[i] = f'ETHERSCAN_API={ETHERSCAN_API}\n'
            elif line.startswith('MORALIS_API'): lines[i] = f'MORALIS_API={MORALIS_API}\n'
            elif line.startswith('MORALIS_ID'): lines[i] = f'MORALIS_ID={MORALIS_ID}\n'
            elif line.startswith('MORALIS_APP_ID'): lines[i] = f'MORALIS_APP_ID={MORALIS_APP_ID}\n'
            elif line.startswith('DEBANK_API'): lines[i] = f'DEBANK_API={DEBANK_API}\n'
            elif line.startswith('MONTHLY_FEE'): lines[i] = f'MONTHLY_FEE={MONTHLY_FEE}\n'
            elif line.startswith('BING_SEARCH_API'): lines[i] = f'BING_SEARCH_API={BING_SEARCH_API}\n'
            elif line.startswith('SPEECH_KEY'): lines[i] = f'SPEECH_KEY={SPEECH_KEY}\n'
            elif line.startswith('SPEECH_REGION'): lines[i] = f'SPEECH_REGION={SPEECH_REGION}\n'
            elif line.startswith('DB_HOST'): lines[i] = f'DB_HOST={DB_HOST}\n'
            elif line.startswith('DB_PORT'): lines[i] = f'DB_PORT={DB_PORT}\n'
            elif line.startswith('DB_USER'): lines[i] = f'DB_USER={DB_USER}\n'
            elif line.startswith('DB_NAME'): lines[i] = f'DB_NAME={DB_NAME}\n'
            elif line.startswith('BOTCREATER_CHAT_ID'): lines[i] = f'BOTCREATER_CHAT_ID={BOTCREATER_CHAT_ID}\n'
            elif line.startswith('Transaction_hash'): lines[i] = f'Transaction_hash={Transaction_hash}\n'

        with open(avatar_tg_bot_env_file, 'w') as f: f.writelines(lines)

        # 为 avatar_tg_bot_env_file 文件添加 is_paied_bot_owner
        with open(avatar_tg_bot_env_file, 'a') as f: f.write(f'\n# 是否是付费用户\nis_paied_bot_owner={is_paied_bot_owner}\n')

    print(f"SETP 9: 用户个性化变量读取并赋值完成, 文件夹已经成功克隆并修改 .env 文件, 准备开始同步到 {UBUNTU_SERVER_IP_ADDRESS}...")

    rsync_tg_bot = f'rsync -avz --exclude=".DS_Store" {user_tg_bot_folder} root@{UBUNTU_SERVER_IP_ADDRESS}:/root/'

    # Append new alias to ~/.bash_aliases
    aliases_need_to_append = f'''
# For {USER_AVATAR_NAME}
alias {USER_AVATAR_NAME}='ssh root@{UBUNTU_SERVER_IP_ADDRESS}'
alias pub{USER_AVATAR_NAME}='ssh-copy-id -i ~/.ssh/id_rsa root@{UBUNTU_SERVER_IP_ADDRESS}'
alias rsb{USER_AVATAR_NAME}=\'{rsync_tg_bot}\'
'''
    with open(mac_aliases, 'a') as f: f.write(aliases_need_to_append)

    # 将 {user_variables_file} 移动到 {user_folder}
    print(f"SETP 11: 将 {user_variables_file} 移动到 {user_folder}")
    shutil.move(user_variables_file, user_folder)

    print(f"SETP 12: 创建临时文件夹 {on_going_file_name}...")
    # 用 build_telegram_bot, build_website, USER_AVATAR_NAME, UBUNTU_SERVER_IP_ADDRESS 创建一个名为 ongoing 的 dictionary, 并且在 {working_folder} 创建一个 on_going_process.json 文件, ongoing 给 auto_upload.py 调用
    ongoing = {
        'user_name': USER_AVATAR_NAME,
        'ip_address': UBUNTU_SERVER_IP_ADDRESS
        }

    with open(f'{working_folder}/{on_going_file_name}', 'w') as f: json.dump(ongoing, f, indent=2)

    print(f"SETP 13: 更新 {bot_owner_chat_id_json} 文件...")
    USER_TELEGRAM_HANDLE = USER_TELEGRAM_LINK.replace('https://t.me/', '')

    # 读出 bot_owner_chat_id_json 为字典
    with open(bot_owner_chat_id_json) as f: bot_owner_chat_id_dic = json.load(f)
    bot_owner_chat_id_dic[USER_TELEGRAM_HANDLE] = BOTOWNER_CHAT_ID

    # 将更新后的 bot_owner_chat_id_dic 保存到 bot_owner_chat_id_json
    with open(bot_owner_chat_id_json, 'w') as f: json.dump(bot_owner_chat_id_dic, f, indent=2)

    print(f'''\nSUCCESS: 自动化部署第一步完成, 请 sz (source ~/.zshrc) 然后用 {USER_AVATAR_NAME} 别名快速登录 {UBUNTU_SERVER_IP_ADDRESS} 设置允许 PublicKey 登录, 步骤如下:

{USER_AVATAR_NAME} (或者 ssh root@{UBUNTU_SERVER_IP_ADDRESS})
ROOT PASSWORD IS: {UBUNTU_SERVER_ROOT_PASSWORD}

sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
systemctl restart ssh

然后用 pub{USER_AVATAR_NAME} 别名将本地的 ~/.ssh/id_rsa.pub 文件上传到 {UBUNTU_SERVER_IP_ADDRESS}

然后再用 cup 别名执行下一步, 根据提示自动化操作...''')