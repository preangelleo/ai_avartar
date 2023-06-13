alias nb='nano /root/.bash_aliases'
alias sb='source ~/.bashrc'
alias sba='source ~/.bash_aliases'
alias a='alias'
alias ll='ls -alF'
alias la='ls -A'
alias c='clear'
alias cb='cd /root/backup'

alias pip='pip3'
alias pm='pm2'

alias pipr='pip3 install -r requirements.txt'

alias pmr='pm2 restart'
alias pmra='pm2 restart all'
alias pms='pm2 stop'
alias pmsall='pm2 stop all'
alias pmdall='pm2 delete all'
alias pml='pm2 list'
alias pmlg='pm2 logs'
alias py='python3'

alias pyl='python3 local_bot.py'
alias pyi='python3 bot_init.py'

alias pmtg='pm2 start local_bot.py --name tg --interpreter python3'
alias prtg='pm2 restart tg'
alias pdtg='pm2 delete tg'
alias pstg='pm2 stop tg'
alias pmlgtg='pm2 logs tg'

alias pmfb='pm2 start ai_avartar/src/bot/fanbook/fanbook_bot.py --name fb --interpreter python3'
alias prfb='pm2 restart fb'
alias pdfb='pm2 delete fb'
alias psfb='pm2 stop fb'
alias pmlgtg='pm2 logs fb'

alias pmwb="pm2 start npm --name wb -- start"
alias prwb="pm2 restart wb"
alias pdwb='pm2 delete wb'
alias pswb='pm2 stop wb'

alias cmx='chmod +x'
alias croot='sudo chown root:root /root && sudo chmod 700 /root'

alias ctg='cd /root/tg'
alias cwb='cd /root/wb'
alias cca='conda create -n av'
alias cde='conda deactivate && cd ~'
alias cav='cd /root/tg && conda activate av'
alias cms='cd /root/tg && chmod +x auto_mysql.sh && ./auto_mysql.sh'
alias ccd='cd /root/tg && chmod +x auto_conda.sh && ./auto_conda.sh'
alias cnd='cd /root/tg && chmod +x auto_node.sh && ./auto_node.sh'
alias cng='cd /root/tg && chmod +x auto_nginx.sh && ./auto_nginx.sh'
alias wbd='cd /root/wb && pnpm build'
alias wpi='cd /root/wb && pnpm i'
alias wpd='cd /root/wb && pnpm dev'
