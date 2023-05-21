# ai_avartar

制作 AI分身 Bot 及网站 操作流程

1）将的 dialogue_tone.xls, system_prompt.txt 和 user_input_variables.txt发给用户完成;

2）登录 Mac 终端执行 cad 别名, 根据提示操作, 完成代码复制和 .env 文件的生成

3) sz (source ~/.zshrc), 用 {USER_AVATAR_NAME} 别名快速登录 {UBUNTU_SERVER_IP_ADDRESS} 激活 Public Key Login, 登录后黏贴以下代码

sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
systemctl restart ssh

# 如果以上步骤无法实现公钥登录那就要手动修改设置
# nano /etc/ssh/sshd_config
# PubkeyAuthentication yes
# PasswordAuthentication yes
# systemctl restart ssh

4) 发送公钥到 Ubuntu 服务器并测试 ( 可以用aliases 别名 ): 

（别名: {USER_AVATAR_NAME}）ssh root@{UBUNTU_SERVER_IP_ADDRESS} 测试密码登录
（别名: pub{USER_AVATAR_NAME}）ssh-copy-id -i ~/.ssh/id_rsa root@{UBUNTU_SERVER_IP_ADDRESS}
（别名: {USER_AVATAR_NAME}）ssh root@{UBUNTU_SERVER_IP_ADDRESS}

如果公钥（无密码）登录成功, 则进行下一步

3) 登录 Mac 终端执行 cup 别名, 根据提示操作, 上传文件夹到 Ubuntu 服务器

4）sz (source ~/.zshrc), 通过 USER_AVATAR_NAME alias 别名快捷登录 Ubuntu: 依次执行 cms, ccd, cnd, cng 四个 shell 脚本程序

第一步：cms 执行（会安装好 mysql, 创建 master）

第二步：ccd 执行（会安装好 anaconda python 创建 av 虚拟环境）

第三步：cnd 执行（会安装好 nodejs, npm, pnpm, pm2）

- 测试之前先通过 pyi 初始化 telegram bot，初始化成功大概率就没问题了;
- 如果初始化没问题就可以通过 pmtg 将 Telegram Bot 正式运行起来了；
- 成功运行后需要在 Terminal 输入 pm2 save && pm2 startup 保存进程及自动启动

第四步: cng 执行（会安装好 nginx, certbot, 为域名获取 ssl 并设置自动 renew）# 尚未测试成功

4) 两个关键文件：

- system_prompt.txt 
这里记录了该 < AI 分身 > 的角色定位和背景信息以及一些注意事项，如果需要调整角色定位，请修改 txt 文件并保存后直接发给你的 Bot，他会自动保存并在下一条对话的时候自动启用新的角色定位；
- dialogue_tone.xls 
这里记录了一些模拟的聊天记录，用于让 GPT 了解该 AI 分身的说话语气和方式。如果需要调整说话语气，可以直接在 xls 表格里修改历史聊天语气和方式并保存，然后直接发给 Bot 即可。空白的地方可以不填也可以填满，但是最好不要再添加更多了。

用户需要把这两个文件修改好并直接发给已经上线的 Telegram bot, 然后就会开启新的角色和聊天语气。
P.S. 请不要修改文件名和文件格式，否则 Bot 就不认了！