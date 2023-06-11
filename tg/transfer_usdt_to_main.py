from tg_binance import *


if __name__ == '__main__':
    # Crontab job 
    '''0 4 * * * cd /root/tg && /root/anaconda3/envs/av/bin/python3 /root/tg/transfer_usdt_to_main.py >> /root/tg/cron.log 2>&1'''

    try: funding_main_transfer_all_usdt()
    except: pass
