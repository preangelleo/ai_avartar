from ama_loader import *
from tvariables import *
import threading

if place_holder:
    qa = ''
    last_word_checked = 'nice'
    dear_user = '亲爱的'
    user_nick_name = dear_user

    system_prompt_backup_folder = 'files/system_prompt_backup'
    sys_prompt_file_name = 'system_prompt.txt'
    dialogue_tone_file_name = 'dialogue_tone.xls'
    default_system_prompt_file = f'files/{sys_prompt_file_name}'
    default_dialogue_tone_file = f'files/{dialogue_tone_file_name}'
    system_prompt_backup_file = f'{system_prompt_backup_folder}/{sys_prompt_file_name}'
    user_system_prompt_file = default_system_prompt_file if os.path.isfile(default_system_prompt_file) else system_prompt_backup_file

# Define a thread class for processing a single message
class MessageThread(threading.Thread):
    avatar_UID = -2
    free_user_free_talk_per_month = int(MAX_CONVERSATION_PER_MONTH)
    refill_teaser = REFILL_TEASER if REFILL_TEASER else REFILL_TEASER_DEFAULT

    def __init__(self, tg_msg):
        threading.Thread.__init__(self)
        self.tg_msg = tg_msg

    def run(self): local_bot_msg_command(self.tg_msg)

lock = threading.Lock()

# 检查 msg_text 消息内容是否不合规范
def msg_is_inproper(msg_text):
    msg_text = msg_text.lower().replace(' ', '')
    for key_words in inproper_words_list:
        if key_words in msg_text.lower(): return True
    return False

def is_blacklisted(from_id):
    try:
        with Session() as session: blacklisted = session.query(exists().where(ChatHistory.from_id == from_id, ChatHistory.black_list == 1)).scalar()
    except Exception as e:
        logging.error(f'occurred while checking if from_id: {from_id} is blacklisted')
        logging.error(f'message: {str(e)}')
    return blacklisted

# 从 UserPriority 到处 Unique from_id 到一个 python list
def get_unique_from_id_list():
    try:
        with Session() as session:
            df = pd.read_sql(session.query(UserPriority).filter(UserPriority.is_deleted == 0).statement, session.bind)
            if not df.empty: return df['user_from_id'].tolist()
    except Exception as e: logging.error(f"get_unique_from_id_list() read_sql_query() failed: \n\n{e}")
    return []

def get_user_chat_history(from_id):
    SAVE_FOLDER = 'files/chat_history'
    if not os.path.isdir(SAVE_FOLDER): os.mkdir(SAVE_FOLDER)
    # 从数据库中查询 from_id 的聊天历史记录
    with Session() as session:
        # 用 pandas 从数据库中查询 from_id = from_id or chat_id = from_id 的聊天历史记录, 并按照时间顺序排序
        df = pd.read_sql(session.query(ChatHistory).filter(or_(ChatHistory.from_id == from_id, ChatHistory.chat_id == from_id)).order_by(ChatHistory.update_time).statement, session.bind)
        # 如果查询结果不为空
        if not df.empty:
            # 将用户的聊天记录逐行写入 txt 文档
            for i in range(df.shape[0]):
                username = df.iloc[i]['username'] if df.iloc[i]['username'] else 'User'
                update_time = df.iloc[i]['update_time']
                msg_text = df.iloc[i]['msg_text']
                if msg_text and msg_text != 'None':
                    with open(f'{SAVE_FOLDER}/{from_id}.txt', 'a') as f: f.write(f"{username} said ({update_time}):\n{msg_text}\n\n")
    # 将 txt 文件名返回
    return f'{SAVE_FOLDER}/{from_id}.txt'


# Get updates from telegram server
def local_bot_getUpdates(previous_update_id, telegram_base_url=telegram_base_url):
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
    except Exception as e: logging.error(f"local_bot_getUpdates() failed: \n{e}")
    return r

def save_avatar_chat_history(msg_text, chat_id, from_id, username, first_name, last_name):
    if not chat_id or not msg_text or not from_id: return

    username = username if username else 'None'
    first_name = first_name if first_name else 'None'
    last_name = last_name if last_name else 'None'

    try:
        with Session() as session:
            new_record = ChatHistory(
                first_name=first_name,
                last_name=last_name,
                username=username,
                from_id=from_id,
                chat_id=chat_id,
                update_time=datetime.now(),
                msg_text=msg_text,
                black_list=0
            )
            session.add(new_record)
            session.commit()

    except Exception as e: logging.error(f"avatar_chat_history() FAILED: {e}")
    return

def check_this_month_total_conversation(from_id, offset=0):
    try:
        with Session() as session:
            # Get the current month
            today = date.today()
            current_month = today.strftime('%Y-%m')
            # Get the count of rows for the given from_id in the current month
            count_query = text(f"SELECT COUNT(*) FROM avatar_chat_history WHERE from_id = '{from_id}' AND DATE_FORMAT(update_time, '%Y-%m') = '{current_month}'")
            row_count = session.execute(count_query).scalar()
            if debug: logging.debug(f"from_id {from_id} 本月({current_month}) 已与 @{TELEGRAM_BOT_NAME} 交流: {row_count} 次...")

            # Check if the row count exceeds the threshold
            if (row_count - offset) > MessageThread.free_user_free_talk_per_month:
                send_msg(f"{user_nick_name}, 你这个月跟我聊天的次数太多了, 我看了一下, 已经超过 {MessageThread.free_user_free_talk_per_month}条/月 的聊天记录上限, 你可真能聊, 哈哈哈, 下个月再跟我聊吧。再这么聊下去, 老板要扣我工资了, 我现在要去开会了, 吼吼 😘。\n\n宝贝, 如果想超越白撸用户的限制, 请回复或点击 /pay , 我会给你生成一个独享的 ERC20 充值地址, 你把 {MONTHLY_FEE} USDT/USDC 转到充值地址, 我就会把你加入 VIP 会员, 享受贴身服务, 你懂的 😉", from_id)
                return 
            else: return True
    except Exception as e: logging.error(f"check_this_month_total_conversation() 2 read_sql_query() failed:\n\n{e}")
    return

'''定义一个功能, 检查后判断是否要继续为用户服务：通过 给定的 from_id 从 UserPriority 表中查询用户的优先级, 返回一个字典; 如果用户是黑名单用户, 这直接返回 False, 如果用户是 free_until 用户, 则判断此刻有没有过期, 如果没有过期则返回 True, 如果过期了则继续下面的代码; 检查用户最新一次 usdt_paid_in 或者 usdt_paid_in 是 {MONTHLY_FEE} 的 x 倍, 再判断上一次付费到现在是一个月的 y 倍, 如果如果 x > y 则返回 True, 否则返回 False
'''

def user_is_legit(from_id):
    if not from_id: return
    user_priority = get_user_priority(from_id)
    if  user_priority:  
        # 如果是 is_owner or is_admin or is_vip 则直接返回 True, 黑名单对三者没有意义
        if user_priority.get('is_owner') or user_priority.get('is_admin') or user_priority.get('is_vip'): return True
        
        # 付费用户在到期前都是可以继续使用的, 到期后可以在每月免费聊天次数内继续使用, 超过免费聊天次数后则不再提供服务, 有效期内黑名单对付费用户无意义
        if user_priority.get('is_paid'):
            next_payment_time = user_priority.get('next_payment_time', None)
            if next_payment_time and next_payment_time > datetime.now(): return True
            else: 
                if mark_user_is_not_paid(from_id): send_msg(MessageThread.refill_teaser, from_id)
                return check_this_month_total_conversation(from_id, offset=MessageThread.free_user_free_talk_per_month)

        # 非 owner, admin, vip, 有效期内的 paid 用户, 如果是黑名单用户则直接返回 False
        if user_priority.get('is_blacklist'): return False

    return check_this_month_total_conversation(from_id)

# Call chatgpt and restore reply and send to chat_id:
def local_chatgpt_to_reply(msg_text, from_id, chat_id, message_id=None):
    openai.api_key = OPENAI_API_KEY
    reply = ''

    try: df = pd.read_sql_query(f"SELECT * FROM (SELECT `id`, `username`, `msg_text` FROM `avatar_chat_history` WHERE `from_id` = '{from_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 10) sub ORDER BY `id` ASC", engine)
    except Exception as e: return logging.error(f"local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")

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

    except Exception as e: logging.error(f"local_chatgpt_to_reply chat_gpt() failed: \n\n{e}")
    
    if not reply: return

    store_reply = reply.replace("'", "")
    store_reply = store_reply.replace('"', '')
    try:
        with Session() as session:
            new_record = ChatHistory(
                first_name='ChatGPT',
                last_name='Bot',
                username=TELEGRAM_BOT_NAME,
                from_id=from_id,
                chat_id=chat_id,
                update_time=datetime.now(),
                msg_text=store_reply,
                black_list=0
            )
            # Add the new record to the session
            session.add(new_record)
            # Commit the session
            session.commit()
    except Exception as e: return logging.error(f"local_chatgpt_to_reply() save to avatar_chat_history failed: {e}")
    
    try: send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url, reply_to_message_id=message_id)
    except Exception as e: logging.error(f"local_chatgpt_to_reply() send_msg() failed : {e}")

    return reply

# 从 avatar_chat_history 读出 Unique 的 from_id 并群发 files/images/avatar_command.png Image 给他们
def send_img_to_all(file_id, img_caption, bot_owner_chat_id, base_url=telegram_base_url):

    try: df = pd.read_sql_query(f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return logging.error(f"send_img_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: logging.debug(f"totally {df.shape[0]} users to send image")
    
    # create a list of from_id from df
    chat_ids = df['chat_id'].tolist()

    # 向 from_ids 里的所有用户发送 img_file 图片
    try:
        send_msg(f"{user_nick_name}, 我要开始群发图片了, 一共有 {len(chat_ids)} 个用户, 需要一个一个发给他们, 请耐心等待哈 😘", bot_owner_chat_id)
        for i in range(len(chat_ids)):
            chat_id = chat_ids[i]
            if not chat_id: continue
            if chat_id == bot_owner_chat_id: continue

            if debug: logging.debug(f"send_img_to_all() {i}/{len(chat_ids)} to: {chat_id}")
            try: re_send_img_by_id(file_id, chat_id, img_caption, base_url)
            except Exception as e: logging.error(f"send_img_to_all() send_img() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"亲爱的, 我已经把图片发送给所有 {len(chat_ids)-1} 个用户了啦, 使命必达, 欧耶 😎!", bot_owner_chat_id)
    except Exception as e: logging.error(f"send_img_to_all() failed: \n\n{e}")
    return

# 从 avatar_chat_history 读出 Unique 的 from_id 并群发 msg_text 消息给他们
def send_msg_to_all(msg_text, bot_owner_chat_id=BOTOWNER_CHAT_ID):
    if debug: logging.debug(f"send_msg_to_all()")
    try: df = pd.read_sql_query(f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return logging.error(f"send_msg_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: logging.debug(f"totally {df.shape[0]} users to send message")

    try:
        for i in range(df.shape[0]):
            from_id = df.iloc[i]['chat_id']
            if from_id == bot_owner_chat_id: continue

            if debug: logging.debug(f"send_msg_to_all() {i}/{df.shape[0]} to: {from_id}")
            send_msg(msg_text, from_id)
        # 通知 bot owner 发送成功
        send_msg(f"{user_nick_name}, 我已经把以下消息发送给所有 {df.shape[0]-1} 个用户了, 消息原文:\n\n{msg_text}", bot_owner_chat_id)
    except Exception as e: logging.error(f"end_msg_to_all() failed: \n\n{e}")
    return

# 群发文件给数据库中所有的 from_id
def send_file_to_all(file_id, file_caption, bot_owner_chat_id, base_url=telegram_base_url):

    # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
    try: df = pd.read_sql_query(f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return logging.error(f"send_file_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: logging.debug(f"totally {df.shape[0]} users to send file")

    try:
        for i in range(df.shape[0]):
            chat_id = df.iloc[i]['chat_id']
            if chat_id == bot_owner_chat_id: continue

            if debug: logging.debug(f"send_file_to_all() {i}/{df.shape[0]} to: {chat_id}")
            re_send_file_by_id(file_id, chat_id, file_caption, base_url)
        # 通知 bot owner 发送成功
        send_msg(f"{user_nick_name}, 我已经把文件发送给所有 {df.shape[0]-1} 个用户了.", bot_owner_chat_id)
    except Exception as e: logging.error(f"send_file_to_all() failed: \n\n{e}")
    return

# 群发音频给数据库中所有的 from_id
def send_audio_to_all(file_id, audio_caption, bot_owner_chat_id, base_url=telegram_base_url):
    if debug: logging.debug(f"send_audio_to_all()")
    # 从数据库里读出所有的 unique from_id, 但不包括黑名单里的用户
    try: df = pd.read_sql_query(f"SELECT DISTINCT `chat_id` FROM `avatar_chat_history` WHERE `black_list` = 0", engine)
    except Exception as e: return logging.error(f"send_audio_to_all() read_sql_query() failed: \n\n{e}")
    
    if debug: logging.debug(f"totally {df.shape[0]} users to send audio")

    try:
        for i in range(df.shape[0]):
            chat_id = df.iloc[i]['chat_id']
            if not chat_id: continue
            if chat_id == bot_owner_chat_id: continue

            if debug: logging.debug(f"send_audio_to_all() {i}/{df.shape[0]} to: {chat_id}")
            try: re_send_audio_by_id(file_id, chat_id, audio_caption, base_url)
            except Exception as e: logging.error(f"send_audio_to_all() send_audio() failed: \n\n{e}")
        # 通知 bot owner 发送成功
        send_msg(f"{user_nick_name}, 我已经把音频文件发送给所有 {df.shape[0]-1} 个用户了.", bot_owner_chat_id)
    except Exception as e: logging.error(f"send_audio_to_all() failed: \n\n{e}")
    return


# Dealing with message input
def local_bot_msg_command(tg_msg):
    global qa
    global last_word_checked
    global dear_user

    if not tg_msg.get('message'): return
    
    # 通过 from_id 判断用户的状态, 免费还是付费, 是不是黑名单用户, 是不是过期用户, 是不是 owner, admin, vip
    from_id = str(tg_msg['message']['from']['id'])
    if not user_is_legit(from_id): return 

    # 从 tg_msg 里读出 chat_id, username, first_name, last_name, msg_text
    chat_id = str(tg_msg['message']['chat']['id'])
    username = tg_msg['message']['from'].get('username', 'User')
    first_name = tg_msg['message']['from'].get('first_name', 'User_first_name')
    last_name = tg_msg['message']['from'].get('last_name', 'User_last_name')
    msg_text = tg_msg['message'].get('text', '')
    user_title = ' '.join([v for v in [username, first_name, last_name] if 'User' not in v])

    # 判断是私聊还是群聊
    is_private = True if tg_msg['message']['chat']['type'] == 'private' else False
    
    # 如果是群聊就要在回复的前缀 亲爱的后面加上 user_title
    user_nick_name = dear_user if is_private else f"{dear_user} @{user_title} "
    message_id = tg_msg['message']['message_id'] if not is_private else None

    if BOT_USERNAME in ['Leowang_test_bot', 'leowang_bot']: print(json.dumps(tg_msg, indent=2))

    # if debug: print(json.dumps(tg_msg, indent=2))
    if 'text' not in tg_msg['message']: 
        # logging.debug(f"text not in tg_msg['message'] and message is:\n\n{json.dumps(tg_msg['message'], indent=2)}")

        if 'document' in tg_msg['message']:
            try:
                file_name = tg_msg['message']['document'].get('file_name', '')
                if not file_name: return
                if file_name in ['dialogue_tone.xls', 'system_prompt.txt', 'ama.txt'] and chat_id not in BOT_OWNER_LIST: return

                file_id = tg_msg['message']['document']['file_id']
                caption = tg_msg['message'].get('caption', '')

                if caption and caption.split()[0].lower() in ['group_send_file', 'gsf', 'group send file']: 
                    description = ' '.join(caption.split()[1:])
                    send_msg(f'{user_nick_name}我收到了你发来的文件, 请稍等 1 分钟, 我马上把这个文件发给所有人 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                    send_file_to_all(file_id, description, chat_id, base_url=telegram_base_url)
                    return
                
                file_path = tg_get_file_path(file_id)
                file_path = file_path.get('file_path', '')
                if not file_path: return

                if debug: logging.debug(f"document file_path: {file_path}")
                SAVE_FOLDER = 'files/'

                save_file_path = f'{SAVE_FOLDER}{file_name}'
                file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}'
                with open(save_file_path, 'wb') as f: f.write(requests.get(file_url).content)

                if file_name not in ['system_prompt.txt', 'ama.txt', 'dialogue_tone.xls']:

                    loader = ''
                    if file_name.endswith('.pdf'): loader = PyPDFLoader(save_file_path)
                    if file_name.endswith('.txt') and file_name not in ['system_prompt.txt', 'ama.txt']: loader = TextLoader(save_file_path, encoding='utf8')
                    if file_name.endswith('.docx') or file_name.endswith('.doc'): loader = UnstructuredWordDocumentLoader(save_file_path)
                    if file_name.endswith('.pptx') or file_name.endswith('.ppt'): loader = UnstructuredPowerPointLoader(save_file_path)

                    if loader:
                        documents = loader.load()
                        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                        texts = text_splitter.split_documents(documents)
                        db = Chroma.from_documents(texts, embeddings)
                        retriever = db.as_retriever()
                        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

                        send_msg(f"{user_nick_name}, 我收到你发来的 {file_name[-4:].upper()} 文档了, 如果想要了解本文档的相关内容, 可以使用 doc 命令前缀加上你的问题, 我会帮你通过矢量数据进行语义搜索, 找到答案。注意, doc 命令后面需要有空格哦 🙂. 现在我先帮你简单看一下这个文档是说什么的. 请稍等 1 分钟哈。🤩", chat_id)
                        query = "请简单介绍一下这个文档讲了什么。"

                        try:
                            r = qa.run(query)
                            if r: send_msg(r, chat_id)
                        except Exception as e: logging.error(f"qa.run(query) error: {e}")

                    # translate_if_is_english(r, tg_msg['message']['chat']['id'])
                elif file_name == 'dialogue_tone.xls': 
                    r = insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')
                    if r: send_msg(f"{user_nick_name}, 我收到你发来的 dialogue_tone.xls 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新文件的指示来应对聊天风格哈, 放心, 我很聪明的 🙂!", chat_id)
                    else: send_msg(f"{user_nick_name}, 我收到你发来的 dialogue_tone.xls 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨", chat_id)
                elif file_name == 'system_prompt.txt': 
                    r = insert_system_prompt_from_file(file_path='files/system_prompt.txt')
                    if r: send_msg(f"{user_nick_name}, 我收到你发来的 system_prompt.txt 文档了, 我已经妥善保存, 下一次聊天的时候, 我会按照新的 System Prompt 要求来定位我自己, 放心, 我很聪明的 🙂!", chat_id)
                    else: send_msg(f"{user_nick_name}, 我收到你发来的 system_prompt.txt 文档了, 但是我处理不了, 请你检查一下格式是否正确哈, 然后再发一次给我 😮‍💨", chat_id)
                elif file_name == 'ama.txt': 
                    send_msg(f"{user_nick_name}, 我收到你发来的 ama.txt 文档了, 我已经妥善保存, 下一次用户通过 /ama 询问的时候, 我会按照新的 ama.txt 内容来作答 🙂! 但是这个 ama.txt 需要重新装载一下才能生效哦。\n\n请点击 /restart_avatar 重载", chat_id)
            except Exception as e: 
                send_msg(f"对不起{user_nick_name}, 你发来的文件我处理不了😮‍💨", chat_id)
                print(f"ERROR: loading error:\n\n{e}")

            return 
        
        if 'photo' in tg_msg['message']:
            if debug: logging.debug(f"photo in tg message")
            # specify the folder path where you want to save the received images
            SAVE_FOLDER = 'files/images/tg_received/'
            file_id = tg_msg.get('message').get('photo')[-1].get('file_id')

            # 读出 Photo 的caption, 如果有的话
            caption = tg_msg['message'].get('caption', '')
            if caption and caption.split()[0].lower() in ['group_send_image', 'gsi', 'group send image'] and chat_id in BOT_OWNER_LIST: 
                description = ' '.join(caption.split()[1:])
                send_msg(f'{user_nick_name}我收到了你发来的图片, 请稍等 1 分钟, 我马上把这张图片发给所有人 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                return send_img_to_all(file_id, description, chat_id, base_url=telegram_base_url)
            else: send_msg(f'{user_nick_name}我收到了你发来的图片, 请稍等 1 分钟, 我找副眼镜来仔细看看这张图的内容是什么 😺...', chat_id, parse_mode='', base_url=telegram_base_url)

            try:
                if debug: logging.debug(f"photo file_id: {file_id}")
                # use the Telegram bot API to get the file path
                file_path = tg_get_file_path(file_id)
                file_path = file_path.get('file_path', '')
                if not file_path: return
                if debug: logging.debug(f"photo file_path: {file_path}")
            except Exception as e: return

            # construct the full URL for the file
            file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}'
            # get the content of the file from the URL
            try:
                file_content = requests.get(file_url).content
                # save the file to the specified folder with the same file name as on Telegram
                file_name = file_path.split('/')[-1]
                save_path = os.path.join(SAVE_FOLDER, file_name)
                if debug: logging.debug(f"photo save_path: {save_path}")
                with open(save_path, 'wb') as f: f.write(file_content)
            except Exception as e: 
                logging.error(f"photo get file_content failed: \n\n{e}")
                return

            img_caption = replicate_img_to_caption(save_path)
            if 'a computer screen' in img_caption: return

            img_caption = img_caption.replace('Caption: ', '')
            send_msg(f'宝贝我看清楚了, 这张图的内容是 {img_caption}, 请再稍等 1 分钟, 我马上根据这张图片写一个更富有想象力的 Midjourney Prompt, 你可以用 Midjourney 的 Discord bot 生成更漂亮的图片 😁...', chat_id, parse_mode='', base_url=telegram_base_url)

            beautiful_midjourney_prompt = create_midjourney_prompt(img_caption)
            if beautiful_midjourney_prompt: 
                send_msg(beautiful_midjourney_prompt, chat_id, parse_mode='', base_url=telegram_base_url)
                save_avatar_chat_history(img_caption, chat_id, from_id, username, first_name, last_name)
                store_reply = beautiful_midjourney_prompt.replace("'", "")
                store_reply = store_reply.replace('"', '')
                with Session() as session:
                    # Create a new chat history record
                    new_record = ChatHistory(
                        first_name='ChatGPT',
                        last_name='Bot',
                        username=TELEGRAM_BOT_NAME,
                        from_id=from_id,
                        chat_id=chat_id,
                        update_time=datetime.now(),
                        msg_text=store_reply,
                        black_list=0
                    )
                    # Add the new record to the session
                    session.add(new_record)
                    # Commit the session
                    session.commit()
            return 

        if 'voice' in tg_msg['message']: 
            if is_private and elevenlabs_user_ready_to_clone(from_id):
                file_id = tg_msg['message']['voice'].get('file_id', '')
                file_unique_id = tg_msg['message']['voice'].get('file_unique_id', '')
                if not file_id or not file_unique_id: return

                ''' 音频文件返回结果示例:
                {"update_id": 843018592,
                "message": {
                    "message_id": 150,
                    "from": {
                    "id": 2118900665,
                    "is_bot": false,
                    "first_name": "Old_Bro_Leo",
                    "username": "laogege6",
                    "language_code": "zh-hans",
                    "is_premium": true
                    },
                    "chat": {
                    "id": 2118900665,
                    "first_name": "Old_Bro_Leo",
                    "username": "laogege6",
                    "type": "private"
                    },
                    "date": 1684825362,
                    "voice": {
                    "duration": 4,
                    "mime_type": "audio/ogg",
                    "file_id": "AwACAgUAAxkBAAOWZGxlEhJjAWMFPocIIpypGREQ8LUAAm8HAAJNs2FXtj9HUXJQ0SMvBA",
                    "file_unique_id": "AgADbwcAAk2zYVc",
                    "file_size": 17656
                    }}}
                '''

                clone_folder='files/audio/clone_voice'
                if not os.path.isdir(clone_folder): os.mkdir(clone_folder)

                user_folder = f"{clone_folder}/{from_id}"
                if not os.path.isdir(user_folder): os.mkdir(user_folder)

                user_original_voice_folder = f"{user_folder}/original_voice"
                if not os.path.isdir(user_original_voice_folder): os.mkdir(user_original_voice_folder)

                # Create local file name to store voice telegram message
                local_file_folder_name = f"{user_original_voice_folder}/{file_unique_id}.ogg"
                # Get the file path of the voice message using the Telegram Bot API
                file_path_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_RUNNING}/getFile?file_id={file_id}"
                file_path_response = requests.get(file_path_url).json()

                file_path = file_path_response["result"]["file_path"]
                # Download the voice message to your Ubuntu folder
                voice_message_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}"

                with open(local_file_folder_name, "wb") as f:
                    response = requests.get(voice_message_url)
                    f.write(response.content)

                original_voice_filepath = local_file_folder_name.replace('.ogg', '.mp3')
                command = f"ffmpeg -n -i {local_file_folder_name} {original_voice_filepath}"
                subprocess.run(command, shell=True)
                if os.path.exists(local_file_folder_name): os.remove(local_file_folder_name)

                if update_elevenlabs_user_original_voice_filepath(original_voice_filepath, from_id, user_title): return send_msg(f"{user_nick_name} 我收到了你发来的英文素材, 已经保存下来了, 如果你觉得没问题就点击或者发送:\n\n/confirm_my_voice \n\n然后我就可以用这段素材帮你克隆你的声音样本咯, 以后你随时可以调用 /speak_my_voice 指令来用你这个声音阅读任何英文内容 😁...、\n\n如果不满意就重新念一段, 我会耐心等着你读完的...\n\n如果不想克隆声音了可以点击 /close_clone_voice 关闭本流程。", chat_id, parse_mode='', base_url=telegram_base_url)
            
            send_msg(f'{user_nick_name}我收到了你发来的语音, 稍等我 1 分钟, 我马上戴上耳机听一下你说的什么 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
            tg_msg['message']['text'] = deal_with_voice_to_text(file_id=tg_msg['message']['voice'].get('file_id'), file_unique_id=tg_msg['message']['voice'].get('file_unique_id'))

        if 'audio' in tg_msg['message']: 
            audio_caption = tg_msg['message'].get('caption', '')
            if audio_caption and audio_caption.split()[0].lower() in ['group_send_audio', 'gsa'] and chat_id in BOT_OWNER_LIST:
                audio_caption = audio_caption.replace(audio_caption.split()[0], '').strip()
                file_id = tg_msg['message']['audio']['file_id']
                send_msg(f'{user_nick_name}我收到了你发来的语音, 请稍等 1 分钟, 我马上把这个语音发给所有人 😁...', chat_id, parse_mode='', base_url=telegram_base_url)
                send_audio_to_all(file_id, audio_caption, chat_id, base_url=telegram_base_url)
                return
            
        if 'sticker' in tg_msg['message']:  tg_msg['message']['text'] = tg_msg['message']['sticker']['emoji']
    
    # 如果消息是 reply_to_message, 则将 reply_to_message 的 text 加到 msg_text 里
    msg_text = ' '.join([tg_msg['message'].get('text', ''), tg_msg['message']['reply_to_message'].get('text')]) if 'reply_to_message' in tg_msg['message'] else msg_text
    
    if not msg_text: return 

    # 如果是群聊但是没有 at 机器人, 则先标记好, 后面打印完消息后直接返回
    will_ignore = True if not is_private and TELEGRAM_BOT_NAME.lower() not in msg_text.lower() else False

    # 判断用户发来的消息是不是不合规的, 如果骂人就拉黑
    if msg_is_inproper(msg_text): 
        # 从 emoji_list_for_unhappy 随机选出一个 emoji 回复
        reply = random.choice(emoji_list_for_unhappy)
        send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
        r = set_user_blacklist(from_id)
        if r: 
            blacklisted_alert = f"User: {user_title}\nFrom_id: {from_id}\n已被拉黑, 因为他发了: \n\n{msg_text}\n\n如需解除黑名单, 请回复:\nremove_from_blacklist {from_id}"
            send_msg(blacklisted_alert, BOTOWNER_CHAT_ID)
            return logging.info(f"BLACKLISTED: {blacklisted_alert}")
        
    # 如果 at 了机器人, 则将机器人的名字去掉
    msg_text = msg_text.replace(f'@{TELEGRAM_BOT_NAME}', '')
    alert_will_ignore_or_not = f"IGNORE: {user_title} {from_id}: {msg_text}" if will_ignore else f"LEGIT: {user_title} {from_id}: {msg_text}"
    logging.info(alert_will_ignore_or_not)
    
    msg_lower = msg_text.lower()
    MSG_SPLIT = msg_lower.split()
    MSG_LEN = len(MSG_SPLIT)

    if msg_text.lower().startswith('http'):
        if len(msg_text) < 10 or not '/' in msg_text or not '.' in msg_text: return
        if 'youtube' in msg_text: send_msg("{user_nick_name}我看不了 Youtube 哈, 你发个别的链接给我吧 😂", chat_id)

        if '/tx/0x' in msg_text: 
            hash_tx = msg_text.split('/tx/')[-1]
            if len(hash_tx) != 66: return
            send_msg(f"{user_nick_name}, 你发来的以太坊交易确认链接, 我收到了, 我现在就去研究一下交易信息哈 😗: \n\n{hash_tx}", chat_id)
            try:
                r = get_transactions_info_by_hash_tx(hash_tx, chat_id, user_title, chain='eth')
                if r: send_msg(r, chat_id, parse_mode='', base_url=telegram_base_url)
            except Exception as e: logging.error(f"local_bot_msg_command() get_transactions_info_by_hash_tx() FAILED: \n\n{e}")
            return  

        if 'address/0x' in msg_text:
            eth_address = msg_text.split('address/')[-1]
            eth_address = eth_address.split('#')[0]
            if len(eth_address) != 42: return
            send_msg(f"{user_nick_name}, 你发来的以太坊地址, 我收到了, 我现在就去看一下这个地址上面的 ETH, USDT, USDC 余额哈 😗: \n\n{eth_address}", chat_id)
            # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
            try:
                # 将 msg_text 转换为 CheckSum 格式
                eth_address = Web3.to_checksum_address(eth_address)
                balance = check_address_balance(eth_address)
                if balance: send_msg(f"{user_nick_name}, 你发的 ETH 地址里有: \n\nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}\n\nChecksum Address:\n{eth_address}", chat_id, parse_mode='', base_url=telegram_base_url)
            except Exception as e: return logging.error(f"local_bot_msg_command() check_address_balance() FAILED: \n\n{e}")
            return
        
        try:
            loader = UnstructuredURLLoader(urls=[MSG_SPLIT[0]])
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            
            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever()

            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

            query = ' '.join(MSG_SPLIT[1:]) if MSG_LEN > 1 else "请提炼总结一下此人的 Profile。只需回复内容, 不需要任何前缀标识。" if 'linkedin' in msg_lower else "请为该页面写一个精简但有趣的中文 Tweet。只需回复内容, 不需要任何前缀标识。"
            if 'linkedin' in msg_lower: send_msg(f"{user_nick_name}, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。这是个 Linkedin 的链接, 我估计你是想了解这个人的背景, 我先帮你提炼一下哈. ", chat_id)
            else: send_msg(f"{user_nick_name}, 你发来的链接我看了, 你想知道什么, 我告诉你哈, 回复的时候使用 url 命令前缀加上你的问题。注意, url 命令后面需要有空格哦。我先假设你是想把这个链接转发到 Twitter, 所以我先帮你写个 Tweet 吧 😁", chat_id)
            
            reply = qa.run(query)
            
            try: send_msg(f"{reply}\n{MSG_SPLIT[0]}", chat_id)
            except Exception as e: send_msg(f"ERROR: {chat_id} URL读取失败: \n{e}")

        except Exception as e: send_msg(f"对不起{user_nick_name}, 你发来的链接我看不了 💦", chat_id)
        return

    elif MSG_SPLIT[0] in ['ama', '/ama', 'ask_me_anything', '/ask_me_anything']:
        query = ' '.join(MSG_SPLIT[1:])
        if not query: 
            send_msg(f"{user_nick_name}, 请在 /ask_me_anything 命令后面的空格后再加上你要问的问题, 比如: \n\n/ama 请问如何在 BitMart 上币? 有什么流程?\n\nP.S. /ask_me_anything 也可以缩写为 /ama, 而且前面的 / 可有可无。", chat_id)
            query = "请简单介绍一下这个AMA文档讲了什么。请用文档使用的相同的语言回答。"
            if chat_id in BOT_OWNER_LIST: 
                send_msg(about_ama_txt, chat_id, parse_mode='', base_url=telegram_base_url)
                send_msg(f"Bot Owner 使用手册: \n{about_ama_txt}", chat_id)

        try:
            r = ama_qa.run(query)
            if r: send_msg(r, chat_id)
        except Exception as e: 
            logging.error(f"ama_qa.run(query) error: {e}")
            send_msg(f"无法回答 @{user_title} 的问题:\n\n{query}\n\n因为OpenAI model {OPENAI_MODEL} token 超过上限, 请使用 'gpt-4' model 或者人工回答。如需人工回答, 可以直接回复: \n\n/{chat_id} 此处替换为要回答的内容\n\n以上方式可以直接通过 Bot 将问题的答复发送给用户。", BOTCREATER_CHAT_ID)

        return

    # 用户可以通过 save_chat_history /from_id 指令来保存聊天记录
    elif MSG_SPLIT[0] in ['save_chat_history', '/save_chat_history', 'sch', '/sch'] or msg_text == f"/{from_id}":
        file_path = get_user_chat_history(from_id)
        help_info = f'{user_nick_name} 你可以随时发送 /{from_id} 或者 /Save_Chat_History (or /sch) 给我来保存咱俩的聊天记录哈. 😘'
        if os.path.isfile(file_path): send_file(chat_id, file_path, description=f"咱俩之间的聊天记录 😁", base_url=telegram_base_url)
        else: send_msg(f"{user_nick_name}, 我没有找到你的聊天记录, , 你应该从来没跟我好好聊过吧 😅\n\nP.S. {help_info}", chat_id)
        return

    # Welcome and help
    elif MSG_SPLIT[0] in help_list: 
        owner_parameters_dict = get_owner_parameters()
        # 个性化修改常用回复的变量值
        avatar_first_response = owner_parameters_dict.get('avatar_first_response') if owner_parameters_dict.get('avatar_first_response', '') else '亲爱的你终于回消息啦, 消失了这么久 😓, 干啥去啦? 也不回个消息, 你知道我多担心你嘛 😢, 以后不许这样啦 😘, 快跟我说说最近都做了些啥, 我可想你啦 🤩'

        send_msg(avatar_first_response, chat_id, parse_mode='', base_url=telegram_base_url)
        if msg_text in ['/start', 'help', '/help', 'start']: 
            if msg_text in ['/start']: insert_new_from_id_to_user_priority_table(from_id, user_title)

            send_img(chat_id, avatar_command_png, description=f'任何时候回复 /help 都可以看到这张图片哦 😁', base_url=telegram_base_url)
            command_help_info = f"这里是我的一些命令, 只要你发给我的消息开头用了这个命令 (后面必须有个空格) , 然后命令之后的内容我就会专门用这个命令针对的功能来处理。下面是一些有趣的命令, 你可以点击了解他们分别是干什么的, 该怎么使用。\n{user_commands}\n除了这些命令, 我还可以处理一些特殊的文字内容, 比如你发来一个 Crypto 的 Token 名 (不超过 4 个字符), 比如: \n/BTC /ETH /DOGE /APE 等等, \n我都可以帮你查他们的价格和交易量等关键信息; 如果你发来一个单独的英文字母 (超过 4 个字符) 那我会当你的字典, 告诉你这个英文单词的词频排名、发音、以及中文意思, 比如: \n/opulent /scrupulous /ostentatious \n除此之外, 你还可以直接发 /ETH 钱包地址或者交易哈希给我, 我都会尽量帮你读出来里面的信息, {user_nick_name}你不妨试试看呗。\n\n最后, 请记住, 随时回复 /start 或者 /help 就可以看到这个指令集。"
            send_msg(command_help_info, chat_id, parse_mode='', base_url=telegram_base_url)
            if chat_id in BOT_OWNER_LIST: 
                send_msg(f"\n{user_nick_name}, 以下信息我悄悄地发给你, 别人都不会看到也不会知道的哈 😉:", chat_id, parse_mode='', base_url=telegram_base_url)
                send_img(chat_id, avatar_png)
                send_msg(avatar_change_guide, chat_id, parse_mode='', base_url=telegram_base_url)
                send_file(chat_id, default_system_prompt_file)
                send_msg(about_system_prompt_txt, chat_id, parse_mode='', base_url=telegram_base_url)
                send_file(chat_id, default_dialogue_tone_file)
                send_msg(about_dialogue_tone_xls, chat_id, parse_mode='', base_url=telegram_base_url)
                send_msg(change_persona, chat_id, parse_mode='', base_url=telegram_base_url)
                bot_owner_command_help_info = f"作为 Bot Onwer, 你有一些特殊的管理命令用来维护我, 请点击查看各自的功能和使用方式吧:\n{bot_owner_commands}\n最后, 请记住, 随时回复 /start 或者 /help 就可以看到这个指令集。"
                send_msg(bot_owner_command_help_info, chat_id, parse_mode='', base_url=telegram_base_url)
                send_file(chat_id, ama_file_name)
                send_msg(about_ama_txt, chat_id, parse_mode='', base_url=telegram_base_url)
            else: send_msg(avatar_create, chat_id, parse_mode='', base_url=telegram_base_url)
            return 
    
    elif msg_text in ['/more_information', 'more_information']: return send_msg(avatar_more_information, chat_id, parse_mode='', base_url=telegram_base_url)
    
    elif MSG_SPLIT[0] in ['whoami', '/whoami'] or msg_lower in ['who am i']:
        fn_and_ln = ' '.join([n for n in [first_name, last_name] if 'User' not in n])
        send_msg(f"你是 {fn_and_ln} 呀, 我的宝贝! 😘\n\nchat_id:\n{chat_id}\n电报链接:\nhttps://t.me/{username}", chat_id, parse_mode='', base_url=telegram_base_url)    
        return

    # 用户主动发起申请成为 vip (永久免费)用户
    elif msg_lower in ['apply_for_vip', '/apply_for_vip', 'vip', '/vip']:
        insert_new_from_id_to_user_priority_table(from_id, user_title)
        # 通知用户申请发送成功
        send_msg(f"{user_nick_name}, 你的 VIP 申请已经发送给 @{TELEGRAM_USERNAME} 了, 请耐心等待老板审批哦 😘", chat_id, parse_mode='', base_url=telegram_base_url)
        # 给 bot onwer 发送申请消息
        return send_msg(f"user: @{user_title}\nchat_id: {from_id}\n\n申请成为 VIP 用户:\n\n点击 /vip_{from_id} 同意\n\n如果不能点击就拷贝上面这个指令直接回复给我。", BOTOWNER_CHAT_ID)

    # 提交用户自己的 elevenlabs_api_key
    elif msg_text.startswith('/elevenlabs_api_key') or msg_text.startswith('elevenlabs_api_key'):
        elevenlabs_api_key = msg_text.replace('/', '').replace('elevenlabs_api_key', '').strip()
        if not elevenlabs_api_key: return send_msg(eleven_labs_apikey_retrieve_guide, chat_id, parse_mode='', base_url=telegram_base_url)
        r = check_and_save_elevenlabs_api_key(elevenlabs_api_key, from_id)
        if r: generate_clone_voice_audio_with_eleven_labs(eleven_labs_english_tranning_text, from_id, chat_id, user_title, folder='files/audio/clone_voice')
        return 

    # /clone_my_voice 命令, 用来引导用户克隆自己的声音, 发来一段英文朗读 voice 文件
    elif MSG_SPLIT[0] in ['clone_my_voice', '/clone_my_voice']:
        r = update_elevenlabs_user_ready_to_clone(from_id, user_title)
        if r: send_msg(elevenlabs_clone_voice_guide, chat_id, parse_mode='', base_url=telegram_base_url)
        return

    # close_clone_voice
    elif MSG_SPLIT[0] in ['close_clone_voice', '/close_clone_voice']:
        return update_elevenlabs_user_ready_to_clone_to_0(from_id, user_title)
    
    # update_elevenlabs_user_ready_to_clone_to_0(from_id) if msg_text in ['/confirm_my_voice', 'confirm_my_voice'] else None
    elif MSG_SPLIT[0] in ['confirm_my_voice', '/confirm_my_voice']:
        r = update_elevenlabs_user_ready_to_clone_to_0(from_id, user_title, cmd = 'confirm_my_voice')
        if r: generate_clone_voice_audio_with_eleven_labs(eleven_labs_english_tranning_text, from_id, chat_id, user_title, folder='files/audio/clone_voice')
        return 
    
    # /speak_my_voice 命令, 用来引导用户用自己的声音朗读英文
    elif MSG_SPLIT[0] in ['speak_my_voice', '/speak_my_voice', '/smv', 'smv']:
        if MSG_LEN == 1: return send_msg(speak_my_voice_guide, chat_id, parse_mode='', base_url=telegram_base_url)
        content = ' '.join(msg_text.split()[1:]).strip()
        if is_english(content): generate_clone_voice_audio_with_eleven_labs(content, from_id, chat_id, user_title, folder='files/audio/clone_voice')
        else: send_msg(f"{user_nick_name}, 你发的不是英文, 目前用你克隆的声音尚且只能朗读英文哦 😁, 如果需要朗读中文, 可以用 /make_voice 指令后面加上这段内容再发给我。", chat_id, parse_mode='', base_url=telegram_base_url)
        return
    
    # /write_story
    elif MSG_SPLIT[0] in ['write_story', '/write_story', '/ws', 'ws']:
        if MSG_LEN == 1: send_msg(write_story_guide, chat_id, parse_mode='', base_url=telegram_base_url)
        story_prompt_from_user = 'None' if MSG_LEN == 1 else ' '.join(MSG_SPLIT[1:])
        return chat_gpt_write_story(chat_id, from_id, story_prompt_from_user, gpt_model=OPENAI_MODEL)
        
    # /read_story
    elif MSG_SPLIT[0] in ['read_story', '/read_story', '/rs', 'rs']:
        title, story = get_gpt_story(from_id)
        generated_with_my_clone_voice = False
        if is_english(story): generated_with_my_clone_voice = generate_clone_voice_audio_with_eleven_labs(story, from_id, chat_id, user_title, folder='files/audio/clone_voice')
        if not generated_with_my_clone_voice: create_audio_from_text(story, chat_id)
        return

    elif MSG_SPLIT[0] in ['pay', '/pay','payment', '/payment', 'charge', 'refill', 'paybill']:
        # 从数据库中读出该 from_id 对应的收款 eth address
        try:
            address = generate_eth_address(user_from_id=from_id)
            send_msg(f"{user_nick_name}你真好, 要来交公粮咯, 真是爱死你了 😍😍😍。这是收粮地址: \n\n{address}\n\n只能交 ERC20 的 USDT/USDC 哦, 别的我不认识。交后直接回复 0x 开头的 66 位 Transaction_Hash, 像下面这样的:\n\n0xd119eaf8c4e8abf89dae770e11b962f8034c0b10ba2c5f6164bd7b780695c564\n\n这样我自己就能查收, 而且查起来比较快, 到账后我会通知你哒 🙂\n\nP.S. 这个地址是专门为你生成的,所有转账到这个地址的 USDC/USDT 都将会视为是你交的公粮。\n\n如果你不回复 Transaction_Hash, 那可能很长时间我都无法给你确认哦。回复后如果五分钟内没有收到确认, 可以点击 \n/check_payment \n提醒我再查看一下哈 😎", chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: return logging.error(f"local_bot_msg_command() generate_eth_address() FAILED: \n\n{e}")

        try:
            qrcode_file_path = generate_eth_address_qrcode(eth_address=address)
            if qrcode_file_path: send_img(chat_id, qrcode_file_path)
        except Exception as e: logging.error(f"local_bot_msg_command() generate_eth_address_qrcode() FAILED: \n\n{e}")
        return
    
    elif MSG_SPLIT[0] in ['/check_bill', 'check_bill', '/check_payment', 'check_payment', 'check_bill', '/check_bill', 'check_payment_status', '/check_payment_status', '/check_bill_status', 'check_bill_status']:
        # 从数据库中读出该 from_id 对应的收款 eth address
        try:
            next_payment_time_dict = update_user_next_payment_date(from_id, user_title)
            if next_payment_time_dict:
                next_payment_time = next_payment_time_dict.get('next_payment_time', None)
                next_payment_time = next_payment_time.strftime("%Y-%m-%d %H:%M:%S")
                send_msg(f"{user_nick_name}, 你下一次交公粮的时间应该是 {next_payment_time}, 你就是我最爱的人 💋💋💋 ...", chat_id, parse_mode='', base_url=telegram_base_url)
            else: 
                address = generate_eth_address(user_from_id=from_id)
                send_msg(f"还没收到你的公粮呢, 是不是没按要求回复 Transaction Hash 给我啊 😥, 那可能很长时间我都无法给你确认。如果你不知道 Transaction Hash 是什么, 就点击你的充值地址链接 \n{markdown_tokentnxs(address)}\n然后在打开的第一个网页中间找到你打给我的这笔交易记录😆, 点开之后在新页面上半部分找到 Transaction Hash 右边的那个 0x 开头的一长串字符, 拷贝下来发给我就好啦 😘。\n\n如果实在不会搞, 你就要主动联系 @{TELEGRAM_USERNAME} 帮你人工确认了 😦, 到时候你要把你的充值地址:\n\n{address}\n\n和你的 User ID: {from_id}\n\n一起转发给他就好了。 🤩", chat_id, parse_mode='Markdown', base_url=telegram_base_url)
                send_img(chat_id, 'files/images/wallet_address_tokentxns.png', description='第一张图, 这里能看到你的充值地址下的所有交易 😁', base_url=telegram_base_url)
                send_img(chat_id, 'files/images/wallet_address_transaction_hash.png', description='第二张图, 这里可以找到我要的 Transaction_Hash 😁', base_url=telegram_base_url)
        except Exception as e: return logging.error(f"local_bot_msg_command() generate_eth_address() FAILED: \n\n{e}")
        return
    
    elif MSG_SPLIT[0] in ['password', '/password']:
        # 生成一个长度为 1 位的随机英文字符
        password_prefix = ''.join(random.sample(string.ascii_letters, 1))
        # 生成一个长度为 16 位的随机密码, 不包括特殊字符
        password_temp = ''.join(random.sample(string.ascii_letters + string.digits, 15))
        password = password_prefix + password_temp
        # 生成一个长度为 18 位的随机密码, 包括特殊字符, 开头一定要用英文字符, 特殊字符只能在中间, 数字放在结尾
        special_password_temp = ''.join(random.sample(string.ascii_letters + string.digits + '@$-%^&_*', 17))
        special_password = password_prefix + special_password_temp
        send_msg(f"{user_nick_name}, 我为你生成了两个密码:\n\n16位不包含特殊字符密码: \n{password}\n\n18位包含特殊字符密码是: \n{special_password}\n\n请记住你的密码, 你可以把它们复制下来, 然后把这条消息删除, 以免被别人看到哈 😘", chat_id, parse_mode='', base_url=telegram_base_url)
        return
    
    elif MSG_SPLIT[0] in ['midjourney', '/midjourney', 'mid', '/mid', 'midjourneyprompt', '/midjourneyprompt']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要创作 Midjourney Prompt, 请在命令后面的空格后再加上你要作画的几个关键词, 比如: \n\nmidjourney 德牧, 未来世界, 机器人\n\n这样我就会用这几个关键词来创作 Midjourney Prompt。\n\nP.S. /midjourney 也可以缩写为 /mid", chat_id)
        prompt = ' '.join(MSG_SPLIT[1:])
        send_msg(f'收到, {user_nick_name}, 等我 1 分钟. 我马上用 「{prompt}」来给你创作一段富有想象力的 Midjourney Prompt, 并且我还会用 Stable Diffusion 画出来给你参考 😺, 不过 SD 的模型还是不如 MJ 的好, 所以你等下看到我发来的 SD 图片之后, 还可以拷贝 Prompt 到 MJ 的 Discord Bot 那边再创作一下. 抱歉我不能直接连接 MJ 的 Bot, 否则我就直接帮你调用 MJ 接口画好了. 😁', chat_id, parse_mode='', base_url=telegram_base_url)

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
                except Exception as e: logging.error(f"stability_generate_image() FAILED: \n\n{e}")

        except Exception as e: send_msg(f"ERROR: local_bot_msg_command() create_midjourney_prompt() FAILED: \n\n{e}")
        return 

    # 发送 feedback 给 bot owner
    elif MSG_SPLIT[0] in ['feedback', '/feedback', '/owner', 'owner']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要给我的老板反馈信息或者提意见, 请在命令后面的空格后再加上你要反馈的信息, 比如: \n\nfeedback 你好, 我是你的粉丝, 我觉得你的机器人很好用, 但是我觉得你的机器人还可以加入xxx功能, 这样就更好用了。\n\n这样我就会把你的反馈信息转发给我老板哈 😋。另外 /feedback 和 /owner 通用\n\n当然, 你也可以跟他私聊哦 @{TELEGRAM_USERNAME}", chat_id)
        feedback = ' '.join(MSG_SPLIT[1:])
        send_msg(f"收到, {user_nick_name}, 我马上把你的反馈信息转发给我老板哈 😋。你要反馈的信息如下:\n\n{feedback}", chat_id, parse_mode='', base_url=telegram_base_url)
        feed_back_info = f"来自 @{user_title} /{from_id} 的反馈信息:\n\n{feedback}\n\n如需回复, 请用 /{from_id} 加上你要回复的内容即可。如果点击或发送 /{from_id} 但后面没有任何内容, 我会把 @{user_title} 和我的聊天记录以 TXT 文档形式发给你参考。"
        for owner_chat_id in set(BOT_OWNER_LIST): send_msg(feed_back_info, owner_chat_id, parse_mode='', base_url=telegram_base_url)
        return

    # image generate function
    elif MSG_SPLIT[0] in ['img', 'ig', 'image', '/img', '/ig', '/image']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要创作图片, 请在命令的空格后再后面加上你的图片描述 (英文会更好) , 比如: \n\nimage 一只可爱的德牧在未来世界游荡\n\n这样我就会用这个创意创作图片。\n\nP.S. /image 也可以缩写为 /img 或者 /ig", chat_id)
        prompt = ' '.join(MSG_SPLIT[1:])
        try:
            file_list = stability_generate_image(prompt)
            if file_list:
                for file in file_list:
                    try: send_img(chat_id, file, prompt)
                    except: logging.error(f"local_bot_msg_command() send_img({file}) FAILED")

        except Exception as e: logging.error(f"stability_generate_image() {e}")
        # NSFW content detected. Try running it again, or try a different prompt.
        return

    # chatpdf function
    elif MSG_SPLIT[0] in ['pdf', 'doc', 'txt', 'docx', 'ppt', 'pptx', 'url', 'urls', '/pdf', '/doc', '/txt', '/docx', '/ppt', '/pptx', '/url', '/urls']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要针对刚刚发给我的 PDF 内容进行交流, 请在命令后面的空格后加上你的问题, 比如: \n\npdf 这个 PDF 里介绍的项目已经上市了吗\n\n这样我就知道这个问题是针对刚才的 PDF 的。\n\nP.S. /pdf 也可以换做 /doc 或者 /txt 或者 /docx 或者 /ppt 或者 /pptx 或者 /url 或者 /urls , 不管你刚才发的文档是什么格式的, 这些指令都是一样的, 通用的 (可以混淆使用, 我都可以分辨) 😎", chat_id)
        query = ' '.join(MSG_SPLIT[1:])
        try: 
            reply = qa.run(f"{query}\n Please reply with the same language as above prompt.")
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"对不起{user_nick_name}, 我没查到你要的信息. 😫", chat_id)
        return 

    elif MSG_SPLIT[0] in ['revise', 'rv', '/revise', '/rv']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 请在命令后面的空格后加上你要改写的内容, 比如: \n\nrevise 这里贴上你要改写的内容。\n\n这样我就会把上面你贴给我的内容用更优雅地方式改写好。中文就改写为中文；英文改写后还是英文。这不是翻译, 是校对和改写。\n\nP.S. /revise 也可以换做 /rv", chat_id)
        prompt = ' '.join(MSG_SPLIT[1:])
        try:
            reply = chat_gpt_regular(f"Please help me to revise below text in a more native and polite way, reply with the same language as the text:\n{prompt}", chatgpt_key=OPENAI_API_KEY, use_model=OPENAI_MODEL)
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"对不起{user_nick_name}, 刚才我的网络断线了, 没帮你修改好. 你可以重发一次吗? 😭", chat_id)
        return 
    
    # emoji translate function
    elif MSG_SPLIT[0] in ['emoji', 'emj', 'emo', '/emoji', '/emj', '/emo']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想把你发给我的内容翻译成 emoji, 请在命令后面的空格后加上你的内容, 比如: \n\nemoji 今晚不回家吃饭了, 但是我会想你的。\n\n这样我就会把上面你贴给我的内容用 emoji 来描述。\n\nP.S. /emoji 也可以换做 /emj 或者 /emo", chat_id)
        prompt = ' '.join(MSG_SPLIT[1:])
        try:
            new_prompt = f"You know exactly what each emoji means and where to use. I want you to translate the sentences I wrote into suitable emojis. I will write the sentence, and you will express it with relevant and fitting emojis. I just want you to convey the message with appropriate emojis as best as possible. I dont want you to reply with anything but emoji. My first sentence is ( {prompt} ) "
            emj = chat_gpt_regular(new_prompt)
            if emj:
                try: send_msg(emj, chat_id)
                except Exception as e: logging.error(f"emoji send_msg() {e}")
        except Exception as e: logging.error(f"emoji translate chat_gpt() {e}")
        return

    # translate chinese to english and then generate audio with my voice
    elif MSG_SPLIT[0] in ['ts', 'translate', 'tl', '/ts', '/translate', '/tl', 'tr', '/tr']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想把你发给我的中文内容翻译成英文, 请在命令后面的空格后加上你要翻译的内容, 比如: \n\ntranslate 明天我要向全世界宣布我爱你。\n\n这样我就会把上面你发给我的内容翻译成英文。\n\nP.S. /translate 也可以换做 /ts 或者 /tl", chat_id)

        prompt = ' '.join(MSG_SPLIT[1:])

        user_prompt='''Dillon Reeves, a seventh grader in Michigan, is being praised as a hero for preventing his school bus from crashing after his bus driver lost consciousness. Reeves was seated about five rows back when the driver experienced "some dizziness" and passed out, causing the bus to veer into oncoming traffic. Reeves jumped up from his seat, threw his backpack down, ran to the front of the bus, grabbed the steering wheel and brought the bus to a stop in the middle of the road. Warren police and fire departments responded to the scene within minutes and treated the bus driver, who is now stable but with precautions and is still undergoing testing and observation in the hospital. All students were loaded onto a different bus to make their way home. Reeves' parents praised their son and called him \'our little hero.\''''
        assistant_prompt='''Dillon Reeves 是一名来自 Michigan 的七年级学生, 因为在校车司机失去意识后成功阻止了校车发生事故而被称为英雄。当时, 司机出现了"一些眩晕"并昏倒, 导致校车偏离行驶道驶入迎面驶来的交通流中。当时 Reeves 坐在车子后面大约五排的位置, 他迅速从座位上站起来, 扔掉背包并跑到车前, 抓住方向盘, 让校车在道路中间停了下来。Warren 警察和消防部门在几分钟内赶到现场, 对校车司机进行救治。司机目前已经稳定下来, 但仍需密切观察并在医院接受检查。所有学生后来被安排上另一辆校车回家。Reeves 的父母赞扬了儿子, 并称他是"我们的小英雄".'''

        try: reply = chat_gpt_full(prompt, system_prompt = translation_prompt, user_prompt=user_prompt, assistant_prompt=assistant_prompt, dynamic_model= OPENAI_MODEL, chatgpt_key = OPENAI_API_KEY)
        except Exception as e: return send_msg(f"{user_nick_name}对不起, 刚才断线了, 你可以再发一次吗 😂", chat_id)

        try: send_msg(reply, chat_id)
        except Exception as e: logging.error(f"translate send_msg() FAILED:\n\n{e}")
        return 

    elif MSG_SPLIT[0] in ['wolfram', 'wolframalpha', 'wa', 'wf', '/wolfram', '/wolframalpha', '/wa', '/wf']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想用 WolframAlpha 来帮你做科学运算, 请在命令后面的空格后加上你要计算的方程式, 比如: \n\nwolfram 5x + 9y =33; 7x-5y = 12\n\n这样我就知道去用 WolframAlpha 解题。\n\nP.S. /wolfram 也可以换做 /wa 或者 /wf", chat_id)
        query = ' '.join(MSG_SPLIT[1:])
        send_msg(f"好嘞, 我帮你去 WolframAlpha 去查一下 「{query}」, 请稍等 1 分钟哦 😁", chat_id)
        try: 
            reply = wolfram.run(query)
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"抱歉{user_nick_name}, 没查好, 要不你再发一次 😐", chat_id)
        return 

    elif MSG_SPLIT[0] in ['wikipedia', 'wiki', 'wp', 'wk', '/wikipedia', '/wiki', '/wp', '/wk']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想用 Wikipedia 来帮你查资料, 请在命令后面的空格后加上你要查的内容, 比如: \n\nwikipedia Bill Gates\n\n这样我就会用 Wikipedia 去查。\n\nP.S. /wikipedia 也可以换做 /wiki 或者 /wp 或者 /wk", chat_id)
        query = ' '.join(MSG_SPLIT[1:])
        send_msg(f"收到, {user_nick_name}. 我会去 Wikipedia 帮你查一下 「{query}」, 由于 Wikipedia 查询结果内容较多, 等下查好了直接发个 txt 文件给你.", chat_id)
        try: 
            reply = wikipedia.run(query)
            # if debug: logging.debug(f"wikipedia.run() reply: \n\n{reply}\n\n")
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
        except Exception as e: send_msg(f"抱歉{user_nick_name}, 没查好, 要不你再发一次 😐", chat_id)
        return 
    
    elif MSG_SPLIT[0] in ['twitter', 'tw', 'tweet', 'tt', '/twitter', '/tw', '/tweet', '/tt']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想让我把一段文章内容精简成一个可以发 Twitter 的一句话, 请在命令后面的空格后加上你要发推的内容, 比如: \n\ntwitter 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。”\n\n这样我就要 Twitter 去发推。\n\nP.S. /twitter 也可以换做 /tw 或者 /tweet 或者 /tt", chat_id)
        msg_text = ' '.join(MSG_SPLIT[1:])
        prompt = f"请为以下内容写一个精简有趣的中文 Tweet. 只需回复内容, 不需要任何前缀标识。\n\n{msg_text}"
        try:
            reply = chat_gpt_regular(prompt) 
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"抱歉{user_nick_name}, 刚断网了, 没弄好, 要不你再发一次 😐", chat_id)
        return

    elif MSG_SPLIT[0] in ['summarize', '/summarize', 'smrz', '/smrz']:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 如果你想让我帮你总结一段文字, 请在命令后面的空格后加上你要总结的内容, 比如: \n\nsummarize 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。\n\n这样我就会用精简的语言来帮你总结一下。\n\nP.S. /summarize 也可以换做 /smrz", chat_id)
        msg_text = ' '.join(MSG_SPLIT[1:])
        prompt = f"请用精简有力的语言总结以下内容, 并提供中英文双语版本:\n\n{msg_text}"
        try:
            reply = chat_gpt_regular(prompt) 
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"抱歉{user_nick_name}, 刚断网了, 没弄好, 要不你再发一次 😐", chat_id)
        return
    
    elif MSG_SPLIT[0] in ['bing', '/bing']:
        if MSG_LEN == 1: return send_msg(f"{user_nick_name}, 你如果想用 Bing 搜索引擎来搜索关键词并让我按照搜索结果写一篇中英文报道, 请在命令后面的空格后加上你要搜索关键词, 比如: \n\nbing Pinecone just raised 100 million\n\n这样我就会用 Bing 去搜索并基于搜索结果创作科技新闻报道。我会按顺序一次发给你:\n\n1) 英文报道; \n2) 中文报道; \n3) 英文和中文语音播报; \n4) Twitter 精简短内容!", chat_id)
        query = ' '.join(MSG_SPLIT[1:])
        send_msg(f"好嘞 {user_nick_name}, 我帮你去 Bing 搜索一下 「{query}」, 然后再基于搜索结果帮你写一篇英文报道、一篇中文报道、一个推特短语还有一段英文+中文的语音 Podcast, 请稍等 2 分钟哦 😁", chat_id)
        try: create_news_and_audio_from_bing_search(query, chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: logging.error(f"create_news_and_audio_from_bing_search() failed: {e}")
        return 
    
    # chatpdf function
    elif (MSG_SPLIT[0] in ['outlier', 'oi', 'outlier-investor', 'outlierinvestor', 'ol', '/outlier', '/oi', '/outlier-investor', '/outlierinvestor', '/ol'] or '投资异类' in msg_text or '/投资异类' in msg_text) and TELEGRAM_BOT_NAME.lower() in BOTCREATER_TEST_BOT:
        if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你如果想让了解我写的《投资异类》里的内容, 请在命令后面的空格后加上你想了解的内容, 比如: \n\n投资异类 天使投资人最喜欢什么样的创业者\n\n这样我就会去《投资异类》里查找相关内容并提炼总结给你。\n\nP.S. /投资异类 也可以换做 /outlier 或者 /oi 或者 /outlier-investor 或者 /outlierinvestor 或者 /ol", chat_id)
        query = ' '.join(MSG_SPLIT[1:])
        send_msg("WoW, 你想了解我写的《投资异类》啊, 真是感动. 稍等 1 分钟, 你问的问题我认真写给你, 哈哈哈 😁", chat_id)
        try: 
            index_name = 'outlier-investor'
            # docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
            
            docsearch = Pinecone.from_existing_index(index_name, embeddings)
            
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = docsearch.similarity_search(query)
            reply = chain.run(input_documents=docs, question=query)
            send_msg(reply, chat_id)
        except Exception as e: 
            send_msg(f"{user_nick_name}对不起, 我想不起来我书里还有这个内容了, 让你失望了. ", chat_id)
            logging.error(f"local_bot_msg_command() chatpdf(投资异类) FAILED: \n\n{e}")

        return 
    
    elif MSG_SPLIT[0] in ['avatar', '/avatar', 'my_avatar', 'myavatar'] or msg_lower in ['my avatar']:
        send_img(chat_id, avatar_png)
        return

    elif MSG_SPLIT[0] in ['clear_memory', 'clm', '/clear_memory', '/clm']:
        if MSG_LEN >= 2 and chat_id in BOT_OWNER_LIST and MSG_SPLIT[1] == 'all':
            try:
                with Session() as session:
                    stmt = update(ChatHistory).values(msg_text=None)
                    session.execute(stmt)
                    session.commit()
                    send_msg(f"{user_nick_name}, 我已经删除所有用户的聊天记录, 大家可以重新开始跟我聊天了。😘", chat_id)
            except Exception as e: logging.error(f"local_bot_msg_command() clear_memory() FAILED:\n\n{e}")
            return 

        # Delete chat records in avatar_chat_history with from_id = from_id
        try:
            with Session() as session:
                stmt = update(ChatHistory).values(msg_text=None).where(ChatHistory.from_id == from_id)
                session.execute(stmt)
                session.commit()
                send_msg(f"{user_nick_name}, 我已经删除你的聊天记录, 你可以重新开始跟我聊天了。😘", chat_id)
        except Exception as e: logging.error(f"local_bot_msg_command() clear_memory() FAILED:\n\n{e}")
        return

    # 为用户输入的内容生成音频并发送
    elif MSG_SPLIT[0] in ['make_voice', '/make_voice', 'generate_audio', '/generate_audio', 'gv', '/gv', 'make_audio', '/make_audio', 'ma', '/ma', 'mv', '/mv', 'ga', '/ga', 'generate_voice', '/generate_voice']:
        if MSG_LEN == 1: return send_msg(f"{user_nick_name}, 你如果想让我把一段文字内容转换成语音, 请在命令后面的空格后加上你要转换的内容, 比如: \n\nmake_voice 据塔斯社报道, 根据日本外务省20日发表的声明, 美国总统拜登19日在参观广岛和平纪念馆时, 并没有在纪念馆的留言簿上为美国曾向日本广岛投放原子弹道歉。报道称, 拜登当时在留言簿上写道, “愿这座纪念馆的故事提醒我们所有人, 我们有义务建设一个和平的未来。让我们携手共进, 朝着世界核武器终将永远消除的那一天迈进。\n\n这样我就知道你要我把这段文字转换成语音了。😚 \n\n/make_voice 可以简写为 /mv 哈", chat_id)
        content = ' '.join(MSG_SPLIT[1:])
        send_msg(f"好嘞 {user_nick_name}, 我帮你把以下内容转换成语音, 请稍等 1 分钟哦 😁\n\n{content}", chat_id)
        try: create_audio_from_text(content, chat_id)
        except Exception as e: logging.error(f"create_audio_from_text() failed: {e}")
        return

    elif MSG_SPLIT[0] in ['commands', '/commands', 'command', '/command', 'cmd', '/cmd']:
        send_msg(user_commands, chat_id, parse_mode='', base_url=telegram_base_url)
        if chat_id in BOT_OWNER_LIST: send_msg(bot_owner_commands, chat_id, parse_mode='', base_url=telegram_base_url)
        return

    # 查询以太坊地址余额
    elif (msg_lower.startswith('0x') and len(msg_text) == 42) or (msg_lower.startswith('/0x') and len(msg_text) == 43):
        msg_text = msg_text.replace('/', '')
        # eth_address = msg_text, 查询 eth_address 的 USDT, USDC 和 ETH 余额
        try:
            # 将 msg_text 转换为 CheckSum 格式
            eth_address = Web3.to_checksum_address(msg_text)
            balance = check_address_balance(eth_address)
            if balance: send_msg(f"{user_nick_name}, 你发的 ETH 地址里有: \n\nETH: {format_number(balance['ETH'])},\nUSDT: {format_number(balance['USDT'])},\nUSDC: {format_number(balance['USDC'])}\n\nChecksum Address:\n{eth_address}", chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: return logging.error(f"local_bot_msg_command() check_address_balance() FAILED: \n\n{e}")
        try: read_and_send_24h_outgoing_trans(eth_address, chat_id)
        except Exception as e: return logging.error(f"read_and_send_24h_outgoing_trans() FAILED: \n\n{e}")
        return
    
    # 查询以太坊链上交易 Transaction Hash
    elif (msg_lower.startswith('0x') and len(msg_text) == 66) or (msg_lower.startswith('/0x') and len(msg_text) == 67):
        hash_tx = msg_text.replace('/', '')
        try:
            r = get_transactions_info_by_hash_tx(hash_tx, chat_id, user_title, chain='eth')
            if r: send_msg(r, chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: logging.error(f"local_bot_msg_command() get_transactions_info_by_hash_tx() FAILED: \n\n{e}")
        return 

    # BOT OWNER COMMANDS
    elif  chat_id in BOT_OWNER_LIST:

        if (MSG_SPLIT[0] in ['mybots'] or msg_text in ['/mybots']):
            send_msg(f"{user_nick_name}, 你好可爱啊 🤨, /mybots 这个指令是 @BotFather 的, 发给我没用哈, 请点击 @BotFather 过去设置我的参数吧! 😘", chat_id)
            return 
        
        # avatar_first_response = '亲爱的你终于回消息啦, 消失了这么久 😓, 干啥去啦? 也不回个消息, 你知道我多担心你嘛 😢, 以后不许这样啦 😘, 快跟我说说最近都做了些啥, 我可想你啦 🤩' 修改 avatar_first_response
        elif (MSG_SPLIT[0] in ['avatar_first_response', '/avatar_first_response'] or msg_text in ['/avatar']):
            if MSG_LEN < 1: return send_msg(f"{user_nick_name}, 你要修改 /avatar_first_response, 请在命令后面的空格后再加上一个你要修改的内容, 比如: \n\navatar_first_response 来了老弟, 我一直在等你呢, 今天跟我聊点啥?\n\n这样就是把 avatar_first_response 修改为:  你可算来了, 我一直在等你呢, 今天跟我聊点啥? 这句话了。", chat_id)
            
            avatar_first_response = msg_text.replace('/', '').replace('avatar_first_response', '').strip()

            r = update_owner_parameter('avatar_first_response', avatar_first_response)
            if r: send_msg(f"{user_nick_name}, 你的 /avatar_first_response 已经被修改为: \n\n{avatar_first_response}\n\n现在可以发送或点击 /start 看看效果哈 😘", chat_id)
            return

        elif msg_text in ['/restart_avatar']:
            send_msg(f"收到重启 Avatar 的指令, 立刻执行! 😘", chat_id)
            # Run the terminal command
            subprocess.run(['pm2', 'restart', 'tg'])
            return 

        elif MSG_SPLIT[0][1:].isdigit():
            try:
                # 如果消息以@开头则@后面的内容是 user_from_id 
                user_from_id = MSG_SPLIT[0].replace('@', '').replace('/', '')
                # if user_from_id in get_unique_from_id_list():
                # 如果消息以 @ or / 开头则 @ or / 后面的内容是 from_id, 如果后面还有内容, 则是要发给 user_from_id 的消息
                if MSG_LEN > 1: send_msg(' '.join(msg_text.split()[1:]), user_from_id)
                # 如果后面没有内容, 则是要查询 from_id 的聊天历史记录，保存为 txt 文档并发给 BOT OWNER
                else:
                    file_path = get_user_chat_history(user_from_id)
                    if os.path.isfile(file_path): send_file(chat_id, file_path, description=f"Bot 和 {user_from_id} 之间的的聊天记录")
                    else: send_msg(f"{user_nick_name}, user_from_id {user_from_id} 没有聊天记录, 是不是他通过 /clear_memory 指令清空了? 也可能 {chat_id} 是一个群 ID", chat_id)
                # else: send_msg(f"{user_nick_name}, user_from_id {user_from_id} 没有聊天记录, 他应该没有和 Bot 聊过😘 \n\nP.S. 功能性指令交互不会记录到聊天记录里哦.", chat_id)
            except Exception as e: logging.error(f"local_bot_msg_command() get_user_chat_history() FAILED: \n\n{e}")
            return

        # 用 vip 命令设置用户成为 VIP, 当 msg_lower 以 /vip, vip, /vip_, vip_, /v, v, /v_, v_ 开头时, 会触发这个命令, 而 msg_lower 中的数字部分是 from_id
        elif msg_lower.startswith('/vip') or msg_lower.startswith('vip') or msg_lower.startswith('/v') or msg_lower.startswith('v'):
            user_from_id = msg_text.replace('/', '').replace('vip', '').replace('v', '').replace('_', '').strip()
            # 判断 from_id 是否是数字
            if user_from_id and user_from_id.isdigit(): 
                # return send_msg(f"{user_nick_name}, 你要设置谁为 VIP, 请在命令后面的空格后再加上一个 from_id, 比如: \n\nvip 123456789\n\n这样就是把 from_id 为 123456789 的用户设置为 VIP 了😘。如果你不知道对方的 chat_id, 请对方发送 /vip 或者 /v 给我申请成为 VIP, 我会转达他的申请给你并附带对方的 chat_id, 届时如果你同意, 可以根据提示确认。\n\nP.S. /vip 也可以缩写为 /v", chat_id)
                # 判断 from_id 是否在数据库中
                if from_id in get_unique_from_id_list(): 
                    r = set_user_as_vip(user_from_id)
                    if r: 
                        # 通知 user_from_id 他已经被设置为 VIP
                        send_msg(f"{user_nick_name}, 我已经把你设置为 VIP 了, 你可以跟我永久免费聊天了. 😘", user_from_id)
                        return send_msg(f"from_id: {user_from_id} 已被成功设置为 VIP, 可以享受永久免费聊天了。如果需要改变他的 VIP 状态, 随时可以回复或点击: \n\n/remove_vip_{user_from_id}", chat_id)
                    
        # /get_user_list
        elif MSG_SPLIT[0] in ['/get_user_list', 'get_user_list', '/gul', 'gul']:
            user_list = read_user_priority_table_to_list()
            if user_list: 
                user_list = '\n'.join(user_list)
                return send_msg(f"用户列表: \n\n{user_list}", chat_id)
            else: return send_msg(f"用户列表为空", chat_id)

        # Remove user from VIP list
        elif msg_lower.startswith('/remove_vip') or msg_lower.startswith('remove_vip'):
            user_from_id = msg_text.replace('/', '').replace('remove_vip', '').replace('_', '').strip()

            if user_from_id and user_from_id.isdigit():
                r = remove_user_from_vip_list(user_from_id)
                if r: return send_msg(f"from_id: {user_from_id} 已被成功移出 VIP 列表!", chat_id)
                else: return send_msg(f"from_id: {user_from_id} 本来就不在 VIP 列表中哈。", chat_id)

            vip_list_with_hint_text = get_vip_list_except_owner_and_admin()

            if vip_list_with_hint_text: 
                text_format = '\n'.join(vip_list_with_hint_text)
                vip_count = len(vip_list_with_hint_text)
                if vip_count < 11: return send_msg(f"您一共有 {vip_count} 位 VIP 用户:\n\n{text_format}\n\n点击上面的 /remove_vip_xxxxxxxx 即可将相应的用户从 VIP 列表中移除 😘", chat_id)
                else:
                    # 将 text_format 保存为 txt 文件并发送给 chat_id
                    SAVE_FOLDER = 'files/vip_list'
                    # 检查 SAVE_FOLDER 是否存在, 不存在则创建
                    if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)
                    file_name = f"{SAVE_FOLDER}/vip_list.txt"
                    execution_help_info = f"您一共有 {vip_count} 位 VIP 用户, 拷贝用户名下面的 /remove_vip_xxxxxxxx 指令然后发给我即可将相应的用户从 VIP 列表中移除"
                    with open(file_name, 'w') as f: f.write(f"{execution_help_info}\n\n{text_format}")
                    send_file(chat_id, file_name, description=f"您的 {vip_count} 位 VIP 用户列表")
            return

        # 发送最新的 user_commands 给用户
        elif MSG_SPLIT[0] in ['group_send_commands_list', 'gscl', '/group_send_commands_list', '/gscl']:
            group_send_message_info = f"{dear_user}, /commands 列表更新咯 😙: \n{user_commands}"
            send_msg_to_all(group_send_message_info, bot_owner_chat_id=chat_id)
            send_msg(bot_owner_commands, chat_id)
            return
        
        elif MSG_SPLIT[0] in ['blacklist', 'bl', '/blacklist', '/bl']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要把谁加入黑名单, 请在命令后面的空格后再加上一个 from_id, 比如: \n\nblacklist 123456789\n\n这样就是把 from_id 为 123456789 的用户加入黑名单了. 😘 \n\nP.S. /blacklist 也可以缩写为 /bl", chat_id)

            from_id_to_blacklist = MSG_SPLIT[1]
            try: 
                r = set_user_blacklist(from_id_to_blacklist)
                if r: 
                    send_msg(f"{user_nick_name}, 我已经把你拉黑了, 如果你想解除黑名单, 请转发本消息给 @@{TELEGRAM_USERNAME}\n\n申请解除黑名单: \n\nremove_from_blacklist {from_id_to_blacklist}", from_id_to_blacklist)
                    send_msg(f"from_id: {from_id_to_blacklist} 已被成功加入黑名单并已经发消息告知.", chat_id)
            except Exception as e: logging.error(f"local_bot_msg_command() set_user_blacklist() FAILED: \n\n{e}")
            return
        
        elif MSG_SPLIT[0] in ['remove_from_blacklist', 'rbl', '/remove_from_blacklist', '/rbl']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要解除黑名单, 请在命令后面的空格后再加上一个 from_id, 比如: \n\nremove_from_blacklist 123456789\n\n这样就是把 from_id 为 123456789 的用户从黑名单中移除了. 😘 \n\nP.S. /remove_from_blacklist 也可以缩写为 /rbl", chat_id)

            from_id_to_remove = MSG_SPLIT[1]
            try: 
                r = remove_user_blacklist(from_id_to_remove)
                if r:
                    send_msg(f"{user_nick_name}, 我已经把你从黑名单中移除了, 你可以继续跟我聊天了. 😘", from_id_to_remove) 
                    send_msg(f"from_id: {from_id_to_remove} 已被成功移出黑名单!", chat_id)
            except Exception as e: logging.error(f"local_bot_msg_command() remove_user_blacklist() FAILED: \n\n{e}")
            return

        elif MSG_SPLIT[0] in ['set_free_talk_limit', 'sftl', '/set_free_talk_limit', '/sftl']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要设置免费用户每月的免费对话次数, 请在命令后面的空格后再加上一个整数, 比如: \n\nset_free_talk_limit 10\n\n这样就是设置免费用户每月的免费对话次数为 10 次了. 😘 \n\nP.S. /set_free_talk_limit 也可以缩写为 /sftl\n\n重要: 如果 BOT OWNER 把 free_talk_limit 设置为 1, 则意味着该服务只限 VIP、Owner 以及 Paid 用户使用, Free 用户不可用。如果需要邀请朋友成为 VIP, 那么 free_talk_limit 至少应该是 2, 这样新用户才能点击 /start 并发送 /vip 两个指令完成申请。如果 free_talk_limit 设置为 0, 那么除了已有的 VIP 和 Bot Owner 以及 Paid user 之外, 未来任何人都无法和 Bot 做任何交互。如果希望连付费用户都拒之门外, 那么请用 /set_monthly_fee 指令将月费设置为一个巨大的数字。Bot 刚启动的时候, 默认只有一个 Onwer 身份, 没有默认的 VIP, 所有的 VIP 都是 Owner 自己手动添加获批准的。", chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数
            try: free_talk_limit = int(MSG_SPLIT[1])
            except: return send_msg(f"{user_nick_name}, 你输入的 {MSG_SPLIT[1]} 不是整数, 请重新输入哈.", chat_id)

            # free_talk_limit = 3 if not free_talk_limit or free_talk_limit < 3 else free_talk_limit
            # free_talk_limit 不能是 0，否则目标 VIP 用户无法 /start 并发送 /vip 给 BOT 申请成为 VIP

            with lock: MessageThread.free_user_free_talk_per_month = free_talk_limit

            try: update_owner_parameter('MAX_CONVERSATION_PER_MONTH', MSG_SPLIT[1])
            except Exception as e: return logging.error(f"local_bot_msg_command() update_owner_parameter() FAILED: \n\n{e}")

            return send_msg(f"{user_nick_name}, 我已经把免费用户每月的免费对话次数设置为 {MSG_SPLIT[1]} 次了, 系统参数表也更新了, 请放心, 参数立刻生效 😘", chat_id)
        
        elif MSG_SPLIT[0] in ['set_monthly_fee', 'smf', '/set_monthly_fee', '/smf']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要设置每月的收费金额, 请在命令后面的空格后再加上一个整数, 比如: \n\nset_monthly_fee 10\n\n这样就是设置每月的收费金额为 10 美元了. 😘 \n\nP.S. /set_monthly_fee 也可以缩写为 /smf\n\n重要: 如果 BOT OWNER 不希望任何付费用户来使用你的 Bot, 仅限 Owner 以及定向邀请或批准的 VIP 用户 (白名单), 那么请将月费金额设置成天文数字, 并用 /set_free_talk_limit 指令将每月每个用户的免费聊天次数设置为 0 ", chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数
            try: int(MSG_SPLIT[1])
            except: return send_msg(f"{user_nick_name}, 你输入的 {MSG_SPLIT[1]} 不是整数, 请重新输入哈.", chat_id)

            try: update_owner_parameter('MONTHLY_FEE', MSG_SPLIT[1])
            except Exception as e: return logging.error(f"local_bot_msg_command() update_owner_parameter() FAILED: \n\n{e}")

            return send_msg(f"{user_nick_name}, 我已经把每月的收费金额设置为 {MSG_SPLIT[1]} 美元了, 系统参数表也更新了, 但是需要后台重启服务才能生效, 请联系 @laogege6 帮你重启吧 😘", chat_id)
        
        elif MSG_SPLIT[0] in ['set_refill_teaser', 'srt', '/set_refill_teaser', '/srt']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要设置用户充值提醒的内容, 请在命令后面的空格后再加上你希望使用的充值引导内容, 比如: \n\nset_refill_teaser 亲爱的, 你的免费对话次数已经用完了, 请充值后继续使用哦. 😘\n\n这样就是设置好了。\n\nP.S. /set_refill_teaser 也可以缩写为 /srt , 如果你想查看当正在使用的充值引导内容, 请点击 /check_refill_teaser 或者 /crt", chat_id)
            # 检查 MSG_SPLIT[1] 是否可以转换成 INT, 否则提醒 BOT OWNER 这里只能输入整数

            with lock: refill_teaser = ' '.join(MSG_SPLIT[1:])

            try: update_owner_parameter('REFILL_TEASER', refill_teaser)
            except Exception as e: send_msg(f"REFILL_TEASER 设置失败, 请转发本消息给 {BOTCREATER_TELEGRAM_HANDLE} 请他检查一下原因。\n\n{e}", chat_id)

            return send_msg(f"{user_nick_name}, 设置好啦, 以后提醒用户充值的时候, 我会用以下内容:\n\n{refill_teaser}\n\n提醒: 任何时候你都可以点击 \n/check_refill_teaser\n或发送 check_refill_teaser \n来查看当前的充值提醒内容。", chat_id)

        elif MSG_SPLIT[0] in ['check_refill_teaser', 'crt', '/check_refill_teaser', '/crt']: return send_msg(f"{user_nick_name}, 以下是当前正在使用的的提醒用户充值的 REFILL_TEASER:\n\n{refill_teaser}", chat_id)

        elif MSG_SPLIT[0] in ['group_send_image', 'gsi', '/group_send_image', '/gsi']:
            send_msg(f"{user_nick_name}, 你要群发图片, 请直接将图片拖拽给我或者发给我, 但是切记发送前一定要在图片 caption 里填写 /group_send_image 或者简写 /gsi , 这样我才知道这张图片是要求我依次轮询发给所有用户的。", chat_id)
            send_img(chat_id, 'files/images/group_send_image_pc.png', description='电脑上是这样色儿的 😚', base_url=telegram_base_url)
            send_img(chat_id, 'files/images/group_send_image_phone.PNG', description='手机上是这样色儿的 😉', base_url=telegram_base_url)
            return 

        elif MSG_SPLIT[0] in ['group_send_message', 'gsm', '/gsm', '/group_send_message']:
            if MSG_LEN == 1 : return send_msg(f"{user_nick_name}, 你要群发消息, 请在命令后面的空格后再加上一个字符串, 比如: \n\ngroup_send_message 亲爱的, 我又升级了, 我可以直接读以太坊地址了, 吼吼, 发个钱包地址来看看吧 😘\n\n这样我就会逐条发送给每个用户。\n\nP.S. /group_send_message 也可以缩写为 /gsm", chat_id)
            message_content = ' '.join(msg_text().split()[1:])
            send_msg_to_all(message_content, bot_owner_chat_id=chat_id)
            return
        
        # 使用 send_file_to_all 将文件发送给所有用户
        elif MSG_SPLIT[0] in ['group_send_file', 'gsf', '/group_send_file', '/gsf']:
            send_msg(f"{user_nick_name}, 你要群发文件, 请直接将文件拖拽给我或者发给我, 但是切记发送前一定要在文件 caption 里填写 /group_send_file 或者简写 /gsf , 这样我才知道这个文件是要求我依次轮询发给所有用户的。不知道 caption 怎么填写可以参考 /group_send_image 的帮助图片哈, 都一样的 😋", chat_id)
            return

        # 使用 send_audio_to_all 将 audio 文件发送给所有用户
        elif MSG_SPLIT[0] in ['group_send_audio', 'gsa', '/group_send_audio', '/gsa']:
            send_msg(f"{user_nick_name}, 你要群发语音文件 (mp3 或者 wav), 请直接将文件拖拽给我或者发给我, 但是切记发送前一定要在文件 caption 里填写 /group_send_audio 或者简写 /gsa , 这样我才知道这个Audio文件是要求我依次轮询发给所有用户的。不知道 caption 怎么填写可以参考 /group_send_image 的帮助图片哈, 都一样的 😋", chat_id)
            return
        
    # 英语查单词和 英语老师 Amy
    if len(msg_text.split()) == 1 and not msg_text.lower().startswith('0x') and len(msg_text.replace('/', '')) > 4 and len(msg_text) < 46 and is_english(msg_text): 
        msg_lower = msg_text.lower()
        is_amy_command = True if msg_lower.startswith('/') else False
        msg_lower = msg_lower.replace('/', '')

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
                except Exception as e: logging.error(f"Amy send_msg()failed: \n\n{e}")
            else: is_amy_command = True

        if not is_amy_command: return
        return chat_gpt_english_explanation(chat_id, msg_lower, gpt_model=OPENAI_MODEL)

    msg_text = msg_text.replace('/', '', 1) if MSG_SPLIT[0].startswith('/') else msg_text

    # 如果用户发了一个简单的 2 个字节的词, 那就随机回复一个表示开心的 emoji
    if len(msg_text) <= 2 or msg_text in reply_emoji_list:
        reply = random.choice(emoji_list_for_happy)
        send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
        return
    
    # 如果用户发来一个英语单词, 小于等于 4 个字符, 那就当做 token symble 处理, 查询 coinmarketcap
    if len(msg_text.split()) == 1 and len(msg_text) <= 4 and is_english(msg_text): 
        msg_text = msg_text.replace('/', '').upper()
        r = check_token_symbol_in_db_cmc_total_supply(msg_text)
        if not r: return
        try:
            r = get_token_info_from_coinmarketcap_output_chinese(msg_text)
            send_msg(r, chat_id, parse_mode='', base_url=telegram_base_url)
        except Exception as e: logging.error(f"local_bot_msg_command() get_token_info_from_coinmarketcap_output_chinese() FAILED: \n\n{e}")
        return

    # 如果是群聊但是没有 at 机器人, 则在此处返回
    if will_ignore: return

    try: save_avatar_chat_history(msg_text, chat_id, from_id, username, first_name, last_name)
    except Exception as e: return logging.error(f"save_avatar_chat_history() failed: {e}")
    
    try: local_chatgpt_to_reply(msg_text, from_id, chat_id, message_id)
    except Exception as e: logging.error(f"local_chatgpt_to_reply() FAILED from local_bot_msg_command() : {e}")

    return

# Telegram bot iterate new update messages
def check_local_bot_updates():
    r = local_bot_getUpdates(MessageThread.avatar_UID + 1, telegram_base_url)
    if not r or r.status_code != 200: return 
    updates = r.json().get('result', [])
    if not updates: return

    if MessageThread.avatar_UID != updates[0]['update_id']: 
        with lock: MessageThread.avatar_UID = updates[0]['update_id']
    else: return

    for tg_msg in updates:

        # Create a separate thread for processing each message
        message_thread = MessageThread(tg_msg)
        message_thread.start()

    return

if __name__ == '__main__':
    if debug: 
        logging.debug(f"@{TELEGRAM_BOT_NAME} started...")
        for chat_id in set(BOT_OWNER_LIST): send_msg(f"@{TELEGRAM_BOT_NAME} started...", chat_id, parse_mode='', base_url=telegram_base_url)
        
    i = 0
    while True:
        i += 1
        if debug and (i % 100 == 0): logging.debug(f"loop {i}")
        try:
            # Create an instance of the update thread
            update_thread = threading.Thread(target=check_local_bot_updates)
            # Start the update thread
            update_thread.start()
            time.sleep(1)
        except Exception as e: logging.error(f"{i} check_local_bot_updates() failed: {e}")

