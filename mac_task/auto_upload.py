## 这是需要在我的 Mac 本地运行的Python脚本，用于自动化部署<AI 分身>Bot和网站
from auto_deploy import *

# 判断 f'{working_folder}/{on_going_file_name}' 文件是否存在
if not os.path.exists(f'{working_folder}/{on_going_file_name}'): exit(f"ERROR: {working_folder}/{on_going_file_name} 不存在; 这意味着上一个脚本没有正确执行, 请先执行 cad 别名并创造 ongoing 文件后再运行本脚本.")

with open(f'{working_folder}/{on_going_file_name}', 'r') as f: ongoing = json.load(f)

build_telegram_bot = ongoing['build_telegram_bot']
build_website = ongoing['build_website']
USER_AVATAR_NAME = ongoing['user_name']
UBUNTU_SERVER_IP_ADDRESS = ongoing['ip_address']

user_folder = f'{archive_folder}/{USER_AVATAR_NAME}'
user_website_folder = f'{user_folder}/wb'
user_tg_bot_folder = f'{user_folder}/tg'
user_aliases = f'{user_folder}/.bash_aliases'

if build_telegram_bot:
    # run rsync_tg_bot with subprocess and prompt me to enter password
    print(f"SETP 1:  开始同步 {user_tg_bot_folder} 文件夹到 {UBUNTU_SERVER_IP_ADDRESS} 的 /root/")
    subprocess.run(f'rsync -avz {user_tg_bot_folder} root@{UBUNTU_SERVER_IP_ADDRESS}:/root/', shell=True)

if build_website:
    # run rsync_website with subprocess and prompt me to enter password
    print(f"SETP 2: 开始同步 {user_website_folder} 文件夹到 {UBUNTU_SERVER_IP_ADDRESS} 的 /root/")
    subprocess.run(f'rsync -avz {user_website_folder} root@{UBUNTU_SERVER_IP_ADDRESS}:/root/', shell=True)

if os.path.isfile(user_aliases): 
    print(f"SETP 3: 将 {user_aliases} 上传到 {UBUNTU_SERVER_IP_ADDRESS}:{ubuntu_aliases}")
    subprocess.run(f'rsync -avz {user_aliases} root@{UBUNTU_SERVER_IP_ADDRESS}:{ubuntu_aliases}', shell=True)

# 上传完成后，删除 ongoing 文件
os.remove(f'{working_folder}/{on_going_file_name}')

print(f"\nSUCCESS: 自动化部署全部完成, {USER_AVATAR_NAME} 的文件夹已经成功上传到 {UBUNTU_SERVER_IP_ADDRESS}, 接下来请用 {USER_AVATAR_NAME} 别名快速登录 {UBUNTU_SERVER_IP_ADDRESS} 并依次执行别名: cms, ccd, cnd, cng 四个 shell 脚本程序")