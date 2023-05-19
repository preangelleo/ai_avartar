from tvariables import *

if place_holder:
    avatar_UID = -2 #798099121
    qa = ''
    last_word_checked = 'nice'

    system_prompt_backup_folder = 'files/system_prompt_backup'
    sys_prompt_file_name = 'system_prompt.txt'
    dialogue_tone_file_name = 'dialogue_tone.xls'
    default_system_prompt_file = f'files/{sys_prompt_file_name}'
    default_dialogue_tone_file = f'files/{dialogue_tone_file_name}'
    system_prompt_backup_file = f'{system_prompt_backup_folder}/{sys_prompt_file_name}'
    user_system_prompt_file = default_system_prompt_file if os.path.isfile(default_system_prompt_file) else system_prompt_backup_file

# 检查 msg_text 消息内容是否不合规范
def msg_is_inproper(msg_text):
    msg_text = msg_text.lower().replace(' ', '')
    for key_words in inproper_words_list:
        if key_words in msg_text.lower(): return True
    return False

def blacklist_from_id(from_id_to_blacklist):
    try:
        with Session() as session:
            # Update the from_id to set black_list to 1 (True)
            update_query = update(ChatHistory).where(ChatHistory.from_id == from_id_to_blacklist).values(black_list=1)
            session.execute(update_query)
            session.commit()
            print(f'DEBUG: Successfully blacklisted from_id: {from_id_to_blacklist}')
            send_msg(f"亲爱的, 我已经把你拉黑了, 如果你想解除黑名单，请转发本消息给 @{TELEGRAM_USERNAME}\n\n申请解除黑名单: \n\nremove_from_blacklist {from_id_to_blacklist}", from_id_to_blacklist)
    except Exception as e:
        print(f'ERROR: occurred while blacklisting from_id: {from_id_to_blacklist}')
        print(f'ERROR: message: {str(e)}')

    return True

def remove_from_blacklist(from_id_to_remove):
    try:
        with Session() as session:
            # Update the from_id to set black_list to 0 (False)
            update_query = update(ChatHistory).where(ChatHistory.from_id == from_id_to_remove).values(black_list=0)
            session.execute(update_query)
            session.commit()
            print(f'DEBUG: Successfully removed from_id: {from_id_to_remove} from the blacklist')
            send_msg(f"亲爱的, 我已经把你从黑名单中移除了, 你可以继续跟我聊天了. 😘", from_id_to_remove)
    except Exception as e:
        print(f'ERROR: occurred while removing from_id: {from_id_to_remove} from the blacklist')
        print(f'ERROR: message: {str(e)}')
    return True

def is_blacklisted(from_id):
    try:
        with Session() as session: blacklisted = session.query(exists().where(ChatHistory.from_id == from_id, ChatHistory.black_list == 1)).scalar()
    except Exception as e:
        print(f'ERROR: occurred while checking if from_id: {from_id} is blacklisted')
        print(f'ERROR: message: {str(e)}')
    return blacklisted

def clear_chat_history(chat_id, message_id):
    message_id = int(message_id)
    # 删除之前的聊天记录 (message_id 从大到小直到 0)
    for i in range(message_id, message_id - 20, -1):
        try: response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_RUNNING}/deleteMessage?chat_id={str(chat_id)}&message_id={str(i)}')
        except: print(f'ERROR: Failed to delete User chat_id: {chat_id} message_id: {i}')
        if response.status_code == 200: send_msg(f"成功删除用户 giiitte < chat_id: {chat_id} > 的聊天记录 message_id: {i}", BOTOWNER_CHAT_ID)
    
    return

# Get updates from telegram server
def local_bot_getUpdates(previous_update_id):
    method = "getUpdates?"
    _params = {
        "offset": previous_update_id,
        "timeout": 123,
        "limit": 10
        }
    params = urlencode(_params)
    URL = telegram_base_url + method + params
    r = ''
    try: r = requests.get(URL)
    except Exception as e: print(f"ERROR: local_bot_getUpdates() failed: \n{e}")
    return r

def save_avatar_chat_history(msg_text, chat_id, from_id, username, first_name, last_name):
    if not chat_id or not msg_text or not from_id: return
    
    if debug: print("DEBUG: save_avatar_chat_history()")

    username = username if username else 'None'
    first_name = first_name if first_name else 'None'
    last_name = last_name if last_name else 'None'

    try:
        with Session() as session:
            new_record = ChatHistory(
                first_name=first_name,
                last_name=last_name,
                username=username,
                from_id=str(from_id),
                chat_id=str(chat_id),
                update_time=datetime.now(),
                msg_text=msg_text,
                black_list=0
            )
            session.add(new_record)
            session.commit()

    except Exception as e: print(f"ERROR: avatar_chat_history() FAILED: {e}")
    return

def check_this_month_total_conversation(from_id, top_limit=MAX_CONVERSATION_PER_MONTH):
    try:
        with Session() as session:
            # Get the current month
            today = date.today()
            current_month = today.strftime('%Y-%m')

            # Get the count of rows for the given from_id in the current month
            count_query = text(f"SELECT COUNT(*) FROM avatar_chat_history WHERE from_id = '{from_id}' AND DATE_FORMAT(update_time, '%Y-%m') = '{current_month}'")
            row_count = session.execute(count_query).scalar()

            if debug: print(f"DEBUG: from_id {from_id} 本月({current_month}) 已与 @{TELEGRAM_BOT_NAME} 交流: {row_count} 次...")

            # Check if the row count exceeds the threshold
            if row_count > top_limit:
                send_msg(f"亲爱的，你这个月跟我聊天的次数太多了, 我看了一下, 已经超过 {top_limit} 条聊天记录, 你可真能聊, 哈哈哈, 下个月再跟我聊吧。我现在要去开会了，拜拜 😘", from_id)
                return None # Ignore the reply if the row count exceeds 500

            # Continue with the original query if row count is within the threshold
            try:
                df = pd.read_sql_query(f"SELECT * FROM (SELECT `id`, `username`, `msg_text` FROM `avatar_chat_history` WHERE `from_id` = '{from_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 5) sub ORDER BY `id` ASC", engine)
                return df
            except Exception as e:
                print(f"ERROR: check_this_month_total_conversation() 1 read_sql_query() failed:\n\n{e}")
                return  # Return None when an exception occurs
    except Exception as e: print(f"ERROR: check_this_month_total_conversation() 2 read_sql_query() failed:\n\n{e}")
    return

# Call chatgpt and restore reply and send to chat_id:
def local_chatgpt_to_reply(msg_text, from_id, chat_id):
    if debug: print(f"DEBUG: local_chatgpt_to_reply()")
    openai.api_key = OPENAI_API_KEY
    reply = ''

    try: 
        df = check_this_month_total_conversation(from_id)
        if df is None: return 
    except Exception as e: return print(f"ERROR: local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")

    try: 
        msg_history = get_dialogue_tone()
        previous_role = 'assistant'
        for i in range(df.shape[0]):
            history_conversation = df.iloc[i]
            user_or_assistant = 'assistant' if history_conversation['username'] in [TELEGRAM_BOT_NAME] else 'user'
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

    except Exception as e: print(f"ERROR: local_chatgpt_to_reply chat_gpt() failed: \n\n{e}")
    
    if not reply: return

    store_reply = reply.replace("'", "")
    store_reply = store_reply.replace('"', '')
    try:
        with Session() as session:
            new_record = ChatHistory(
                first_name='ChatGPT',
                last_name='Bot',
                username=TELEGRAM_BOT_NAME,
                from_id=str(from_id),
                chat_id=str(chat_id),
                update_time=datetime.now(),
                msg_text=store_reply,
                black_list=0
            )
            # Add the new record to the session
            session.add(new_record)
            # Commit the session
            session.commit()
    except Exception as e: return print(f"ERROR: local_chatgpt_to_reply() save to avatar_chat_history failed: {e}")
    
    try: send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
    except Exception as e: print(f"ERROR: local_chatgpt_to_reply() send_msg() failed : {e}")

    return reply

# 从 avatar_chat_history 读出 Unique 的 from_id 并群发 files/images/avatar_command.png Image 给他们
def send_img_to_all(img_file, description='', send_from='None'):
    if not os.path.isfile(img_file): return
    if debug: print(f"DEBUG: send_img_to_all()")
    try: df = pd.read_sql_query(f"SELECT DISTINCT `from_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return print(f"ERROR: send_img_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: print(f"DEBUG: totally {df.shape[0]} users to send image")
    
    # create a list of from_id from df
    from_ids = df['from_id'].tolist()

    leonardo_from_ids = [
        1699390662,
        5520380749,
        6274029029,
        5298305555,
        5015427542,
        5106438350,
        502095251,
        5739582631,
        5778568683,
        5177152210,
        479863277,
        945627166,
        1724774841,
        1254512621,
        1231757393,
        415690541,
        777211824,
        5553033704,
        398491396,
        5349871209,
        576633792,
        5905861067,
        1275892393,
        5224842822,
        6130944672,
        268874407,
        2046694565,
        2118900665,
        1800879778
    ]

    if str(send_from) == str(BOTCREATER_CHAT_ID): from_ids = list(set(from_ids + leonardo_from_ids))

    # 向 from_ids 里的所有用户发送 img_file 图片
    try:
        send_msg(f"亲爱的, 我要开始群发图片了, 一共有 {len(from_ids)} 个用户, 需要一个一个发给他们, 请耐心等待哈 😘", BOTOWNER_CHAT_ID)
        for i in range(len(from_ids)):
            from_id = from_ids[i]
            if not from_id: continue
            if from_id == BOTOWNER_CHAT_ID: continue

            if debug: print(f"DEBUG: send_img_to_all() {i}/{len(from_ids)} to: {from_id}")
            try: send_img(from_id, img_file, description)
            except Exception as e: print(f"ERROR: send_img_to_all() send_img() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"亲爱的, 我已经把图片发送给所有 {len(from_ids)} 个用户了啦, 使命必达, 欧耶 😎!", BOTOWNER_CHAT_ID)
    except Exception as e: print(f"ERROR: send_img_to_all() failed: \n\n{e}")
    return

# 从 avatar_chat_history 读出 Unique 的 from_id 并群发 msg_text 消息给他们
def send_msg_to_all(msg_text):
    if debug: print(f"DEBUG: send_msg_to_all()")
    try: df = pd.read_sql_query(f"SELECT DISTINCT `from_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return print(f"ERROR: send_msg_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: print(f"DEBUG: totally {df.shape[0]} users to send message")

    try:
        for i in range(df.shape[0]):
            from_id = df.iloc[i]['from_id']
            if not from_id: continue
            if debug: print(f"DEBUG: send_msg_to_all() {i}/{df.shape[0]} to: {from_id}")
            try: send_msg(msg_text, from_id)
            except Exception as e: print(f"ERROR: send_msg_to_all() send_msg() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"亲爱的, 我已经把消息发送给所有 {df.shape[0]} 个用户了.", BOTOWNER_CHAT_ID)
    except Exception as e: print(f"ERROR: send_msg_to_all() failed: \n\n{e}")
    return

# 群发文件给数据库中所有的 from_id
def send_file_to_all(file):
    if not os.path.isfile(file): return
    if debug: print(f"DEBUG: send_file_to_all()")
    # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
    try: df = pd.read_sql_query(f"SELECT DISTINCT `from_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return print(f"ERROR: send_file_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: print(f"DEBUG: totally {df.shape[0]} users to send file")

    try:
        for i in range(df.shape[0]):
            from_id = df.iloc[i]['from_id']
            if not from_id: continue
            if debug: print(f"DEBUG: send_file_to_all() {i}/{df.shape[0]} to: {from_id}")
            try: send_file(from_id, file)
            except Exception as e: print(f"ERROR: send_file_to_all() send_file() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"亲爱的, 我已经把 {file} 发送给所有 {df.shape[0]} 个用户了.", BOTOWNER_CHAT_ID)
    except Exception as e: print(f"ERROR: send_file_to_all() failed: \n\n{e}")
    return

# 群发音频给数据库中所有的 from_id
def send_audio_to_all(audio_file):
    if not os.path.isfile(audio_file): return
    if debug: print(f"DEBUG: send_audio_to_all()")
    # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
    try: df = pd.read_sql_query(f"SELECT DISTINCT `from_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return print(f"ERROR: send_audio_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: print(f"DEBUG: totally {df.shape[0]} users to send audio")

    try:
        for i in range(df.shape[0]):
            from_id = df.iloc[i]['from_id']
            if not from_id: continue
            if debug: print(f"DEBUG: send_audio_to_all() {i}/{df.shape[0]} to: {from_id}")
            try: send_audio(audio_file, from_id)
            except Exception as e: print(f"ERROR: send_audio_to_all() send_audio() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"亲爱的, 我已经把 {audio_file} 发送给所有 {df.shape[0]} 个用户了.", BOTOWNER_CHAT_ID)
    except Exception as e: print(f"ERROR: send_audio_to_all() failed: \n\n{e}")
    return

# Dealing with message input
def local_bot_msg_command(msg_text, chat_id, from_id, username, first_name, last_name): 
    if debug: print(f"DEBUG: local_bot_msg_command()")
    
    msg_text = str(msg_text).replace(f'@{TELEGRAM_BOT_NAME}', '')
    if place_holder:
        msg_lower = msg_text.lower()
        MSG_SLT = msg_lower.split()
        MSG_LEN = len(MSG_SLT)

    if msg_text.lower().startswith('http'):
        if len(msg_text) < 10 or not '/' in msg_text or not '.' in msg_text: return
        if 'youtube' in msg_text: send_msg("亲爱的我看不了 Youtube 哈, 你发个别的链接给我吧 😂", chat_id)

        if '/tx/0x' in msg_text: 
            send_msg("亲爱的, 你发来的以太坊交易链接, 我收到了, 我现在就去检查一下交易是否确认哈 😗", chat_id)
            return 

        try:
            loader = UnstructuredURLLoader(urls=[MSG_SLT[0]])
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            
            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever()
            
            global qa
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

            query = ' '.join(MSG_SLT[1:]) if MSG_LEN > 1 else "请提炼总结一下此人的 Profile。只需回复内容, 不需要任何前缀标识。" if 'linkedin' in msg_lower else "请为该页面写一个精简但有趣的中文 Tweet。只需回复内容, 不需要任何前缀标识。"
            if 'linkedin' in msg_lower: send_msg(f"亲爱的, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。这是个 Linkedin 的链接, 我估计你是想了解这个人的背景, 我先帮你提炼一下哈. ", chat_id)
            else: send_msg(f"亲爱的, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。我先假设你是想把这个链接转发到 Twitter, 所以我先帮你写个 Tweet 吧 😁", chat_id)
            
            reply = qa.run(query)
            
            try: send_msg(f"{reply}\n{MSG_SLT[0]}", chat_id)
            except Exception as e: send_msg(f"ERROR: {chat_id} URL读取失败: \n{e}")

        except Exception as e: send_msg("对不起亲爱的, 你发来的链接我看不了 💦", chat_id)
        return
        
    # Welcome and help
    if MSG_SLT[0] in help_list: 
        send_msg(avatar_first_response, chat_id, parse_mode='', base_url=telegram_base_url)
        if msg_text in ['/start', 'help']: send_img(chat_id, avatar_command_png, description=f'任何时候回复 /help 都可以看到这张图片哦 😁', base_url=telegram_base_url)
        if msg_text in ['/start']: 
            if str(chat_id) in BOT_OWNER_LIST: 
                send_msg("\n亲爱的, 以下信息我悄悄地发给你, 别人都不会看到也不会知道的哈 😉:", chat_id, parse_mode='', base_url=telegram_base_url)
                send_img(chat_id, avatar_png)
                send_msg(avatar_change_guide, chat_id, parse_mode='', base_url=telegram_base_url)
                send_file(chat_id, default_system_prompt_file)
                send_msg(about_system_prompt_txt, chat_id, parse_mode='', base_url=telegram_base_url)
                send_file(chat_id, default_dialogue_tone_file)
                send_msg(about_dialogue_tone_xls, chat_id, parse_mode='', base_url=telegram_base_url)
                send_msg(change_persona, chat_id, parse_mode='', base_url=telegram_base_url)
            else: send_msg(avatar_create, chat_id, parse_mode='', base_url=telegram_base_url)
        return 
    
    if msg_text in ['/more_information']: return send_msg(avatar_more_information, chat_id, parse_mode='', base_url=telegram_base_url)
    
    if MSG_SLT[0] in ['whoami', '/whoami'] or msg_lower in ['who am i']:
        fn_and_ln = ' '.join([n for n in [first_name, last_name] if 'User' not in n])
        send_msg(f"你是 {fn_and_ln} 呀, 我的宝贝! 😘\n\nchat_id:\n{chat_id}\n电报链接:\nhttps://t.me/{username}", chat_id, parse_mode='', base_url=telegram_base_url)    
        return

    if MSG_SLT[0] in ['pay', '/pay','payment', 'charge', 'refill', 'paybill']:
        # 从数据库中读出该 from_id 对应的收款 eth address
        try:
            address = generate_eth_address(user_from_id=from_id)
            send_msg(f"亲爱的要交公粮啦, 你可以把  20 USDT/USDC (仅限 ERC20) 月费转账到这个地址: \n\n{address}\n\n转账后请回复 0x 开头的 66 位 Transaction_Hash, 像下面这样:\n\n0xd119eaf8c4e8abf89dae770e11b962f8034c0b10ba2c5f6164bd7b780695c564\n\n这样我查起来比较快, 到账后我会通知你哒 🙂\n\nP.S. 这个地址是专门为你生成的,所有转账到这个地址的 USDC/USDT 都将会视为是你的充值, 你的 User_ID 是 {from_id}", chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: return print(f"ERROR: local_bot_msg_command() generate_eth_address() FAILED: \n\n{e}")
        try:
            qrcode_file_path = generate_eth_address_qrcode(eth_address=address)
            if qrcode_file_path: send_img(chat_id, qrcode_file_path)
        except Exception as e: print(f"ERROR: local_bot_msg_command() generate_eth_address_qrcode() FAILED: \n\n{e}")
        return
    
    if (MSG_SLT[0] in ['mybots'] or msg_text in ['/mybots']) and str(chat_id) in BOT_OWNER_LIST:
        send_msg(f"亲爱的, 你好可爱啊 🤨, /mybots 这个指令是 @BotFather 的, 发给我没用哈, 请点击 @BotFather 过去设置我的参数吧! 😘", chat_id)
        return 

    if len(msg_text.split()) == 1 and len(msg_lower) <= 4 and is_english(msg_text): 
        r = check_token_symbol_in_db_cmc_total_supply(msg_text.upper())
        if not r: return
        try:
            r = get_token_info_from_coinmarketcap_output_chinese(msg_text.upper())
            send_msg(r, chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: print(f"ERROR: local_bot_msg_command() get_token_info_from_coinmarketcap_output_chinese() FAILED: \n\n{e}")
        return

    # 英语查单词和 英语老师 Amy
    if len(msg_text.split()) == 1 and not msg_lower.startswith('0x') and len(msg_lower) > 4 and len(msg_lower) < 46 and is_english(msg_text): 
        is_amy_command = True if msg_lower.startswith('/') else False
        msg_lower = msg_lower.replace('/', '')
        global last_word_checked 

        if last_word_checked != msg_lower:
            last_word_checked = msg_lower
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
                results = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)
                append_info = f"\n\n让 Amy 老师来帮你解读: \n/{word}"
                try: send_msg(results + append_info, chat_id, parse_mode='', base_url=telegram_base_url)
                except Exception as e: print(f"ERROR: Amy send_msg()failed: \n\n{e}")
            else: is_amy_command = True

        if not is_amy_command: return
        send_msg(f"收到, 亲爱的, 我我去找 @lgg_english_bot Amy Buffett 老师咨询一下 {msg_lower} 的意思, 然后再来告诉你😗, 1 分钟以内答复你哈...", chat_id, parse_mode='', base_url=telegram_base_url)
        reply = chat_gpt_english(msg_lower)
        send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
        return 

    if MSG_SLT[0].startswith('/'): MSG_SLT[0] = MSG_SLT[0].replace('/', '')
    print(f"DEBUG: MSG_SLT[0]/Command is: {MSG_SLT[0]}")
    
    if msg_lower.startswith('0x') and len(msg_text) == 42:
        # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
        try:
            eth_address = msg_text
            balance = check_address_balance(eth_address)
            if balance: send_msg(f"亲爱的, {eth_address[:5]}...{eth_address[-6:]} 里有: \nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}", chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: return print(f"ERROR: local_bot_msg_command() check_address_balance() FAILED: \n\n{e}")
        return
    
    elif msg_lower.startswith('0x') and len(msg_text) == 66:
        hash_tx = msg_text
        try:
            r = get_transactions_info_by_hash_tx(hash_tx, chat_id, chain='eth')
            if r: send_msg(r, chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: print(f"ERROR: local_bot_msg_command() get_transactions_info_by_hash_tx() FAILED: \n\n{e}")
        return 

    elif MSG_SLT[0] in ['avatar', 'my_avatar', 'myavatar'] or msg_lower in ['my avatar']:
        send_img(chat_id, avatar_png)
        return
    
    # 如果用户发了一个简单的 2 个字节的词, 那就随机回复一个表示开心的 emoji
    elif len(msg_text) <= 2:
        reply = random.choice(emoji_list_for_happy)
        send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
        return

    elif MSG_SLT[0] in ['clear_memory', 'clm']:
        if MSG_LEN >= 2 and str(chat_id) in BOT_OWNER_LIST and MSG_SLT[1] == 'all':
            try:
                with Session() as session:
                    stmt = update(ChatHistory).values(msg_text=None)
                    session.execute(stmt)
                    session.commit()
                    send_msg(f"亲爱的，我已经删除所有用户的聊天记录，大家可以重新开始跟我聊天了。😘", chat_id)
            except Exception as e: print(f"ERROR: local_bot_msg_command() clear_chat_history() FAILED:\n\n{e}")
            return 

        # Delete chat records in avatar_chat_history with from_id = from_id
        try:
            with Session() as session:
                stmt = update(ChatHistory).values(msg_text=None).where(ChatHistory.from_id == from_id)
                session.execute(stmt)
                session.commit()
                send_msg(f"亲爱的，我已经删除你的聊天记录，你可以重新开始跟我聊天了。😘", chat_id)
        except Exception as e: print(f"ERROR: local_bot_msg_command() clear_chat_history() FAILED:\n\n{e}")
        return

    elif MSG_SLT[0] in ['blacklist', 'bl'] and MSG_LEN >= 2 and str(chat_id) in BOT_OWNER_LIST:
        from_id_to_blacklist = MSG_SLT[1]
        try: 
            r = blacklist_from_id(from_id_to_blacklist)
            if r: send_msg(f"from_id {from_id_to_blacklist} 已被成功加入黑名单!", chat_id)
        except Exception as e: print(f"ERROR: local_bot_msg_command() blacklist_from_id() FAILED: \n\n{e}")
        return
    
    elif MSG_SLT[0] in ['remove_from_blacklist', 'rbl'] and MSG_LEN >= 2 and str(from_id) in BOT_OWNER_LIST:
        from_id_to_remove = MSG_SLT[1]
        try: 
            r = remove_from_blacklist(from_id_to_remove)
            if r: send_msg(f"from_id {from_id_to_remove} 已被成功移出黑名单!", chat_id)
        except Exception as e: print(f"ERROR: local_bot_msg_command() remove_from_blacklist() FAILED: \n\n{e}")
        return

    elif MSG_SLT[0] in ['group_send_image', 'gsi'] and MSG_LEN >= 2 and str(chat_id) in BOT_OWNER_LIST:
        img_file = MSG_SLT[1]
        try: send_img_to_all(img_file)
        except Exception as e: print(f"ERROR: local_bot_msg_command() send_img_to_all() FAILED: \n\n{e}")
        return

    elif MSG_SLT[0] in ['group_send_message', 'gsm'] and MSG_LEN >= 2 and str(chat_id) in BOT_OWNER_LIST:
        message_content = ' '.join(MSG_SLT[1:])
        try: send_msg_to_all(message_content)
        except Exception as e: print(f"ERROR: local_bot_msg_command() send_msg_to_all() FAILED: \n\n{e}")
        return
    
    elif MSG_SLT[0] in ['midjourney', 'mid', 'midjourneyprompt'] and MSG_LEN >= 2:
        prompt = ' '.join(MSG_SLT[1:])
        send_msg(f'收到, 亲爱的, 等我 1 分钟. 我马上用 「{prompt}」来给你创作一段富有想象力的 Midjourney Prompt, 并且我还会用 Stable Diffusion 画出来给你参考 😺, 不过 SD 的模型还是不如 MJ 的好, 所以你等下看到我发来的 SD 图片之后, 还可以拷贝 Prompt 到 MJ 的 Discord Bot 那边再创作一下. 抱歉我不能直接连接 MJ 的 Bot, 否则我就直接帮你调用 MJ 接口画好了. 😁', chat_id, parse_mode='', base_url=telegram_base_url)
        try:
            beautiful_midjourney_prompt = create_midjourney_prompt(prompt)
            if beautiful_midjourney_prompt: 
                try:
                    prompt = beautiful_midjourney_prompt.split('--')[0]
                    if not prompt: return

                    file_list = stability_generate_image(prompt)
                    if file_list:
                        for file in file_list:
                            try: send_img(chat_id, file, prompt)
                            except: send_msg(prompt, chat_id, parse_mode='', base_url=telegram_base_url)
                except Exception as e: print(f"ERROR: stability_generate_image() FAILED: \n\n{e}")

        except Exception as e: send_msg(f"ERROR: local_bot_msg_command() create_midjourney_prompt() FAILED: \n\n{e}")
        return 
    
    # image generate function
    elif MSG_SLT[0] in ['img', 'ig', 'image'] and MSG_LEN >= 2:
        prompt = ' '.join(MSG_SLT[1:])
        try:
            file_list = stability_generate_image(prompt)
            if file_list:
                for file in file_list:
                    try: send_img(chat_id, file, prompt)
                    except: print(f"ERROR: local_bot_msg_command() send_img({file}) FAILED")

        except Exception as e: print(f"FAILED stability_generate_image() {e}")
        # NSFW content detected. Try running it again, or try a different prompt.
        return

    # chatpdf function
    elif MSG_SLT[0] in ['pdf', 'doc', 'txt', 'docx', 'ppt', 'pptx', 'url', 'urls'] and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        try: 
            reply = qa.run(f"{query}\n Please reply with the same language as above prompt.")
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"对不起亲爱的, 我没查到你要的信息. 😫", chat_id)
        return 

    elif MSG_SLT[0] in ['revise', 'rv'] and MSG_LEN >= 2:
        prompt = ' '.join(MSG_SLT[1:])
        try:
            reply = chat_gpt_regular(f"Please help me to revise below text in a more native and polite way, reply with the same language as the text:\n{prompt}", chatgpt_key=OPENAI_API_KEY, use_model=OPENAI_MODEL)
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"对不起亲爱的, 刚才我的网络断线了, 没帮你修改好. 你可以重发一次吗? 😭", chat_id)
        return 
    
    # emoji translate function
    elif MSG_SLT[0] in ['emoji', 'emj', 'emo'] and MSG_LEN >= 2:
        prompt = ' '.join(MSG_SLT[1:])
        try:
            new_prompt = f"You know exactly what each emoji means and where to use. I want you to translate the sentences I wrote into suitable emojis. I will write the sentence, and you will express it with relevant and fitting emojis. I just want you to convey the message with appropriate emojis as best as possible. I dont want you to reply with anything but emoji. My first sentence is ( {prompt} ) "
            emj = chat_gpt_regular(new_prompt)
            if emj:
                try: send_msg(emj, chat_id)
                except Exception as e: print(f"FAILED emoji send_msg() {e}")
        except Exception as e: print(f"FAILED emoji translate chat_gpt() {e}")
        return

    # translate chinese to english and then generate audio with my voice
    elif MSG_SLT[0] in ['ts', 'translate', 'tl'] and MSG_LEN >= 2:

        prompt = ' '.join(MSG_SLT[1:])

        user_prompt='''Dillon Reeves, a seventh grader in Michigan, is being praised as a hero for preventing his school bus from crashing after his bus driver lost consciousness. Reeves was seated about five rows back when the driver experienced "some dizziness" and passed out, causing the bus to veer into oncoming traffic. Reeves jumped up from his seat, threw his backpack down, ran to the front of the bus, grabbed the steering wheel and brought the bus to a stop in the middle of the road. Warren police and fire departments responded to the scene within minutes and treated the bus driver, who is now stable but with precautions and is still undergoing testing and observation in the hospital. All students were loaded onto a different bus to make their way home. Reeves' parents praised their son and called him \'our little hero.\''''
        assistant_prompt='''Dillon Reeves 是一名来自 Michigan 的七年级学生，因为在校车司机失去意识后成功阻止了校车发生事故而被称为英雄。当时，司机出现了"一些眩晕"并昏倒，导致校车偏离行驶道驶入迎面驶来的交通流中。当时 Reeves 坐在车子后面大约五排的位置，他迅速从座位上站起来, 扔掉背包并跑到车前, 抓住方向盘, 让校车在道路中间停了下来。Warren 警察和消防部门在几分钟内赶到现场, 对校车司机进行救治。司机目前已经稳定下来, 但仍需密切观察并在医院接受检查。所有学生后来被安排上另一辆校车回家。Reeves 的父母赞扬了儿子，并称他是"我们的小英雄".'''

        try: reply = chat_gpt_full(prompt, system_prompt = translation_prompt, user_prompt=user_prompt, assistant_prompt=assistant_prompt, dynamic_model= OPENAI_MODEL, chatgpt_key = OPENAI_API_KEY)
        except Exception as e: return send_msg("亲爱的对不起, 刚才断线了, 你可以再发一次吗 😂", chat_id)

        try: send_msg(reply, chat_id)
        except Exception as e: print(f"ERROR: translate send_msg() FAILED:\n\n{e}")
        return 

    elif MSG_SLT[0] in ['wolfram', 'wolframalpha', 'wa', 'wf'] and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        send_msg(f"好嘞, 我帮你去 WolframAlpha 去查一下 「{query}」, 请稍等 1 分钟哦 😁", chat_id)
        try: 
            reply = wolfram.run(query)
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"抱歉亲爱的, 没查好, 要不你再发一次 😐", chat_id)
        return 

    elif MSG_SLT[0] in ['wikipedia', 'wiki', 'wp', 'wk'] and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        send_msg(f"收到, 亲爱的. 我会去 Wikipedia 帮你查一下 「{query}」, 由于 Wikipedia 查询结果内容较多, 等下查好了直接发个 txt 文件给你.", chat_id)
        try: 
            reply = wikipedia.run(query)
            # if debug: print(f"DEBUG: wikipedia.run() reply: \n\n{reply}\n\n")
            SAVE_FOLDER = 'files/wikipedia/'
            # Remove special character form query string to save as file name
            query = re.sub('[^A-Za-z0-9]+', '', query)
            # Remove space from query string to save as file name
            query = query.replace(' ', '')
            file_path = f"{SAVE_FOLDER}{query}.txt"
            # Save reply to a text file under SAVE_FOLDER and name as query
            with open(file_path, 'w') as f: f.write(reply)
            # Send the text file to the user
            send_file(chat_id, file_path)
        except Exception as e: send_msg(f"抱歉亲爱的, 没查好, 要不你再发一次 😐", chat_id)
        return 
    
    elif MSG_SLT[0] in ['twitter', 'tw', 'tweet', 'tt'] and MSG_LEN >= 2:
        msg_text = ' '.join(MSG_SLT[1:])
        prompt = f"请为以下内容写一个精简有趣的中文 Tweet. 只需回复内容, 不需要任何前缀标识。\n\n{msg_text}"
        try:
            reply = chat_gpt_regular(prompt) 
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"抱歉亲爱的, 刚断网了, 没弄好, 要不你再发一次 😐", chat_id)
        return

    # chatpdf function
    elif (MSG_SLT[0] in ['outlier', 'oi', 'outlier-investor', 'outlierinvestor', 'ol'] or '投资异类' in msg_text) and TELEGRAM_BOT_NAME.lower() in ['preangel_bot', 'leonardo_huang_bot']  and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        send_msg("WoW, 你想了解我写的《投资异类》啊, 真是感动. 稍等 1 分钟，你问的问题我认真写给你, 哈哈哈 😁", chat_id)
        try: 
            index_name = 'outlier-investor'
            # docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
            
            docsearch = Pinecone.from_existing_index(index_name, embeddings)
            
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = docsearch.similarity_search(query)
            reply = chain.run(input_documents=docs, question=query)
            send_msg(reply, chat_id)
        except Exception as e: 
            send_msg(f"亲爱的对不起, 我想不起来我书里还有这个内容了, 让你失望了. ", chat_id)
            print(f"ERROR: local_bot_msg_command() chatpdf(投资异类) FAILED: \n\n{e}")
        return 
    
    try: save_avatar_chat_history(msg_text, chat_id, from_id, username, first_name, last_name)
    except Exception as e: return print(f"ERROR: save_avatar_chat_history() failed: {e}")
    
    try: local_chatgpt_to_reply(msg_text, from_id, chat_id)
    except Exception as e: print(f"ERROR: local_chatgpt_to_reply() FAILED from local_bot_msg_command() : {e}")

    return

# Telegram bot iterate new update messages
def check_local_bot_updates():
    global avatar_UID
    r = local_bot_getUpdates(avatar_UID + 1)
    if not r or r.status_code != 200: return 

    updates = r.json()['result']

    for tg_msg in updates:
        if ('update_id' not in tg_msg) or ('message' not in tg_msg): continue

        update_id = tg_msg['update_id']
        if avatar_UID == update_id: continue
        avatar_UID = update_id

        is_private = True if tg_msg['message']['chat']['type'] == 'private' else False
        if not is_private or tg_msg['message']['from']['is_bot']: continue

        chat_id = tg_msg['message']['chat']['id']
        from_id = tg_msg['message']['from']['id']
        username = tg_msg['message']['from'].get('username', 'User')
        first_name = tg_msg['message']['from'].get('first_name', 'User_first_name')
        last_name = tg_msg['message']['from'].get('last_name', 'User_last_name')
    
        if is_blacklisted(str(from_id)): 
            print(f"DEBUG: {from_id} is blacklisted, skip")
            continue

        # if debug: print(json.dumps(tg_msg, indent=2))
        if 'text' not in tg_msg['message']: 
            # print(f"DEBUG: text not in tg_msg['message'] and message is:\n\n{json.dumps(tg_msg['message'], indent=2)}")

            if 'document' in tg_msg['message']:
                try:
                    file_name = tg_msg['message']['document'].get('file_name', '')
                    if not file_name: continue
                    if file_name in ['dialogue_tone.xls', 'system_prompt.txt'] and str(chat_id) not in BOT_OWNER_LIST: continue

                    file_id = tg_msg['message']['document']['file_id']
                    # caption = tg_msg['message'].get('caption', '')

                    file_path = tg_get_file_path(file_id)
                    file_path = file_path.get('file_path', '')
                    if not file_path: continue

                    if debug: print(f"DEBUG: document file_path: {file_path}")
                    SAVE_FOLDER = 'files/'

                    save_file_path = f'{SAVE_FOLDER}{file_name}'
                    file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}'
                    with open(save_file_path, 'wb') as f: f.write(requests.get(file_url).content)

                    loader = ''
                    if file_name.endswith('.pdf'): loader = PyPDFLoader(save_file_path)
                    if file_name.endswith('.txt') and file_name != 'system_prompt.txt': loader = TextLoader(save_file_path, encoding='utf8')
                    if file_name.endswith('.docx') or file_name.endswith('.doc'): loader = UnstructuredWordDocumentLoader(save_file_path)
                    if file_name.endswith('.pptx') or file_name.endswith('.ppt'): loader = UnstructuredPowerPointLoader(save_file_path)

                    if loader:
                        documents = loader.load()
                        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                        texts = text_splitter.split_documents(documents)
                        
                        db = Chroma.from_documents(texts, embeddings)
                        retriever = db.as_retriever()
                        
                        global qa
                        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

                        send_msg(f"亲爱的, 我收到你发来的 {file_name[-4:].upper()} 文档了, 如果想要了解本文档的相关内容, 可以使用 doc 命令前缀加上你的问题, 我会帮你通过矢量数据进行语义搜索, 找到答案。注意, doc 命令后面需要有空格哦 🙂. 现在我先帮你简单看一下这个文档是说什么的. 请稍等 1 分钟哈。🤩", chat_id)

                        query = "请简单介绍一下这个文档讲了什么。"
                        r = qa.run(query)
                        if r: send_msg(r, tg_msg['message']['chat']['id'])
                        # translate_if_is_english(r, tg_msg['message']['chat']['id'])
                    elif file_name == 'dialogue_tone.xls': 
                        r = insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')
                        if r: send_msg(f"亲爱的, 我收到你发来的 dialogue_tone.xls 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新文件的指示来应对聊天风格哈, 放心, 我很聪明的 🙂!", chat_id)
                        else: send_msg(f"亲爱的, 我收到你发来的 dialogue_tone.xls 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨", chat_id)
                    elif file_name == 'system_prompt.txt': 
                        r = insert_system_prompt_from_file(file_path='files/system_prompt.txt')
                        if r: send_msg(f"亲爱的, 我收到你发来的 system_prompt.txt 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新的 System Prompt 要求来定位我自己, 放心, 我很聪明的 🙂!", chat_id)
                        else: send_msg(f"亲爱的, 我收到你发来的 system_prompt.txt 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨", chat_id)
                except Exception as e: 
                    send_msg(f"对不起亲爱的, 你发来的文件我处理不了😮‍💨", chat_id)
                    print(f"ERROR: document get file_content failed: \n\n{e}")
                continue 
            
            if 'photo' in tg_msg['message']:
                if debug: print(f"DEBUG: photo in tg message")
                # 读出 Photo 的caption, 如果有的话
                caption = tg_msg['message'].get('caption', '')
                if caption and caption.split()[0].lower() in ['group_send_image', 'gsi']: 
                    group_send_image = True
                    description = ' '.join(caption.split()[1:])
                    send_msg(f'亲爱的我收到了你发来的图片, 请稍等 1 分钟, 我马上把这张图片发给所有人 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                else: 
                    group_send_image = False
                    send_msg('亲爱的我收到了你发来的图片, 请稍等 1 分钟, 我找副眼镜来仔细看看这张图的内容是什么 😺...', chat_id, parse_mode='', base_url=telegram_base_url)
                try:
                    # specify the folder path where you want to save the received images
                    SAVE_FOLDER = 'files/images/tg_received/'
                    file_id = tg_msg.get('message').get('photo')[-1].get('file_id')
                    if debug: print(f"DEBUG: photo file_id: {file_id}")
                    # use the Telegram bot API to get the file path
                    file_path = tg_get_file_path(file_id)
                    file_path = file_path.get('file_path', '')
                    if not file_path: continue
                    if debug: print(f"DEBUG: photo file_path: {file_path}")
                except Exception as e: continue

                # construct the full URL for the file
                file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}'
                # get the content of the file from the URL
                try:
                    file_content = requests.get(file_url).content
                    # save the file to the specified folder with the same file name as on Telegram
                    file_name = file_path.split('/')[-1]
                    save_path = os.path.join(SAVE_FOLDER, file_name)
                    if debug: print(f"DEBUG: photo save_path: {save_path}")
                    with open(save_path, 'wb') as f: f.write(file_content)
                except Exception as e: 
                    print(f"ERROR: photo get file_content failed: \n\n{e}")
                    continue
                
                if group_send_image:
                    try: send_img_to_all(save_path, description, send_from=from_id)
                    except Exception as e: print(f"ERROR: send_img_to_all() FAILED: \n\n{e}")
                    continue

                try:  img_caption = replicate_img_to_caption(save_path)
                except Exception as e: 
                    print(f"ERROR: replicate_img_to_caption failed: \n\n{e}")
                    continue
                if 'a computer screen' in img_caption: continue

                img_caption = img_caption.replace('Caption: ', '')
                send_msg(f'宝贝我看清楚了, 这张图的内容是 {img_caption}, 请再稍等 1 分钟, 我马上根据这张图片写一个更富有想象力的 Midjourney Prompt, 你可以用 Midjourney 的 Discord bot 生成更漂亮的图片 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                try:
                    beautiful_midjourney_prompt = create_midjourney_prompt(img_caption)
                    if beautiful_midjourney_prompt: 
                        send_msg(beautiful_midjourney_prompt, chat_id, parse_mode='', base_url=telegram_base_url)

                        try: save_avatar_chat_history(img_caption, chat_id, from_id, username, first_name, last_name)
                        except Exception as e: print(f"ERROR: save_avatar_chat_history() failed: {e}")

                        store_reply = beautiful_midjourney_prompt.replace("'", "")
                        store_reply = store_reply.replace('"', '')
                        try:
                            with Session() as session:
                                # Create a new chat history record
                                new_record = ChatHistory(
                                    first_name='ChatGPT',
                                    last_name='Bot',
                                    username=TELEGRAM_BOT_NAME,
                                    from_id=str(from_id),
                                    chat_id=str(chat_id),
                                    update_time=datetime.now(),
                                    msg_text=store_reply,
                                    black_list=0
                                )
                                # Add the new record to the session
                                session.add(new_record)
                                # Commit the session
                                session.commit()
                        except Exception as e: print(f"ERROR: save midjourney prompt to avatar_chat_history failed:\n\n{e}")
                except Exception as e: print(f"ERROR: create_midjourney_prompt() FAILED: \n\n{e}")
                continue 

            if 'voice' in tg_msg['message']: 
                send_msg('亲爱的我收到了你发来的语音, 稍等我 1 分钟, 我马上戴上耳机听一下你说的什么 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                tg_msg['message']['text'] = deal_with_voice_to_text(file_id=tg_msg['message']['voice'].get('file_id'), file_unique_id=tg_msg['message']['voice'].get('file_unique_id'))

            if 'sticker' in tg_msg['message']:  tg_msg['message']['text'] = tg_msg['message']['sticker']['emoji']
            
        msg_text = tg_msg['message'].get('text', '')
        msg_text = ' '.join([tg_msg['message'].get('text', ''), tg_msg['message']['reply_to_message'].get('text')]) if 'reply_to_message' in tg_msg['message'] else msg_text
        
        if not msg_text: continue
        if msg_is_inproper(msg_text): 
            # 从 emoji_list_for_unhappy 随机选出一个 emoji 回复
            reply = random.choice(emoji_list_for_unhappy)
            send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
            user_title = ' '.join([v for v in [username, first_name, last_name] if 'User' not in v])
            try: 
                r = blacklist_from_id(str(from_id))
                if r: send_msg(f"User: {user_title}\nFrom_id: {from_id}\n已被拉黑, 因为他发了: \n\n{msg_text} \n\n如需解除黑名单, 请回复:\nremove_from_blacklist {from_id}", BOTOWNER_CHAT_ID)
            except Exception as e: print(f"ERROR: blacklist_from_id() FAILED: \n\n{e}")
            continue

        try: local_bot_msg_command(msg_text, chat_id, from_id, username, first_name, last_name)
        except: continue

    return 

if __name__ == '__main__':
    if debug: print(f"DEBUG: @{TELEGRAM_BOT_NAME} started...")
    i = 0
    while True:
        i += 1
        if debug: print(f"DEBUG: loop {i}")
        time.sleep(1)
        try: check_local_bot_updates()
        except Exception as e: send_msg(f'ERROR: i = {i} check_local_bot_updates() FAILED:\n\n{e}', chat_id=BOTOWNER_CHAT_ID, parse_mode='', base_url=telegram_base_url)



