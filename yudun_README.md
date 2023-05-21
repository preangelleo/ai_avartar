
制作 AI分身 Bot 及网站 操作流程


1. change auto_deploy 
2. Create /Users/yudun/ai_avartar/download/user_input_variables.txt
3. Run cd /Users/yudun/ai_avartar/mac_task && python3 auto_deploy.py


# TODO(@yudun): Customize
alias yudun='ssh root@54.150.233.30'
alias pubyudun='ssh-copy-id -i ~/.ssh/id_rsa root@54.150.233.30'
alias rsbyudun='rsync -avz --exclude=".DS_Store" /Users/yudun/ai_avartar/download/Create_AI_Avatar/Users_Archive/yudun/tg root@54.150.233.30:/root/'


请输入目标服务器的 IP 地址: enter the lightsail ip address of new instances
4. Login to the instance and:
sudo -i
pass wd
change to the one hinted by step 3

Then run:
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
systemctl restart ssh

New aliases are added to .bash_aliaes
`source .bash_aliaes`
Then you can log into your new instance with the given password (saved in /Users/yudun/ai_avartar/download/Create_AI_Avatar/Users_Archive/yudun/configuration.json)

Run `pubyudun`

5. Run `python3 mac_task/auto_upload.py` in local environment 
It will run rsync to upload tg folder to the instance
Copy tg/.bash_aliases to instance

6. Follow the instructions printed by auto_upload, run cms, ccd, cnd

7. run pyi

8. Run pmtg

Finished
