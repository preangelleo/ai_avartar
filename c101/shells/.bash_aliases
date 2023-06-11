alias nb='nano /root/.bash_aliases'
alias sb='source ~/.bashrc'
alias sba='source ~/.bash_aliases'
alias a='alias'
alias ll='ls -alF'
alias la='ls -A'
alias c='clear'
alias cb='cd /root/backup'
alias cj='cd /root/major'
alias ce='conda deactivate && cd ~'

alias cam='conda activate env-major && cd /root/major'
alias cm='conda activate env-major && cd /root/major'
alias cmj='conda activate env-major && cd /root/major'

alias pi='pip3 install'
alias pm='pm2'

alias pipr='pip3 install -r requirements.txt'

alias pmcb='pm2 start chatgpt_bot.py --name cb --interpreter python3'
alias prcb='pm2 restart cb'

alias pmeb='pm2 start email_bot.py --name eb --interpreter python3'
alias preb='pm2 restart eb'

alias pmst='pm2 start c101_run_st.py --name st --interpreter python3'
alias prst='pm2 restart st'

alias pmds='pm2 start c101discord.py --name ds --interpreter python3'
alias prds='pm2 restart ds'

alias pmlh='conda activate lh && cd /root/leonardo && pm2 start local_bot.py --name lh --interpreter python3'
alias prlh='pm2 restart lh'

alias pmfb='pm2 start c101fanbook.py --name fb --interpreter python3'
alias prfb='pm2 restart fb'

alias pmvb='pm2 start c101variables.py --name vb --interpreter python3'
alias prvb='pm2 restart vb'

alias pmr='pm2 restart'
alias pmra='pm2 restart all'
alias pms='pm2 stop'
alias pmsa='pm2 stop all'
alias pmda='pm2 delete all'
alias pml='pm2 list'
alias pmlg='pm2 logs'
alias py='python3'
alias pyb='python3 chatgpt_bot.py'
alias pys='streamlit run c101streamlit.py --server.port 8501'
alias pyd='python3 c101dictionary.py'

alias ip='curl -4 icanhazip.com'

alias wpy='which python3'

alias restore='chmod +x /root/db_auto_restore.sh && /root/db_auto_restore.sh'
alias backup='chmod +x /root/db_auto_back.sh && /root/db_auto_back.sh'

alias rst='chmod +x /root/db_auto_restore.sh && /root/db_auto_restore.sh'
alias bkp='chmod +x /root/db_auto_back.sh && /root/db_auto_back.sh'
alias croot='sudo chown root:root /root && sudo chmod 700 /root'
alias pub='sudo chown root:root /root && sudo chmod 700 /root'