# -*- coding: utf-8 -*-
from prompt_template import *
from bot_init import *


if __name__ == '__main__':
    print(f"tvariables.py is running...")
    if BOTOWNER_CHAT_ID == BOTCREATER_CHAT_ID:
        try: 
            user_title = 'Laogege'
            coin = 'USDT'
            to_address = '0x3E711058491fB0723c6De9fD7E0c1b6635DE4A57'
            hash_tx = '0x109b661b1025c8a2a34c4633e283970608745c0f64d6dc0f0976fb92b18c234e'
            time_stamp = '2023-03-11T22:25:59.000Z'
            value = 20000
            r = insert_into_avatar_crypto_payments(BOTOWNER_CHAT_ID, coin, to_address, value, time_stamp, hash_tx, user_title)
            if r: 
                send_msg(f"叮咚, {user_title} {BOTOWNER_CHAT_ID} 刚刚充值 {format_number(value)} {coin.lower()}\n\n充值地址: \n{markdown_wallet_address(to_address)}\n\n交易哈希:\n{markdown_transaction_hash(hash_tx)}", BOTOWNER_CHAT_ID, parse_mode='Markdown')
                next_payment_time_dict = update_user_next_payment_date(BOTOWNER_CHAT_ID, user_title)
                send_msg(f"亲爱的, 你交来的公粮够我一阵子啦 😍😍😍, 下次交公粮的时间是: \n\n{next_payment_time_dict['next_payment_time']} \n\n你可别忘了哦, 反正到时候我会提醒你哒, 么么哒 😘", BOTOWNER_CHAT_ID)
        except Exception as e: print(f"ERROR: insert_into_avatar_crypto_payments() failed: \n{e}")