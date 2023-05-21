# ai_avartar

新的 IMAGE 建好以后，需要考虑以下步骤完成新服务器的个性化设置：

1）MAC 终端执行 cad alias 创建用户文件夹并完成程序源码和.env.avatar的复制以及在本地 bash_aliases 为用户添加新的 aliases 快捷键;

2）从 AWS 后台登录新的 Instance，修改 root 的密码，激活 Publickey 登录还是省不了要做, 如果镜像 IMAGE 也同步了 Public 登录功能, 最好也是要更换一个新的 root 密码，直接使用上一步生成的密码即可;

sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
systemctl restart ssh

3）然后我的电脑本地用一个 alias 或者 shell script 上传刚刚为新用户生成的 .evn.avatar 文件到 tg 项目目录下

4）登录到服务器后台，cav 进入项目文件夹 cp .env.avatar .env

5）然后通过 pyi 初始化一下（这个过程第一步要增加一下 Mysql 的数据库清空, IMAGE 里面应该是有老的数据库 Tables 数据的）