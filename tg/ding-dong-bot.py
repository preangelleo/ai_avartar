"""
Python Wechaty - https://github.com/wechaty/python-wechaty
Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>
2020 @ Copyright Wechaty Contributors <https://github.com/wechaty>
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# https://wechaty.js.org/docs/polyglot/python/ 

import os
import asyncio


from urllib.parse import quote

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

from local_bot import *

# Set the WECHATY_PUPPET environment variable
os.environ['WECHATY_PUPPET'] = 'wechaty-puppet-service'
# Set the WECHATY_PUPPET_SERVICE_TOKEN environment variable
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = os.getenv('PUPPET_PADLOCAL')

'''
    class WechatyChatHistory(Base):
        __tablename__ = 'wechaty_chat_history'

        id = Column(Integer, primary_key=True, autoincrement=True)
        sender_name = Column(String(255))
        sender_id = Column(String(255))
        room_id = Column(String(255))
        message_id = Column(String(255))
        msg_text = Column(Text)
        update_time = Column(DateTime)
        black_list = Column(Integer, default=0)
        '''

# Call chatgpt and restore reply and send to chat_id:
def wechaty_chatgpt_to_reply(msg_text, sender_id, room_id, message_id):
    openai.api_key = OPENAI_API_KEY
    reply = ''

    try: df = pd.read_sql_query(f"SELECT * FROM (SELECT `id`, `sender_name`, `msg_text` FROM `wechaty_chat_history` WHERE `sender_id` = '{sender_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 10) sub ORDER BY `id` ASC", engine)
    except Exception as e: return logging.error(f"wechaty_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")

    try: 
        msg_history = get_dialogue_tone()
        previous_role = 'assistant'
        for i in range(df.shape[0]):
            history_conversation = df.iloc[i]
            user_or_assistant = 'assistant' if history_conversation['sender_name'] in [WECHATY_BOT_NAME] else 'user'
            if user_or_assistant == previous_role: continue
            if i == df.shape[0] - 1 and user_or_assistant == 'user': continue
            if len(history_conversation['msg_text']) > 1200: continue
            need_to_be_appended = {"role": user_or_assistant, "content": history_conversation['msg_text']}
            msg_history.append(need_to_be_appended)
            previous_role = user_or_assistant
        msg_history.append({"role": "user", "content": msg_text})

        response = openai.ChatCompletion.create(
            model = OPENAI_MODEL,
            messages=msg_history
            )
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()

    except Exception as e: logging.error(f"wechaty_chatgpt_to_reply chat_gpt() failed: \n\n{e}")
    return reply

async def generate_img_for_qrcode(qrcode: str, working_folder='files/qrcode'):
    """
    Generate an image for the QR code
    """
    # Create the directory if not exists
    if not os.path.exists(working_folder): os.makedirs(working_folder)
    # Check if the file exists
    file_path = f"{working_folder}/qrcode.png"

    # Generate the QR code
    params = urlencode({'data': qrcode})
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?{params}"
    r = requests.get(qr_code_url)
    # Save the QR code to the file_path
    with open(file_path, 'wb') as f: f.write(r.content)
    return file_path

async def dealing_with_msg_text(msg_text, sender_id, sender_name):

    msg_lower = msg_text.lower()
    MSG_SPLIT = msg_lower.split()
    MSG_LEN = len(MSG_SPLIT)
    reply = ''

    # 如果用户发了一个简单的 2 个字节的词, 那就随机回复一个表示开心的 emoji
    if len(msg_text) <= 2 or msg_text in reply_emoji_list: return random.choice(emoji_list_for_happy)

    if msg_lower in ['whoami', '/whoami', '/wai', '/woshishui', 'woshisui', 'who am i', 'who_am_i', 'wo shi shui', '我是谁', '我是谁?']:
        reply = f"你是 @{sender_name} 呀, 😘\n\nWechat_ID: {sender_id}" 
        return reply
    
    if sender_id == WECHAT_SENDER_ID:
        # /binance_send_crypto
        if MSG_SPLIT[0] in ['binance_send_crypto', '/binance_send_crypto', 'binance_send_coin', '/binance_send_coin', 'binance_send_token', '/binance_send_token', 'bsc', '/bsc', 'bst', '/bst']:
            if MSG_LEN < 5: 
                reply = f"@{sender_name}, 你要从币安提币给别的地址, 请在命令 /binance_send_crypto 后面的空格后再加上一个你要提币的数量, 网络, 币种和地址, 比如: \n\n/binance_send_crypto 10 erc20 usdt 0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377\n\n这样就是把 10 USDT 从币安提币到 0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377 这个地址了。\n\nP.S. /binance_send_crypto 也可以简写为 /bsc 或者 bsc。\n\nCoin 的大小写无所谓, 但是提币费用会从余额里自动扣除, 这里的 amount 数量是到账实际数量哈。"
                return reply
            amount = msg_text.split()[1]
            try: amount = float(amount)
            except: 
                reply = f"@{sender_name}, 命令 /binance_send_crypto 空格后面的第一个参数应该是一个数字, 代表你的提币数量, 你发来的 '{amount}' 并不是一个数字哦。"
                return reply

            network = msg_text.split()[2].upper()
            coin = msg_text.split()[3].upper()
            address = msg_text.split()[4]

            r = binance_withdraw_prep_and_call(amount, network, coin, address)
            confirm_id = r.get('id', None)
            if confirm_id: 
                reply = f"@{sender_name}, 你的提币请求已经提交, 请稍等几分钟后再查询一下提币状态, 提币 ID 是: {confirm_id}"
                return reply
            else: 
                reply = f"@{sender_name}, 你的提币请求提交失败, 错误信息: \n\n{r}"
                return reply

        # /binance_wallet_balance
        elif MSG_SPLIT[0] in ['binance_wallet_balance', '/binance_wallet_balance', 'bwb', '/bwb', '币安现货钱包余额', '币安现货余额', '币安钱包余额', '币安现货账户余额', '币安账户余额']:
            coin = msg_text.split()[1].upper() if MSG_LEN >= 2 else 'ALL'
            if coin == 'ALL':
                return_dict = get_coin_wallet_balance_all()
                dict_to_str = '\n'.join([f"{k}: {format_number(v)}" for k, v in return_dict.items()])
                reply = f"@{sender_name}, 你的币安现货账户余额: \n\n{dict_to_str}"
                return reply
            r = get_coin_wallet_balance(coin)
            reply = f"@{sender_name}, 你的币安现货账户里有: \n\n{format_number(r)} {coin.lower()}"
            return reply
        
        # /binance_funding_balance
        elif MSG_SPLIT[0] in ['binance_funding_balance', '/binance_funding_balance', 'bfb', '/bfb']:
            coin = msg_text.split()[1].upper() if MSG_LEN >= 2 else 'ALL'
            if coin == 'ALL':
                return_dict = get_coin_funding_balance_all()
                dict_to_str = '\n'.join([f"{k}: {format_number(v)}" for k, v in return_dict.items()])
                reply = f"@{sender_name}, 你的币安资金账户余额: \n\n{dict_to_str}"
                return reply
            r = get_coin_funding_balance(coin)
            reply = f"@{sender_name}, 你的币安资金账户里有: \n\n{format_number(r)} {coin.lower()}"
            return reply

    # 查询以太坊地址余额
    if (msg_lower.startswith('0x') and len(msg_text) == 42) or (msg_lower.startswith('/0x') and len(msg_text) == 43):
        msg_text = msg_text.replace('/', '')
        # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
        # 将 msg_text 转换为 CheckSum 格式
        eth_address = Web3.to_checksum_address(msg_text)
        balance = check_address_balance(eth_address)
        reply = f"{user_nick_name}, 你发的 ETH 地址里有: \n\nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}\n\nChecksum Address:\n{eth_address}" if balance else None
        return reply

    # 英语查单词和 英语老师 Amy
    if len(msg_text.split()) == 1 and not msg_lower.startswith('0x') and len(msg_text) > 4 and len(msg_text) < 46 and is_english(msg_text):     
        if not msg_text.startswith('/'):
            word_dict = st_find_ranks_for_word(msg_lower)
            if word_dict:
                word = word_dict.get('word', '')
                word_category = [key.upper() for key, value in word_dict.items() if value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
                word_category_str = ' / '.join(word_category)
                word_trans = {
                    '单词': word,
                    '排名': word_dict.get('rank', ''),
                    '发音': word_dict.get('us-phonetic', ''),
                    '词库': word_category_str,
                    '词意': word_dict.get('chinese', ''),
                }
                reply = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)
                return reply
        else:
            msg_text = msg_text.replace('/', '').lower()
            print(f'英语老师 Amy: {msg_text}')
            reply = chat_gpt_english_explanation(None, msg_text, gpt_model=OPENAI_MODEL)
            return reply

    # 如果用户发来一个英语单词, 小于等于 4 个字符, 那就当做 token symble 处理, 查询 coinmarketcap
    if len(msg_text.split()) == 1 and len(msg_text) <= 4 and is_english(msg_text): 
        msg_text = msg_text.replace('/', '').upper()
        r = check_token_symbol_in_db_cmc_total_supply(msg_text)
        if not r: return
        return get_token_info_from_coinmarketcap_output_chinese(msg_text)
    
    return 


async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    if msg.is_self(): return

    '''
    ['Type', '__annotations__', '__class__', '__class_getitem__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__orig_bases__', '__parameters__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_is_protocol', '_payload', '_puppet', '_wechaty', 'abstract', 'age', 'chatter', 'date', 'find', 'find_all', 'forward', 'get_puppet', 'get_wechaty', 'is_ready', 'is_self', 'load', 'mention_list', 'mention_self', 'mention_text', 'message_id', 'message_type', 'payload', 'puppet', 'ready', 'recall', 'room', 'say', 'set_puppet', 'set_wechaty', 'talker', 'text', 'to', 'to_contact', 'to_file_box', 'to_image', 'to_mini_program', 'to_recalled', 'to_url_link', 'type', 'wechaty']
    '''
    
    if msg.type() == Message.Type.MESSAGE_TYPE_TEXT:

        msg_text = msg.text()
        message_id = str(msg.message_id)
        room_id = None

        room = msg.room()
        if room: 
            is_group_chat = True
            room_id = room.room_id
            print(f'Room ID: {room_id}')
            '''Room ID: 21180830405@chatroom'''
        else: is_group_chat = False

        sender = msg.talker()
        if sender: 
            sender_id = sender.contact_id
            sender_name = sender.name
            mention = f'@{sender_name}'

            '''
            Sender ID: betashow
            Sender Name: 王利杰 Leo
            Mention: @王利杰 Leo
            '''

        if msg_text == 'ding':
            await msg.say('dong dong')
            # file_box = FileBox.from_url(
            #     'https://bellard.org/bpg/2.png',
            #     name='ding-dong-bot.png',
            # )
            # await msg.say(file_box)
            return 
        
        if '王利杰 Leo' in msg_text: send_msg(f"@{sender_name} 在微信上对你说: \n\n{msg_text}", BOTOWNER_CHAT_ID)

        if is_group_chat:
            if WECHATY_BOT_NAME not in msg_text: return
            else: msg_text = msg_text.replace(f'@{WECHATY_BOT_NAME}', '').strip('\n').strip()

        if not msg_text: return

        try:
            r = await dealing_with_msg_text(msg_text, sender_id, sender_name)
            if r: return await msg.say(r)
        except: pass

        r = insert_wechaty_chat_history(sender_name, sender_id, room_id, message_id, msg_text, black_list=0)
        if r: 
            reply = wechaty_chatgpt_to_reply(msg_text, sender_id, room_id, message_id)
            r = insert_wechaty_chat_history(WECHATY_BOT_NAME, sender_id, room_id, message_id, reply, black_list=0)
            if r:
                if not is_group_chat: await msg.say(reply)
                else: await msg.say(f'{mention}\n{reply}')

        return
    
    # elif msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
    #     imageFileBox = await msg.to_file_box()
    #     name = imageFileBox.name
    #     await imageFileBox.to_file('/tmp/' + name)
    #     f = open(name, 'rb')
        
    #     return
    
    # elif msg.type() == Message.Type.MESSAGE_TYPE_VOICE:
    #     voiceFileBox = await msg.to_file_box()
    #     await voiceFileBox.to_file('voice.mp3') # silk to mp3
    #     f = open('voice.mp3', 'rb')
    #     return

    # elif msg.type() == Message.Type.MESSAGE_TYPE_VIDEO:
    #     videoFileBox = await msg.to_file_box()
    #     await videoFileBox.to_file('video.mp4')
    #     return
    # elif msg.type() == Message.Type.MESSAGE_TYPE_EMOTICON:
    #     emoticonFileBox = await msg.to_file_box()
    #     await emoticonFileBox.to_file('emoticon.gif')
    #     return
    

async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + quote(qrcode))
    send_msg(qrcode, BOTOWNER_CHAT_ID)
    file_path = await generate_img_for_qrcode(qrcode)
    send_img(BOTOWNER_CHAT_ID, file_path)


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    # Learn more about services (and TOKEN) from https://wechaty.js.org/docs/puppet-services/
    #
    # It is highly recommanded to use token like [paimon] and [wxwork].
    # Those types of puppet_service are supported natively.
    # https://wechaty.js.org/docs/puppet-services/paimon
    # https://wechaty.js.org/docs/puppet-services/wxwork
    # 
    # Replace your token here and umcommt that line, you can just run this python file successfully!
    # os.environ['token'] = 'puppet_paimon_your_token'
    # os.environ['token'] = 'puppet_wxwork_your_token'
    #     
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
