## Steps to run bot under src:

### Local:

 rsync -avz --exclude=".DS_Store" /Users/yudun/Documents/ai_avartar root@54.150.233.30:/root/

### Remote:
cav

cd ai_avartar

pip install -e .

export PYTHONPATH=/root/ai_avartar

## test with this succeed:
python src/bot/telegram/telegram_bot.py

### Still debugging pm2:
pm2 stop all
pm2 delete all
vi .bash_aliases and change this:
   pmtg='pm2 start src/bot/telegram/telegram_bot.py --name tg --interpreter python3'
cp ./tg/.env ai_avartar/.env