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
alias pmwc='pm2 start ding-dong-bot.py --name wc --interpreter python3'
alias prtg='pm2 restart tg'
alias prwc='pm2 restart wc'
alias pdtg='pm2 delete tg'
alias pdwc='pm2 delete wc'
alias pstg='pm2 stop tg'
alias pswc='pm2 stop wc'

alias pwc='python3 ding-dong-bot.py'

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

alias dwc='docker run --rm -ti -e WECHATY_LOG=verbose -e WECHATY_PUPPET=wechaty-puppet-padlocal -e WECHATY_PUPPET_PADLOCAL_TOKEN=puppet_padlocal_eb452aef230b4d5a91595f8b50529aab -e WECHATY_PUPPET_SERVER_PORT=8788 -e WECHATY_TOKEN="puppet_padlocal_eb452aef230b4d5a91595f8b50529aab" -e WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER=true -p 8788:8788 -d wechaty/wechaty'

# https://blog.zmyos.com/tgproxy.html
alias tgproxy='bash <(wget -qO- https://git.io/mtg.sh)'
# https://github.com/mlldxe/X-UI
alias xui='bash <(curl -Ls https://raw.githubusercontent.com/vaxilu/x-ui/master/install.sh)'

