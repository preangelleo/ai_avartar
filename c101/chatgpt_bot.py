from c101variables import *
from chatgpt_english import *
from c101functions import *
from c101binance import get_balances_realtime_value_dataframe
from stability_ai import *
from c101twitter import *

global_UID = -2  # 798099121
qa = ''

def owner(from_id):
    TG_Group_Owner = [bot_owner_chat_id, woshi_laogege, danli_yu]
    if str(from_id) in TG_Group_Owner:
        return True
    else:
        return False

def create_chatgpt_whitelist_table():
    with db_engine.connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS db_chatgpt_whitelist (id INT AUTO_INCREMENT PRIMARY KEY, from_id VARCHAR(255) NOT NULL, user_name VARCHAR(255) DEFAULT NULL, first_name VARCHAR(255) DEFAULT NULL, is_approved TINYINT DEFAULT 0)")
    return True

def create_ai_chat_history_table():
    with db_engine.connect() as con:
        con.execute("CREATE TABLE IF NOT EXISTS ai_chat_history (id INT AUTO_INCREMENT PRIMARY KEY, `question_input` TEXT DEFAULT NULL, `response_output` TEXT DEFAULT NULL, `update_time` DATETIME)")
    return True

def in_direct_chat_whitelist(from_id):
    if debug:
        print(f"DEBUG: in_direct_chat_whitelist()")
    try:
        return not pd.read_sql_query(f'SELECT * FROM db_chatgpt_whitelist WHERE from_id="{from_id}" AND is_approved=1', db_engine).empty
    except:
        return False

def update_chatgpt_whitelist(from_id):
    if debug:
        print(f"DEBUG: update_chatgpt_whitelist(): {from_id}")
    try:
        with db_engine.connect() as con:
            query_select = f"SELECT * FROM db_chatgpt_whitelist WHERE from_id='{from_id}'"
            df = pd.read_sql_query(query_select, con)
            if df.empty:
                return
            query_update = f"UPDATE db_chatgpt_whitelist SET is_approved=1 WHERE from_id='{from_id}'"
            con.execute(query_update)
        return True
    except Exception as e:
        print(f"Error updating/inserting whitelist: {e}")
    return

def apply_join_chatgpt_whitelist(from_id, first_name, user_name, base_url=base_url):
    if debug: print(f"DEBUG: apply_join_chatgpt_whitelist()")
    if not from_id: return
    if not first_name: first_name = 'none'
    if debug: print(f"DEBUG: apply_join_chatgpt_whitelist()", from_id, first_name, user_name)
    if debug: print(f"DEBUG: apply_join_chatgpt_whitelist(): {from_id}, {first_name}, {user_name}")
    try:
        with db_engine.connect() as con:
            query_select = f"SELECT * FROM db_chatgpt_whitelist WHERE from_id='{from_id}'"
            df = pd.read_sql_query(query_select, con)
            if not df.empty:
                query_update = f"UPDATE db_chatgpt_whitelist SET first_name='{first_name}', user_name='{user_name}' WHERE from_id='{from_id}'"
                con.execute(query_update)
            else:
                query_insert = f"INSERT INTO db_chatgpt_whitelist (from_id, first_name, user_name) VALUES ('{from_id}', '{first_name}', '{user_name}')"
                con.execute(query_insert)
        send_msg(f"{first_name}, {user_name}, {from_id}, 向您申请私聊，如同意，请回复：\nwhitelistadd {from_id}", bot_owner_chat_id, parse_mode='', base_url=base_url)
        return True
    except Exception as e: print(f"Error updating/inserting whitelist: {e}")
    return

def drop_from_chatgpt_whitelist(from_id):
    try:
        with db_engine.connect() as con:
            con.execute(
                f"DELETE FROM db_chatgpt_whitelist WHERE from_id='{from_id}'")
        return True
    except Exception as e:
        print(f"Error deleting from whitelist: {e}")
    return False

def translation_for_chatgpt_bot(word, chat_id=bot_owner_chat_id):
    # if debug: print(f"DEBUG: translation_for_chatgpt_bot() started")
    word_dict = st_find_ranks_for_word(word)
    if not word_dict:
        return

    word = word_dict.get('word', '')
    if not word:
        return
    if debug:
        print(f"DEBUG: translation_for_chatgpt_bot() word: {word} is legit")

    yurl = f"http://mobile.youdao.com/dict?le=eng&q={word}"
    word_category = [key.upper() for key, value in word_dict.items(
    ) if value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
    word_category_str = ' / '.join(word_category)
    word_trans = {
        '单词': f"[{word}]({yurl})",
        '排名': word_dict.get('rank', ''),
        '发音': word_dict.get('us-phonetic', ''),
        '词库': word_category_str,
        '词意': word_dict.get('chinese', ''),
    }
    if word_dict.get('synonyms', ''):
        word_trans['同义'] = word_dict.get('synonyms', '')
    results = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)

    if not chat_id:
        word_trans['单词'] = word
        if word_dict.get('chat_gpt_explanation', ''):
            word_trans['英译'] = word_dict.get('chat_gpt_explanation')
        results = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)
        return results

    send_msg(results, chat_id, parse_mode='Markdown')
    try:
        audio_path = generate_or_read_tts(folder='word_tts', content=word)
    except:
        print(f"DEBUG: WORD: {word} audio_path FAILED")
    if audio_path:
        try:
            send_audio(audio_path, chat_id)
        except:
            pass
    responsed_content = ''
    if word_dict.get('chat_gpt_explanation', ''):
        responsed_content = word_dict.get('chat_gpt_explanation')
    else:
        try:
            responsed_content = chat_gpt(
                f"What is the English explanation of {word}")
        except:
            return
        if responsed_content:
            try:
                update_or_insert_data(
                    db_engine, 'db_daily_words', 'word', word, 'chat_gpt_explanation', responsed_content)
            except:
                return
    if responsed_content:
        send_msg(f"Chat_GPT: {responsed_content}", chat_id)
        try:
            tts_file_name = generate_or_read_tts(
                folder='sentences_tts', content=responsed_content)
        except:
            return
        if tts_file_name:
            try:
                send_audio(tts_file_name, chat_id)
            except:
                return
    return word_dict

def getUpdates(previous_update_id):
    if debug:
        print(f"DEBUG: getUpdates()")
    method = "getUpdates?"
    _params = {
        "offset": previous_update_id,
        "timeout": 123,
        "limit": 10
    }
    params = urlencode(_params)
    URL = base_url + method + params
    r = requests.get(URL)
    return r

def call_chatgpt_to_reply(msg_text, chat_id=bot_owner_chat_id, conversation_id=0):
    if debug:print(f"DEBUG: call_chatgpt_to_reply()")
    openai.api_key = openai_key
    reply = ''
    df = pd.read_sql_query(f"SELECT * FROM (SELECT * FROM `telegram_chat_history` WHERE `chat_id` = '{chat_id}' ORDER BY `id` DESC LIMIT 5) sub ORDER BY `id` ASC", db_engine)

    try:
        system_prompt = f"You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work. Answer with the same language as the question, and try to answer the question as concise as possible, and use the same language as the question."
        msg_history = [{"role": "system", "content": system_prompt}]
        previous_role = 'assistant'
        
        for i in range(df.shape[0]):
            history_conversation = df.iloc[i]
            user_or_assistant = 'assistant' if history_conversation['username'] == 'lgg_chatgpt_bot' else 'user'
            if user_or_assistant == previous_role: continue
            if i == df.shape[0] - 1 and user_or_assistant == 'user': continue

            need_to_be_appended = {"role": user_or_assistant,"content": history_conversation['msg_text']}
            msg_history.append(need_to_be_appended)
            previous_role = user_or_assistant
        msg_history.append({"role": "user", "content": msg_text})

        response = openai.ChatCompletion.create(model='gpt-4', messages=msg_history)
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()

    except Exception as e: print(f"ERROR: chat_gpt() failed: \n\n{e}")

    if not reply: return

    command_conn = db_engine.connect()
    # 从 Table 中读出最新的 id
    latest_id = 0
    sql_id = f"SELECT `id` FROM `telegram_chat_history` ORDER BY `id` DESC LIMIT 1"
    result = command_conn.execute(sql_id)
    for row in result: latest_id = row[0]

    store_reply = reply.replace("'", "")
    store_reply = store_reply.replace('"', '')
    try:command_conn.execute(f"INSERT INTO `telegram_chat_history` VALUES ({latest_id+1}, 'ChatGPT', 'Bot', 'lgg_chatgpt_bot', '{str(chat_id)}', '{str(chat_id)}', '{datetime.now()}', '{store_reply}', {conversation_id})")
    except Exception as e:print(f"ERROR : call_chatgpt_to_reply() save to telegram_chat_history failed : {e}")
    command_conn.close()

    try: send_msg(reply, chat_id)
    except: pass

    if len(reply) > 6000: return reply
    is_chinese = False if is_english(reply) else True
    tts_file_name = generate_or_read_tts_male('ai_chat', reply, is_chinese)
    if tts_file_name: send_audio(tts_file_name, chat_id)
    return reply

def save_user_chat_history(**kwargs):
    if debug:
        print(f"DEBUG: save_user_chat_history()")
    chat_id = kwargs.get('chat_id')
    from_id = kwargs.get('from_id')
    first_name = kwargs.get('message_from_first_name')
    last_name = kwargs.get('message_from_last_name')
    username = kwargs.get('message_from_username')
    msg_text = kwargs.get('message_text')
    if not chat_id:
        return
    if not msg_text:
        return
    if not first_name:
        first_name = ''
    if not last_name:
        last_name = ''
    if not username:
        username = ''
    # 创建一个 table 来保存用户的聊天历史
    try:
        coversation_history_conn = db_engine.connect()
        # sql = f"CREATE TABLE IF NOT EXISTS `telegram_chat_history` (`id` INTEGER PRIMARY KEY, `first_name` TEXT, `last_name` TEXT, `username` TEXT, `from_id` TEXT, `chat_id` TEXT, `update_time` DATETIME, `msg_text` TEXT, `conversation_id` BIGINT DEFAULT 0)"
        # coversation_history_conn.execute(sql)

        # 从 Table 中读出最新的 id
        latest_id = 0
        sql_id = f"SELECT `id` FROM `telegram_chat_history` ORDER BY `id` DESC LIMIT 1"
        result = coversation_history_conn.execute(sql_id)
        for row in result:
            latest_id = row[0]

        coversation_history_conn.execute(
            f"INSERT INTO `telegram_chat_history` VALUES ({latest_id+1}, '{first_name}', '{last_name}', '{username}', '{str(from_id)}', '{str(chat_id)}', '{datetime.now()}', '{msg_text}', {latest_id})")

        return latest_id + 1

    except Exception as e:
        print(f"ERROR : save_user_chat_history() FAILED : {e}")
    return

def translate_if_is_english(prompt, chat_id=False):
    if not is_english(prompt): return 
    pre_prompt = "你是精通中文和英文的计算机科学家，也是 CNN 的科技专栏记者，现在我打算你刚刚发表的英文科技报道转载到中文媒体，请帮我翻译成中文。请注意，涉及到人名和产品名以及品牌名的情况，保留英文即可；涉及到技术专有术语，也请保留英文或者英文缩写：\n"
    text_cn = chat_gpt_regular(f"{pre_prompt} {prompt}", openai_key, 'gpt-4')
    if chat_id: send_msg(text_cn, chat_id)
    return text_cn

def msg_command(**kwargs):
    if place_holder:
        chat_id = str(kwargs.get('chat_id'))
        from_id = str(kwargs.get('from_id'))
        first_name = kwargs.get('message_from_first_name')
        user_name = kwargs.get('message_from_username')
        msg_text = str(kwargs.get('message_text'))
        conversation_id = kwargs.get('conversation_id', 0)
        
        if len(msg_text) <= 1: return
        
        if msg_text.lower().startswith('http'):

            msg_lower = msg_text.lower()
            MSG_SLT = msg_lower.split()
            MSG_LEN = len(MSG_SLT)

            if len(msg_text) < 10 or not '/' in msg_text or not '.' in msg_text or 'youtube' in msg_text: return

            try:
                loader = UnstructuredURLLoader(urls=[MSG_SLT[0]])
                documents = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents(documents)
                
                db = Chroma.from_documents(texts, embeddings)
                retriever = db.as_retriever()
                
                global qa
                qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

                query = ' '.join(MSG_SLT[1:]) if MSG_LEN > 1 else "请提炼总结一下此人的 Profile。只需回复内容, 不需要任何前缀标识。" if 'linkedin' in msg_lower else "请为该页面写一个中文 Tweet。只需回复内容, 不需要任何前缀标识。"
                send_msg(f"URL页面已加载, 如果想要咨询了解本页面的相关内容, 请使用 url 命令前缀加上您的问题。(url 命令后面需要有空格)", chat_id)
                reply = qa.run(query)
                
                try: send_msg(f"tweet {reply}\n{MSG_SLT[0]}", chat_id)
                except Exception as e: send_msg(f"ERROR: Tweet 生成失败: \n{e}", chat_id)

            except Exception as e: send_msg(f"ERROR: 页面加载及内容摘要失败: \n{e}", chat_id)
            return

        is_direct_chat = True if from_id == chat_id else False
        is_at_chatgpt = True if '@lgg_chatgpt_bot' in msg_text.lower() else False

        if not is_direct_chat and not is_at_chatgpt: return

        if msg_text == '/start': 
            send_msg(aply_for_whitelist, chat_id)
            return 

        if msg_text in ['whitelist', 'wl', '白名单', '申请白名单', '白名单申请']:
            if debug: print(f"DEBUG: msg_command() whitelist apply : whitelistadd {from_id}")
            try: r = apply_join_chatgpt_whitelist(from_id, first_name, user_name)
            except: send_msg(f"白名单申请提交失败, 请联系老哥哥 @laogege6", chat_id)
            if r: send_msg(f"白名单申请提交成功, 请提醒老哥哥 审批或者耐心等待。", chat_id)
            return

        if is_direct_chat and not from_id == bot_owner_chat_id and not in_direct_chat_whitelist(from_id): 
            send_msg(aply_for_whitelist, chat_id)
            return
        
        if is_at_chatgpt:
            msg_text = msg_text.replace('@lgg_chatgpt_bot ', '')
            kwargs['message_text'] = msg_text

        msg_lower = msg_text.lower()
        MSG_SLT = msg_lower.split()
        MSG_LEN = len(MSG_SLT)

    # Welcome and help
    if MSG_SLT[0] in help_list:
        try: send_msg(message_help, chat_id)
        except: print(f"DEBUG: msg_command() message_help FAILED")
        return

    elif MSG_SLT[0] in ['update', 'balance', 'balances'] and from_id == bot_owner_chat_id:
        df = get_balances_realtime_value_dataframe()
        coin_balances = {row['coin']: row['balance'] for _, row in df.iterrows()}
        coin_balances = '\n'.join([f"{k}:\t{format_number(v)}" for k, v in coin_balances.items()])
        if coin_balances: return send_msg(coin_balances, chat_id)
        else: return send_msg(f"ERROR : Update balances from binance failed.", chat_id)
        
    elif MSG_LEN == 1 and is_english(msg_text):
        if debug: print(f"DEBUG: Checking English Dictionary for: {msg_text}")
        
        word_dict = {}
        try: word_dict = translation_for_chatgpt_bot(msg_lower, chat_id)
        except: print(f"ERROR: msg_command() translation_for_chatgpt_bot() FAILED")
        if word_dict: return

        output_text = chat_gpt_word_correction( msg_lower, chatgpt_key=openai_key)
        if output_text: send_msg(output_text, chat_id)
        return

    # image generate function
    elif MSG_SLT[0] in ['img', 'ig', 'image']:
        if MSG_SLT[1] in ['random', 'rdn', 'rd']:
            df_random = pd.read_sql_query(f"SELECT `prompt` FROM `prompt_examples` ORDER BY RAND() LIMIT 1", db_engine)
            prompt = df_random['prompt'].values[0]
        else: prompt = ' '.join(MSG_SLT[1:])

        if prompt in ['balance', 'bl', 'b', 'credit', 'credits', 'c', '余额', '额度', '剩余额度']:
            try:
                balance_json = stability_balance()
                if balance_json:
                    balance = balance_json.get('credits', '0')
                    # 显示小数点后两位
                    images_count = int(float(balance) * 5)
                    balance = f"{float(balance):.2f}"
                    send_msg(f"SD Credits 余额: {balance}\n大约可生成图片: {images_count} 张", chat_id)
            except: send_msg(f"当前SD余额查询失败", chat_id)
            return

        if prompt in ['models', 'model', 'm', 'engines', 'engine', 'e']:
            try:
                models_file = stability_engines()
                if models_file:
                    # 打开 models 文件
                    df = pd.read_csv(models_file)
                    # 选择需要的列
                    df_models = df['id'].to_list()
                    list_to_str = '\n'.join(df_models)
                    send_msg(f"SD当前可用模型:\n{list_to_str}", chat_id)
                    send_file(chat_id, models_file)
            except:
                send_msg(f"SD当前可用模型查询失败", chat_id)
            return

        try:
            file_list = stability_generate_image(prompt)
            if file_list:
                for file in file_list:
                    try:
                        send_img(chat_id, file, prompt)
                    except:
                        print(f"ERROR: msg_command() send_img({file}) FAILED")
            try:
                add_prompt_and_words(prompt)
            except Exception as e:
                print(f"FAILED add_prompt_and_words() {e}")
        except Exception as e:
            print(f"FAILED stability_generate_image() {e}")
        # NSFW content detected. Try running it again, or try a different prompt.

        return

    # chatpdf function
    elif MSG_SLT[0] in ['pdf', 'doc', 'txt', 'docx', 'csv', 'ppt', 'pptx', 'url', 'urls'] and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        try: 
            reply = qa.run(f"{query}\n Please reply with the same language as the question.")
            send_msg(reply.strip('\n').strip(), chat_id)
            translate_if_is_english(reply, chat_id)
        except Exception as e: send_msg(f"ERROR: ChatPDF 查询失败, 原因 :\n{e}", chat_id)
        return 

    # chatpdf function
    elif MSG_SLT[0] in ['outlier', 'oi', 'outlier-investor', 'outlierinvestor', 'ol'] and MSG_LEN >= 2:
        query = ' '.join(MSG_SLT[1:])
        try: 
            index_name = 'outlier-investor'
            # docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
            
            docsearch = Pinecone.from_existing_index(index_name, embeddings)
            
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = docsearch.similarity_search(query)
            reply = chain.run(input_documents=docs, question=query)
            send_msg(reply, chat_id)
            translate_if_is_english(reply, chat_id)
        except Exception as e: send_msg(f"ERROR: ChatPDF 查询失败, 原因 :\n{e}", chat_id)
        return 
    
    elif MSG_SLT[0] in ['revise', 'rv'] and MSG_LEN >= 2:
        prompt = ' '.join(MSG_SLT[1:])
        try:
            reply = chat_gpt_regular(f"Please help me to revise below English in a more native and polite way:\n{prompt}", chatgpt_key=openai_key, use_model='gpt-4')
            send_msg(reply, chat_id)
        except Exception as e: send_msg(f"ERROR: ChatGPT 查询失败, 原因 :\n{e}", chat_id)
        return 

    elif MSG_SLT[0] in ['midjourney', 'mid', 'midjourneyprompt'] and MSG_LEN >= 2:
        try:
            r = create_midjourney_prompt(' '.join(MSG_SLT[1:]))
            if r: send_msg(r, chat_id)
        except Exception as e: send_msg(f"ERROR: create_midjourney_prompt() FAILED: {e}", chat_id)
        return 

    is_owner = owner(from_id)

    if MSG_SLT[0].lower() in ['whitelistadd', 'wlad'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        input_from_id = str(MSG_SLT[1])
        try:
            r = update_chatgpt_whitelist(input_from_id)
            successful_info = f"SUCCESSFULLY added from_id: {input_from_id} into CHAT_GPT whitelist"
            failed_info = f"FALIED to add from_id: {input_from_id} into CHAT_GPT whitelist"
            if r:
                send_msg(successful_info, chat_id)
                send_msg(successful_info, input_from_id)
                send_msg(message_help, input_from_id)
            else:
                send_msg(failed_info, chat_id)
        except: print(f"ERROR : update_chatgpt_whitelist() failed.")
        return

    elif MSG_SLT[0] in ['whitelistdrop', 'wldp'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        input_from_id = str(MSG_SLT[1])
        try:
            r = drop_from_chatgpt_whitelist(input_from_id)
        except:
            print(f"FAILED drop {from_id} from whitelist")
        successful_info = f"SUCCESSFULLY dropped from_id: {input_from_id} from CHAT_GPT whitelist"
        failed_info = f"FALIED to drop from_id: {input_from_id} from CHAT_GPT whitelist"
        if r:
            send_msg(successful_info, chat_id)
        else:
            send_msg(failed_info, chat_id)
        return

    # add to email_whitelist
    elif MSG_SLT[0] in ['aew', 'add_email_whitelist', 'addemailwitelist'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        email_address = str(MSG_SLT[1])
        try:
            r = add_email_to_whitelist(email_address)
            if r: send_msg(f"SUCCESSFULLY add {email_address} to whitelist", chat_id)
        except: send_msg(f"FAILED add {email_address} to whitelist", chat_id)
        return

    # send sms to phone number
    elif MSG_SLT[0] in ['sms', 'send_sms', 'sendsms'] and from_id == bot_owner_chat_id and MSG_LEN > 2:
        phone_number = str(MSG_SLT[1])
        phone_book_dict = {'danli': '+16693234727', 'leo': '+19205369264'}
        if '+' not in phone_number and len(phone_number) == 10 and phone_number not in phone_book_dict:
            phone_number = '+1' + phone_number
        if phone_number in phone_book_dict:
            phone_number = phone_book_dict[phone_number]
        if not phone_number.startswith('+1'):
            send_msg(
                f"Only support sending SMS to US mobile phone number.", chat_id)
            return

        sms_content = ' '.join(MSG_SLT[2:140]+['\n\nNO_REPLY'])

        try:
            r = send_sms(sms_content, phone_number)
            if r:
                send_msg(
                    f"SUCCESSFULLY send sms to {str(MSG_SLT[1])} : {phone_number}, \n{r}", chat_id)
        except:
            send_msg(f"FAILED send sms to {phone_number}", chat_id)

        return

    # add email blacklist:
    elif MSG_SLT[0] in ['aeb', 'add_email_blacklist', 'addemailblacklist', 'blacklistemail', 'ble'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        email_from = str(MSG_SLT[1]).strip()
        try:
            with db_engine.connect() as conn:
                conn.execute(
                    f"UPDATE `email_records` SET `in_blacklist`=1 WHERE `email_address`='{email_from}'")
            send_msg(
                f"SUCCESSFULLY add \n\n{email_from} to blacklist", chat_id)
        except Exception as e:
            print(f"FAILED add_email_to_blacklist() {e}")
        return

    # add alice bot blacklist:
    elif MSG_SLT[0] in ['aab', 'add_alice_blacklist', 'addaliceblacklist', 'blacklistalice', 'bla'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        bl_conn = db_engine.connect()
        bl_conn.execute(
            f"UPDATE `alice_chat_history` SET `black_list`=1 WHERE `chat_id`='{MSG_SLT[1]}'")
        bl_conn.close()
        send_msg(f"SUCCESSFULLY added \n\n{MSG_SLT[1]} to blacklist", chat_id)
        return

    # remove alice bot blacklist:
    elif MSG_SLT[0] in ['rab', 'remove_alice_blacklist', 'removealiceblacklist', 'whitelistalice', 'wla'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        bl_conn = db_engine.connect()
        bl_conn.execute(
            f"UPDATE `alice_chat_history` SET `black_list`=0 WHERE `chat_id`='{MSG_SLT[1]}'")
        bl_conn.close()
        send_msg(
            f"SUCCESSFULLY removed \n\n{MSG_SLT[1]} from Alice blacklist", chat_id)
        return

    # send email_welcome to email_address
    elif MSG_SLT[0] in ['sew', 'send_email_welcome', 'sendemailwelcome'] and from_id == bot_owner_chat_id and MSG_LEN == 2:
        email_address = str(MSG_SLT[1]).strip()
        try:
            send_email(email_welcome, email_address,
                       email_subject='Welcome to ChatGPT Email Assistant')
            send_msg(
                f"SUCCESSFULLY send email_welcome to \n\n{email_address}", chat_id)
        except Exception as e:
            print(f"FAILED send_email_welcome() {e}")
        return

    # emoji translate function
    elif MSG_SLT[0] in ['emoji', 'emj', 'emo'] and MSG_LEN >= 2 and is_owner:
        prompt = ' '.join(MSG_SLT[1:])
        if debug:
            print(f"DEBUG: will generate emoji with {prompt}")
        try:
            new_prompt = f"You know exactly what each emoji means and where to use. I want you to translate the sentences I wrote into suitable emojis. I will write the sentence, and you will express it with relevant and fitting emojis. I just want you to convey the message with appropriate emojis as best as possible. I don’t want you to reply with anything but emoji. My first sentence is ( {prompt} ) "
            emj = chat_gpt(new_prompt)
        except Exception as e:
            print(f"FAILED emoji translate chat_gpt() {e}")
        if emj:
            try:
                send_msg(emj, chat_id)
            except Exception as e:
                print(f"FAILED emoji send_msg() {e}")
        return

    # common voice generate function
    elif MSG_SLT[0] in ['voice', 'audio', 'ad', 'vo'] and is_owner:
        prompt = ' '.join(MSG_SLT[1:])
        if debug:
            print(f"DEBUG: AZURE will generate voice with {prompt[:40]}")

        is_chinese = False if is_english(prompt) else True

        tts_file_name = generate_or_read_tts('ai_chat', prompt, is_chinese)
        if tts_file_name:
            send_audio(tts_file_name, chat_id)
        return

    # male voice generate function / 中文粤语男声
    elif MSG_SLT[0] in ['male_voice', 'male_audio', 'mv', 'ma', 'malevoice', 'maleaudio'] and is_owner:
        prompt = ' '.join(MSG_SLT[1:])
        if debug:
            print(f"DEBUG: AZURE will generate voice with {prompt[:40]}")

        is_chinese = False if is_english(prompt) else True

        tts_file_name = generate_or_read_tts_male(
            'ai_chat', prompt, is_chinese)
        if tts_file_name:
            send_audio(tts_file_name, chat_id)
        return

    # female voice generate function / 中文陕西话女声
    elif MSG_SLT[0] in ['female_voice', 'female_audio', 'fa', 'fv', 'femalevoice', 'femaleaudio', 'fm'] and is_owner:
        prompt = ' '.join(MSG_SLT[1:])
        if debug:
            print(f"DEBUG: AZURE will generate voice with {prompt[:40]}")

        is_chinese = False if is_english(prompt) else True

        tts_file_name = generate_or_read_tts_female(
            'ai_chat', prompt, is_chinese)
        if tts_file_name:
            send_audio(tts_file_name, chat_id)
        return

    # voice generate function
    elif MSG_SLT[0] in ['leo_voice', 'leovoice', 'lv', 'la', 'leoaudio', 'leo_audio'] and from_id == bot_owner_chat_id and MSG_LEN < 500:
        prompt = ' '.join(MSG_SLT[1:])
        if debug:
            print(f"DEBUG: will generate voice with {prompt[:40]}")

        tts_file_name = ''
        if is_english(prompt):
            try:
                tts_file_name = generate_or_read_tts_11_labs(
                    folder='leo_voice', content=prompt, voice_id='YEhWVRrlzrtA9MzdS8vE')
            except Exception as e:
                print(f"FAILED generate_or_read_tts_11_labs() {e}")
            if tts_file_name:
                send_audio(tts_file_name, chat_id)
            return
        else:
            return send_msg(f"Sorry, Leo's voice only support English for now.", chat_id)

    # translate chinese to english and then generate audio with my voice
    elif MSG_SLT[0] in ['ts', 'translate', 'tl'] and from_id == bot_owner_chat_id:

        prompt = ' '.join(MSG_SLT[1:])

        user_prompt='''Dillon Reeves, a seventh grader in Michigan, is being praised as a hero for preventing his school bus from crashing after his bus driver lost consciousness. Reeves was seated about five rows back when the driver experienced "some dizziness" and passed out, causing the bus to veer into oncoming traffic. Reeves jumped up from his seat, threw his backpack down, ran to the front of the bus, grabbed the steering wheel and brought the bus to a stop in the middle of the road. Warren police and fire departments responded to the scene within minutes and treated the bus driver, who is now stable but with precautions and is still undergoing testing and observation in the hospital. All students were loaded onto a different bus to make their way home. Reeves' parents praised their son and called him \'our little hero.\''''
        assistant_prompt='''Dillon Reeves 是一名来自密歇根州的七年级学生，因为在校车司机失去意识后成功阻止了校车发生事故而被称为英雄。当时，司机出现了“一些眩晕”并昏倒，导致校车偏离行驶道驶入迎面驶来的交通流中。当时 Reeves 坐在车子后面大约五排的位置，他迅速从座位上站起来, 扔掉背包并跑到车前, 抓住方向盘, 让校车在道路中间停了下来。Warren 警察和消防部门在几分钟内赶到现场, 对校车司机进行救治。司机目前已经稳定下来, 但仍需密切观察并在医院接受检查。所有学生后来被安排上另一辆校车回家。Reeves 的父母赞扬了儿子，并称他是“我们的小英雄”'''

        try: reply = chat_gpt_full(prompt, system_prompt = translation_prompt, user_prompt=user_prompt, assistant_prompt=assistant_prompt, dynamic_model= 'gpt-4', chatgpt_key = openai_key)
        except Exception as e: return

        try: send_msg(reply, chat_id)
        except Exception as e: print(f"ERROR : translation send_msg() failed : {e}")

        if len(reply.split()) > 1000: return

        is_chinese = False if is_english(reply) else True

        tts_file_name = generate_or_read_tts_male('ai_chat', reply, is_chinese)
        if tts_file_name: send_audio(tts_file_name, chat_id)
        return

    # note find/search function
    elif MSG_SLT[0] in ['note', 'nt', 'notes', 'nts'] and MSG_LEN >= 3 and is_owner:
        if not owner(from_id):
            return

        if MSG_SLT[1] in ['find', 'search', 'fd', 'sc']:
            key_words = ' '.join(MSG_SLT[2:])
            try:
                notes_memos_list = search_table_notes_and_memos(key_words)
                if notes_memos_list:
                    for n in notes_memos_list:
                        send_msg(n, chat_id)
            except Exception as e:
                print(f"ERROR : search_table_notes_and_memos() failed: {e}")
            return
        if MSG_SLT[1] in ['update', 'add', 'ad', 'up', 'ud', 'upd', 'insert']:
            input_notes = ' '.join(MSG_SLT[2:])
            try:
                r = update_table_notes_and_memos(input_notes)
                if r:
                    send_msg(
                        f"Successfully inserted.\ntable: notes_and_memos", chat_id)
            except Exception as e:
                print(f"ERROR : update_table_notes_and_memos() failed: {e}")
            return

    elif MSG_SLT[0] == 'otp' and MSG_LEN == 2 and is_owner:
        if not owner(from_id):
            return

        if MSG_SLT[1] in ['list', 'lt', 'ls', 'all', 'read', 'rd']:
            try:
                otp_list = pd.read_sql_query(
                    f"SELECT `app_name` FROM `one_time_passcode_key`", db_engine)['app_name'].tolist()
                if otp_list:
                    send_msg('\n'.join(otp_list), chat_id)
            except Exception as e:
                print(f"ERROR : read_otp_list() failed: {e}")
            return

        try:
            r = read_otp(MSG_SLT[1])
            if r:
                send_msg(r, chat_id)
        except Exception as e:
            print(f"ERROR : read_otp() failed: {e}")
        return

    elif MSG_SLT[0] in ['synonyms', 'syn', 'sno'] and MSG_LEN == 2 and is_owner:
        input_text = MSG_SLT[1]
        word_dict = st_find_ranks_for_word(input_text)
        if not word_dict:
            return
        if word_dict.get('synonyms'):
            send_msg(f"CURRENT SYNONYMS: \n{word_dict.get('synonyms')}")

        try:
            synonyms = chat_gpt(
                f"You are a highly respected English teacher who is not only a language master but also knows synonyms of every word, when I send a curten word to you, you will reply maximum 5 synonyms words to me, each synonym should be one single word, not a phrase, and not using word that contains - as a connector. For example, I send (ostentatious), you reply: showy pretentious pompous bombastic grandiloquent. Now I send ({input_text}), what you should reply?")
            if not synonyms:
                return
        except Exception as e:
            print(f"ERROR : synonyms chat_gpt() failed: {e}")

        try:
            updated_synonyms = append_synonyms_to_database(
                input_text, synonyms)
            if updated_synonyms:
                send_msg(f"UPDATED SYNONYMS: \n{updated_synonyms}")
        except:
            pass
        return

    elif MSG_SLT[0] in ['bing'] and MSG_LEN >= 2 and is_owner:
        query = ' '.join(MSG_SLT[1:])
        try: create_news_and_audio_from_bing_search(query)
        except Exception as e: print(f"ERROR : create_news_and_audio_from_bing_search() failed: {e}")
        return

    elif MSG_SLT[0] in ['wolfram', 'wolframalpha', 'wa'] and MSG_LEN >= 2 and is_owner:
        query = ' '.join(MSG_SLT[1:])
        try: 
            reply = wolfram.run(query)
            send_msg(reply, chat_id)
        except Exception as e: print(f"ERROR : wolfram.run() failed: {e}")
        return 

    elif MSG_SLT[0] in ['wikipedia', 'wiki', 'wp', 'wk', 'wf'] and MSG_LEN >= 2 and is_owner:
        query = ' '.join(MSG_SLT[1:])
        try: 
            reply = wikipedia.run(query)
            # if debug: print(f"DEBUG: wikipedia.run() reply: \n\n{reply}\n\n")
            SAVE_FOLDER = 'json_datas/files/tg_received/'
            # Remove special character form query string to save as file name
            query = re.sub('[^A-Za-z0-9]+', '', query)
            # Remove space from query string to save as file name
            query = query.replace(' ', '')
            # Save reply to a text file under SAVE_FOLDER and name as query
            with open(f"{SAVE_FOLDER}{query}.txt", 'w') as f: f.write(reply)
            # Send the text file to the user
            send_file(chat_id, f"{SAVE_FOLDER}{query}.txt")
        except Exception as e: print(f"ERROR : wikipedia.run() failed: {e}")
        return 
    
    elif MSG_SLT[0] in ['twitter', 'tw'] and MSG_LEN >= 2 and is_owner:
        msg_text = ' '.join(MSG_SLT[1:])
        prompt = f"请为以下内容写一个精简的中文 Tweet. 只需回复内容, 不需要任何前缀标识。\n\n{msg_text}"
        try:
            reply = chat_gpt_regular(prompt) 
            send_msg(f"tweet {reply}", chat_id)
        except Exception as e: send_msg(f"ERROR: Tweet 生成失败: \n{e}", chat_id)
        return
    
    elif MSG_SLT[0] in ['tweet', 'tw'] and MSG_LEN >= 2 and is_owner:
        try: 
            tweet_id = twitter_v1_creat_tweet(' '.join(MSG_SLT[1:]))
            send_msg(f"推特发送成功:\n\nhttps://twitter.com/preangelleo/status/{tweet_id}", chat_id)
        except Exception as e: send_msg(f"ERROR: 推特发送失败: \n{e}", chat_id)
        return

    conversation_id = 0
    try: conversation_id = save_user_chat_history(**kwargs)
    except Exception as e: print(f"ERROR : save_user_chat_history() failed: {e}")

    try: reply = call_chatgpt_to_reply(msg_text, chat_id, conversation_id)
    except Exception as e: print(f"ERROR : call_chatgpt_to_reply() FAILED from msg_command() : {e}")

    return

def convert_mp3_to_wav(mp3_file_path):
    wav_file_path = mp3_file_path.replace('.mp3', '.wav')
    # Load the mp3 file
    sound = AudioSegment.from_file(mp3_file_path)
    # Set the parameters for the output WAV file
    sample_width = 2  # 16-bit samples
    frame_rate = 16000  # 16 kHz
    # Convert the sound to a mono (single channel) AudioSegment
    sound = sound.set_channels(1)

    # Export the sound as a WAV file with the specified parameters
    sound.export(wav_file_path, format="wav", parameters=["-f", "wav", "-ac", "1", "-ar", "16000"])
    return wav_file_path

def from_voice_to_text(audio_file_path):
    wave_file_path = convert_mp3_to_wav(audio_file_path)

    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    audio_config = speechsdk.AudioConfig(filename=wave_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()
    return result.text

def deal_with_voice_to_text(file_id, file_unique_id):
    if debug: print(f"DEBUG: deal_with_voice_to_text()")
    text = ''  # Create an empty text
    # Create local file name to store voice telegram message
    local_file_folder_name = f"json_datas/tg_voice/{file_unique_id}.mp3"
    # Get the file path of the voice message using the Telegram Bot API
    file_path_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    file_path_response = requests.get(file_path_url).json()
    file_path = file_path_response["result"]["file_path"]
    # Download the voice message to your Ubuntu folder
    voice_message_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    try:
        with open(local_file_folder_name, "wb") as f:
            response = requests.get(voice_message_url)
            f.write(response.content)
            text = from_voice_to_text(local_file_folder_name)
    except: print(f"ERROR : deal_with_voice_to_text() FAILED, text: {text}")
    return text

def check_bot_updates():
    if debug: print(f"DEBUG: check_bot_updates()")
    global global_UID
    r = getUpdates(global_UID + 1)
    if r.status_code != 200: return
    updates = r.json()['result']

    for tg_msg in updates:
        if ('update_id' not in tg_msg) or ('message' not in tg_msg): continue
        update_id = tg_msg['update_id']
        if global_UID == update_id: continue
        global_UID = update_id

        is_owner = owner(tg_msg['message']['from']['id'])
        if debug: print(f"DEBUG: check_bot_updates() {tg_msg['message']['from']['first_name']} is_owner: {is_owner}, from_id : {tg_msg['message']['from']['id']}")

        chat_id = tg_msg['message']['chat']['id']

        # if debug: print(json.dumps(tg_msg, indent=2))
        if 'text' not in tg_msg['message']:
            msg_text = ''
            
            if 'document' in tg_msg['message']:
                try:
                    file_id = tg_msg['message']['document']['file_id']

                    if debug: print(f"DEBUG: document file_id: {file_id}")
                    # use the Telegram bot API to get the file path
                    file_path = tg_get_file_path(file_id)
                    file_path = file_path.get('file_path', '')
                    if not file_path: continue

                    if debug: print(f"DEBUG: document file_path: {file_path}")
                    SAVE_FOLDER = 'json_datas/files/tg_received/'

                    file_name = os.path.basename(file_path)
                    save_file_path = f'{SAVE_FOLDER}{file_name}'
                    file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
                    with open(save_file_path, 'wb') as f: f.write(requests.get(file_url).content)

                    fire_type = ''
                    if file_name.endswith('.pdf'):
                        fire_type = 'pdf'
                        loader = PyPDFLoader(save_file_path)
                    if file_name.endswith('.txt'):
                        fire_type = 'txt'
                        loader = TextLoader(save_file_path, encoding='utf8')
                    if file_name.endswith('.docx') or file_name.endswith('.doc'):
                        fire_type = 'doc'
                        loader = UnstructuredWordDocumentLoader(save_file_path)
                    if file_name.endswith('.pptx') or file_name.endswith('.ppt'):
                        fire_type = 'ppt'
                        loader = UnstructuredPowerPointLoader(save_file_path)
                    if file_name.endswith('.csv'):
                        fire_type = 'csv'
                        loader = CSVLoader(save_file_path)

                    if fire_type:
                        documents = loader.load()
                        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                        texts = text_splitter.split_documents(documents)
                        
                        db = Chroma.from_documents(texts, embeddings)
                        retriever = db.as_retriever()
                        
                        global qa
                        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
                        
                        send_msg(f"{fire_type.upper()} 文档已收到, 如果想要咨询了解本文档的相关内容, 请使用 doc 命令前缀加上您的问题。(doc 命令后面需要有空格)", chat_id)

                        query = "请为该文档写一段中文 Tweet，只需回复内容，不需要任何前缀标识。"
                        r = qa.run(query)
                        if r: send_msg(r, tg_msg['message']['chat']['id'])
                        # translate_if_is_english(r, tg_msg['message']['chat']['id'])
                    else: send_msg(f"File {file_name} saved to {SAVE_FOLDER} as:\n{save_file_path}", chat_id)

                except Exception as e: send_msg(f"ERROR: 电报机器人处理文件失败: \n{e}", chat_id)
                continue 

            if 'photo' in tg_msg['message'] and tg_msg['message']['from']['id'] == tg_msg['message']['chat']['id']:
                if debug: print(f"DEBUG: photo in tg message and is_direct_msg...")
                try:
                    # specify the folder path where you want to save the received images
                    SAVE_FOLDER = 'json_datas/img/tg_received/'
                    file_id = tg_msg.get('message').get('photo')[-1].get('file_id')
                    if debug: print(f"DEBUG: photo file_id: {file_id}")
                    # use the Telegram bot API to get the file path
                    file_path = tg_get_file_path(file_id)
                    file_path = file_path.get('file_path', '')
                    if not file_path: continue
                    if debug: print(f"DEBUG: photo file_path: {file_path}")
                except Exception as e: continue

                # construct the full URL for the file
                file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
                # get the content of the file from the URL
                file_content = requests.get(file_url).content
                # save the file to the specified folder with the same file name as on Telegram
                file_name = file_path.split('/')[-1]
                save_path = os.path.join(SAVE_FOLDER, file_name)
                if debug: print(f"DEBUG: photo save_path: {save_path}")
                with open(save_path, 'wb') as f: f.write(file_content)

                try: msg_text = replicate_img_to_caption(save_path, chat_id=tg_msg['message']['chat']['id'])
                except Exception as e: print(f"FAILED replicate_img_to_caption: {e}")
                if not msg_text: continue

                send_msg(msg_text, chat_id=tg_msg['message']['chat']['id'])

                continue

            if 'voice' in tg_msg['message'] and is_owner:
                try: msg_text = deal_with_voice_to_text(file_id=tg_msg['message']['voice'].get('file_id'), file_unique_id=tg_msg['message']['voice'].get('file_unique_id'))
                except: continue
                if not msg_text: continue

                send_msg(msg_text, chat_id=tg_msg['message']['chat']['id'])
                if 'adam' not in msg_text.lower(): continue

                tg_msg['message']['text'] = msg_text.replace('adam,', '').replace('adam', '').strip()

        user_name = tg_msg['message']['from'].get('username', 'none') if tg_msg['message'].get('from') else 'none'
        msg_text = tg_msg['message'].get('text')
        msg_text = ' '.join([tg_msg['message'].get('text'), tg_msg['message']['reply_to_message'].get('text')]) if 'reply_to_message' in tg_msg['message'] else msg_text

        msg_text = msg_text.strip('\n').strip()
        msg_text = msg_text.replace('?', '')
        msg_text = msg_text.replace('%', ' percent')
        msg_text = msg_text.replace("'", '')
        msg_text = msg_text.replace('"', '')

        if not msg_text: continue

        try:
            kwargs = {
                "chat_id": tg_msg['message']['chat']['id'],
                "from_id": tg_msg['message']['from']['id'],
                "message_id": tg_msg['message']['message_id'],
                "message_from_first_name": tg_msg['message']['from'].get('first_name', 'none'),
                "message_from_last_name": tg_msg['message']['from'].get('last_name', 'none'),
                "message_from_username": user_name,
                "message_text": msg_text,
            }
        except: continue

        try: msg_command(**kwargs)
        except: continue
    return


if __name__ == '__main__':
    exception_sleep_time = 10
    if debug: print(f"DEBUG: @lgg_chatgpt_bot started, ali_101_major...")
    i = 0
    while True:
        i += 1
        time.sleep(1)
        try: check_bot_updates()
        except Exception as e: send_msg(f'ERROR: i = {i} check_bot_updates FAILED:\n\n{e}', chat_id=bot_owner_chat_id)
