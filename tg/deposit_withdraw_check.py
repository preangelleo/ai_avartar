from tg_binance import *


if __name__ == '__main__':
    # Crontab job 每三分钟运行一次检查充值和提币
    '''*/3 * * * * cd /root/tg && /root/anaconda3/envs/av/bin/python3 /root/tg/deposit_withdraw_check.py >> /root/tg/cron.log 2>&1'''

    try: get_deposit_history_by_hours(chat_id=BOTOWNER_CHAT_ID, hours=0.05)
    except: pass

    try: get_withdraw_history_by_hours(chat_id=BOTOWNER_CHAT_ID, hours=0.05)
    except: pass

    try: binance_position_buy_check_all(chat_id=BOTOWNER_CHAT_ID, coin=None, target_profit=0.07, crontab=True)
    except: pass

