from chatgpt_bot import *

# https://a1.fanbook.mobi/api/bot/bot2c829f9283969c688001e19b628cba3989d5e164f375edc6a239ab91253d2ad121ec4a7bec8027d63dc323820f54ac58/getMe

# FANBOOK_CLIENT_ID=os.getenv("FANBOOK_CLIENT_ID")
# FANBOOK_SECRET=os.getenv("FANBOOK_SECRET")
# FANBOOK_DICTIONARY_BOT=os.getenv("FANBOOK_DICTIONARY_BOT")

# Replace 'YOUR_BOT_TOKEN' with the bot token you copied from the Discord Developer Portal

'''{
"ok": true,
"result": {
"id": 492100155395661800,
"is_bot": true,
"first_name": "查单词",
"last_name": "492095151452565504",
"username": "查单词",
"avatar": "https://fanbook-gamescluster-1251001060.cos.ap-shanghai.myqcloud.com/open-fanbook/pro/BotAvatar-703cb1eeda0dd1c1101f28f3d0a23b00.jpg?v=1682548707000",
"user_token": "c912b6f823d925c25d14e8855c04ef5b223bb572fa884ff0791741b6dea8358851ed1f67841c50986c84fd13a76c3e8f93e332e08bdb5338749d20ac14853b2bb917a66b9176136cc8547426212bb7b84a630fab7cb44b4f7ebf76ae913ea7e24204b322dceebfa5ec2fd1c9710831ba",
"owner_id": 492095151452565500,
"can_join_groups": false,
"can_read_all_group_messages": false,
"supports_inline_queries": false
}
}'''

# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from websocket import WebSocketConnectionClosedException
from websocket._core import create_connection

'''
{'action': 'connect', 'data': {'client_id': '0a0504670b5d00020a20'}}
{'action': 'pong', 'data': {'time': 1682576627}}
{'action': 'push', 'data': {'content': '{"type":"text","text":"${@!492100155395661824}opulent","contentType":1}', 'time': 1682576638421, 'user_id': '492095151452565504', 'channel_id': '492117767286538242', 'message_id': '492217304810033152', 'quote_l1': None, 'quote_l2': None, 'guild_id': '492117767177486336', 'channel_type': 0, 'status': 0, 'nonce': '492216178593271809', 'ctype': 1, 'mentions': [{'nickname': '查单词', 'user_id': '492100155395661824'}], 'member': {'nick': None, 'roles': ['492117767265566720'], 'guild_card': None}, 'author': {'nickname': '老哥哥', 'username': '12844776', 'avatar': 'https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f', 'avatar_nft': None, 'bot': False}, 'desc': ''}, 'ack': -1, 'seq': None}
{'action': 'pong', 'data': {'time': 1682576647}}
'''
'''
{'action': 'push', 'data': {'content': '{"type":"text","text":"后台打印出来消息了","contentType":0}', 'time': 1682576692756, 'user_id': '492095151452565504', 'channel_id': '492117767286538242', 'message_id': '492217532707540992', 'quote_l1': None, 'quote_l2': None, 'guild_id': '492117767177486336', 'channel_type': 0, 'status': 0, 'nonce': '492217304810033153', 'ctype': 0, 'member': {'nick': None, 'roles': ['492117767265566720'], 'guild_card': None}, 'author': {'nickname': '老哥哥', 'username': '12844776', 'avatar': 'https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f', 'avatar_nft': None, 'bot': False}, 'desc': ''}, 'ack': -1, 'seq': None}
'''

'''
{
    "action": "push",
    "data": {
        "content": "{\"type\":\"text\",\"text\":\"${@!492100155395661824}这个机器人的 ID 应该是固定的吧\",\"contentType\":1}",
        "time": 1682576991910,
        "user_id": "492095151452565504",
        "channel_id": "492117767286538242",
        "message_id": "492218787450359808",
        "quote_l1": null,
        "quote_l2": null,
        "guild_id": "492117767177486336",
        "channel_type": 0,
        "status": 0,
        "nonce": "492217532707540993",
        "ctype": 1,
        "mentions": [
            {
                "nickname": "查单词",
                "user_id": "492100155395661824"
            }
        ],
        "member": {
            "nick": null,
            "roles": [
                "492117767265566720"
            ],
            "guild_card": null
        },
        "author": {
            "nickname": "老哥哥",
            "username": "12844776",
            "avatar": "https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f",
            "avatar_nft": null,
            "bot": false
        },
        "desc": ""
    },
    "ack": -1,
    "seq": null
}
{
    "action": "push",
    "data": {
        "content": "{\"type\":\"text\",\"text\":\"我在测试，大家请无视我的消息，哈哈哈\",\"contentType\":0}",
        "time": 1682577000288,
        "user_id": "492095151452565504",
        "channel_id": "492117767286538242",
        "message_id": "492218822590238720",
        "quote_l1": null,
        "quote_l2": null,
        "guild_id": "492117767177486336",
        "channel_type": 0,
        "status": 0,
        "nonce": "492218787450359809",
        "ctype": 0,
        "member": {
            "nick": null,
            "roles": [
                "492117767265566720"
            ],
            "guild_card": null
        },
        "author": {
            "nickname": "老哥哥",
            "username": "12844776",
            "avatar": "https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f",
            "avatar_nft": null,
            "bot": false
        },
        "desc": ""
    },
    "ack": -1,
    "seq": null
}
'''

def send_fb_msg_simple(chat_id, msg_text):
    """Sends a message using the Fanbook API"""
    url = f"https://a1.fanbook.mobi/api/bot/{FANBOOK_DICTIONARY_BOT}/sendMessage"
    headers = {'Content-type': 'application/json'}
    payload = {
        'chat_id': int(chat_id),
        'text': msg_text,
        'desc': msg_text
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def send_fb_msg(chat_id, msg_text, desc='', parse_mode='Fanbook', selective=False, disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None, reply_to_message_id_level_2=None, reply_markup=None, unreactive=None, ephemeral=None, users=None, mentions=None, mention_roles=None):
    """Sends a message using the Fanbook API"""
    url = f"https://a1.fanbook.mobi/api/bot/{FANBOOK_DICTIONARY_BOT}/sendMessage"
    headers = {'Content-type': 'application/json'}
    payload = {
        'chat_id': int(chat_id),
        'text': msg_text,
        'desc': desc,
        'parse_mode': parse_mode,
        'selective': selective,
        'disable_web_page_preview': disable_web_page_preview,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_to_message_id_level_2': reply_to_message_id_level_2,
        'reply_markup': reply_markup,
        'unreactive': unreactive,
        'ephemeral': ephemeral,
        'users': users,
        'mentions': mentions,
        'mention_roles': mention_roles
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()
'''
{"ok": true,
"result": {
"message_id": 492374057917190144,
"date": 1682614011277,
"chat": {
    "id": 492117767286538242,
    "guild_id": 492117767177486336,
    "type": "channel",
    "channel_type": 0
},
"from": {
    "id": 492100155395661824,
    "is_bot": true,
    "first_name": "\u67e5\u5355\u8bcd",
    "username": "12551933",
    "avatar": "https://fanbook-gamescluster-1251001060.cos.ap-shanghai.myqcloud.com/open-fanbook/pro/BotAvatar-703cb1eeda0dd1c1101f28f3d0a23b00.jpg?v=1682548707000"
},
"reply_to_message": null,
"text": "{\"type\":\"text\",\"contentType\":0,\"text\":\"\u5355\u8bcd:\\t opulent\\n\u6392\u540d:\\t 18007\\n\u53d1\u97f3:\\t [\u02c8\u0251\u02d0pj\u0259l\u0259nt]\\n\u8bcd\u5e93:\\t GMAT / SAT\\n\u8bcd\u610f:\\t adj. \u8c6a\u534e\u7684\u3001\u5bcc\u4e3d\u5802\u7687\u7684\u3001\u5bcc\u6709\u7684\u3001\u9614\u7ef0\u7684\u3001\u4e30\u5bcc\u7684\u3001\u5927\u91cf\u7684\\n\u540c\u4e49:\\t grand(1687) | luxurious(9728) | lavish(10032) | extravagant(11474) | sumptuous(16459)\\n\u82f1\u8bd1:\\t \\nOpulent means having or displaying a great deal of wealth, luxury, or grandeur. It is often used to describe a person, place, or thing that is very wealthy and luxurious.\"}",
"entities": []}}'''

def on_message(message):
    s = message.decode('utf8')
    obj = json.loads(s)
    # print(json.dumps(obj, indent=4, ensure_ascii=False))
    # ${@!492100155395661824}
    # r.get('data').get('content').get('text')
    if obj.get('action') == 'push':
        # if debug: print(f"DEBUG: FANBOOK GOT obj: {obj}")
        '''FANBOOK GOT obj: {'action': 'push', 'data': {'content': '{"type":"text","text":"${@!492100155395661824}scupulous","contentType":1}', 'time': 1682612426397, 'user_id': '492095151452565504', 'channel_id': '492117767286538242', 'message_id': '492367410460889088', 'quote_l1': None, 'quote_l2': None, 'guild_id': '492117767177486336', 'channel_type': 0, 'status': 0, 'nonce': '492363435628040193', 'ctype': 1, 'mentions': [{'nickname': '查单词', 'user_id': '492100155395661824'}], 'member': {'nick': None, 'roles': ['492117767265566720'], 'guild_card': None}, 'author': {'nickname': '老哥哥', 'username': '12844776', 'avatar': 'https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f', 'avatar_nft': None, 'bot': False}, 'desc': ''}, 'ack': -1, 'seq': None}'''

        is_bot = obj.get('data').get('author').get('bot')
        if is_bot: return

        # 获取 channel_id
        channel_id = obj.get('data').get('channel_id')
        author = obj.get('data').get('author').get('nickname')
        if not channel_id or not author: return

        try:
            bot_is_mentioned = False
            is_mentioned = True if obj.get('data').get('ctype') == 1 else False
            if is_mentioned:
                bot_is_mentioned_df = pd.DataFrame(obj.get('data').get('mentions'))
                if not bot_is_mentioned_df.empty:
                    bot_is_mentioned = True if bot_is_mentioned_df['nickname'].str.contains('AI_英语老师_Amy').any() else False
        except Exception as e: print(f"ERROR: FANBOOK: {e}")
        
        channel_type = obj.get('data').get('channel_type')
        guild_id = obj.get('data').get('guild_id')

        data_str = obj.get('data').get('content')
        data_dict = json.loads(data_str)

        if data_dict.get('type') == 'text':
            msg_text = data_dict.get('text')

            # if msg_text.startswith('${@!492100155395661824}'):
            msg_text = msg_text.replace('${@!492100155395661824}', '')

            if len(msg_text.split()) == 1 and is_english(msg_text): 

                if (msg_text.lower() != 'r' and len(msg_text) == 1) or msg_text.lower() in ['help', 'hi', 'hello', 'sup'] or '/' in msg_text: 
                    try: send_fb_msg_simple(chat_id = int(channel_id), msg_text = f"@{author}\n{english_bot_welcome_and_help_info}")
                    except Exception as e: print(f"ERROR: FANBOOK SEND MSG ERROR: {e}")                    
                    return
                
                if msg_text.lower() == 'r':
                    df_random = pd.read_sql_query(f"SELECT `word` FROM `db_daily_words` WHERE `rank` > 500 ORDER BY RAND() LIMIT 1", db_engine)
                    msg_text = df_random['word'].values[0]

                word_dict = st_find_ranks_for_word(msg_text.lower())
                if word_dict:
                    word = word_dict.get('word', '')

                    if not bot_is_mentioned and word_dict.get('rank', '') and word_dict.get('rank', '') < 500: 
                        print(f"DEBUG: FANBOOK: dictionary bot was not mentioned and rank is less than 1000, ignore.")
                        return 

                    word_category = [key.upper() for key, value in word_dict.items() if value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
                    word_category_str = ' / '.join(word_category)
                    word_trans = {
                        '单词': word,
                        '排名': word_dict.get('rank', ''),
                        '发音': word_dict.get('us-phonetic', ''),
                        '词库': word_category_str,
                        '词意': word_dict.get('chinese', ''),
                    }
                    results = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)

                    # 将查询结果发回到群里
                    try: send_fb_msg_simple(chat_id = int(channel_id), msg_text = f"@{author}\n{results}")
                    except Exception as e: print(f"ERROR: FANBOOK SEND MSG ERROR: {e}")

            if bot_is_mentioned or channel_type == 3 or not guild_id:
                # results = chat_gpt_regular(msg_text)
                msg_text = msg_text.replace('${@!492100155395661824}', '')
                try:
                    if is_english(msg_text): message = chat_gpt_english(msg_text)
                    else: message = chat_gpt_chinese(msg_text)
                    send_fb_msg_simple(chat_id = int(channel_id), msg_text = f"@{author}\n{message}")
                    
                except Exception as e:
                    print(f"ERROR: fanbook_english_dictionary() failed with error: \n{e}")
                    return 
    return 

def send_ping(ws):
    while True:
        time.sleep(20)
        ws.send('{"type":"ping"}')

def get_me():
    BASE_URL = 'https://a1.fanbook.mobi/api'
    response = requests.get(f"{BASE_URL}/bot/{FANBOOK_DICTIONARY_BOT}/getMe", timeout=3)
    return response.json()

def get_private_chat():
    BASE_URL = 'https://a1.fanbook.mobi/api'
    response = requests.get(f"{BASE_URL}/bot/{FANBOOK_DICTIONARY_BOT}/getPrivateChat", timeout=3)
    return response.json()
'''{'action': 'push', 'data': {'content': '{"type":"text","text":"ostentatious","contentType":0}', 'time': 1682613126167, 'user_id': '492095151452565504', 'channel_id': '492370317524983808', 'message_id': '492370345508999168', 'quote_l1': None, 'quote_l2': None, 'guild_id': None, 'channel_type': 3, 'status': 0, 'nonce': '492370317579509761', 'ctype': 0, 'author': {'nickname': '老哥哥', 'username': '12844776', 'avatar': 'https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f', 'avatar_nft': None, 'bot': False}, 'desc': 'ostentatious'}, 'ack': -1, 'seq': None}
{'action': 'push', 'data': {'content': '{"type":"text","text":"发私信从哪个参数可以分别出来","contentType":0}', 'time': 1682617801300, 'user_id': '492095151452565504', 'channel_id': '492370317524983808', 'message_id': '492389954438041600', 'quote_l1': None, 'quote_l2': None, 'guild_id': None, 'channel_type': 3, 'status': 0, 'nonce': '492387343223754753', 'ctype': 0, 'author': {'nickname': '老哥哥', 'username': '12844776', 'avatar': 'https://fb-cdn.fanbook.mobi/fanbook/app/files/service/headImage/24ad91617e8d01e4288a147f95b5e09f', 'avatar_nft': None, 'bot': False}, 'desc': '发私信从哪个参数可以分别出来'}, 'ack': -1, 'seq': None}'''

def handleWS(user_token):
    version = '1.6.60'
    device_id = f'bot{FANBOOK_CLIENT_ID}'
    header_map = json.dumps({
        "device_id": device_id,
        "version": version,
        "platform": "bot",
        "channel": "office",
        "build_number": "1"
    })
    super_str = base64.b64encode(header_map.encode('utf8')).decode('utf8')
    addr = f'wss://gateway-bot.fanbook.mobi/websocket?id={user_token}&dId={device_id}&v={version}&x-super-properties={super_str}'
    ws = create_connection(addr)

    ping_thread = threading.Thread(target=send_ping, args=(ws,))
    ping_thread.daemon = True
    ping_thread.start()
    try:
        while True:
            evt_data = ws.recv()
            on_message(evt_data)
    except WebSocketConnectionClosedException:
        print("WebSocketClosed")
    except Exception as e:
        print("WebSocketError: ", e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    res = get_me()
    user_token = res["result"]['user_token']
    # pv_res = get_private_chat()
    # if debug: print(f"DEBUG: FANBOOK GOT pv_res: {pv_res}")
    handleWS(user_token)



