## 这是需要在我的 Mac 本地运行的Python脚本，用于自动化部署<AI 分身>Bot和网站
import subprocess

from auto_deploy import *

# 判断 f'{working_folder}/{on_going_file_name}' 文件是否存在
if not os.path.exists(f'{working_folder}/{on_going_file_name}'): exit(f"ERROR: {working_folder}/{on_going_file_name} 不存在; 这意味着上一个脚本没有正确执行, 请先执行 cad 别名并创造 ongoing 文件后再运行本脚本.")

with open(f'{working_folder}/{on_going_file_name}', 'r') as f: ongoing = json.load(f)

USER_AVATAR_NAME = ongoing['user_name']
UBUNTU_SERVER_IP_ADDRESS = ongoing['ip_address']

user_folder = f'{archive_folder}/{USER_AVATAR_NAME}'
user_tg_bot_folder = f'{user_folder}/tg'

# run rsync_tg_bot with subprocess and prompt me to enter password
print(f"SETP 1:  开始同步 {user_tg_bot_folder} 文件夹到 {UBUNTU_SERVER_IP_ADDRESS} 的 /root/")
subprocess.run(f'rsync -avz {user_tg_bot_folder} root@{UBUNTU_SERVER_IP_ADDRESS}:/root/', shell=True)

# 上传完成后，删除 ongoing 文件
print(f"SETP 2:  删除 {working_folder}/{on_going_file_name} 文件")
os.remove(f'{working_folder}/{on_going_file_name}')

next_step = f'''\nSUCCESS: 自动化部署全部完成, {USER_AVATAR_NAME} 的文件夹已经成功上传到 {UBUNTU_SERVER_IP_ADDRESS}, 接下来请用 {USER_AVATAR_NAME} 别名快速登录 {UBUNTU_SERVER_IP_ADDRESS}:

1. 如果服务器环境是通过 AWS Snapshots 创建的, 登录后只需要执行 cp .env.avatar .env 命令后即可运行 pyi 初始化 Alias
2. 服务器环境尚未搭建也没有通过 IMAGES 创建, 登录后依次执行别名: cms, ccd, cnd, cng 四个 shell 脚本程序, 然后再 pyi 初始化 Alias
3. 最后, 通过 pmtg 启动程序, 并通过 pm2 save && pm2 startup 命令将 pm2 作为服务常驻进程.'''

print(next_step)