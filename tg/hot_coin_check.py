from tg_binance import *

''' Coinmarketcap API Plan Feature 
Feature	 BASIC Free No subscription required
Rest API	9 latest market data endpoints & exchange asset reserve endpoints
Monthly API credits	10,000
Rate limit	30 Requests per minute
Update frequency	**Every 1 minute
'''

if __name__ == '__main__':
    # Crontab job 
    '''0 */4 * * * cd /root/tg && /root/anaconda3/envs/av/bin/python3 /root/tg/hot_coin_check.py >> /root/tg/cron.log 2>&1'''

    try: binance_today_hot_coins_check(chat_id=BOTOWNER_CHAT_ID, user_nick_name='亲爱的', crontab=True, trading_volume_limit = 30_000_000, check_size = 1000)
    except: pass
