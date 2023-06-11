from chatgpt_bot import *
from c101binance import get_balances_realtime_value_dataframe, creat_task_for_db_withdraw_task, get_deposit_address, get_withdraw_and_deposit_network
import matplotlib.pyplot as plt
from streamlit.components.v1 import html
# import mpld3

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state='expanded')

with open('my_config/st_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if place_holder:
    input_text = ''
    synonyms_list = ''
    word_dict = {}
    notes = NOTES_DICT
    for s in ['current_word', 'is_sealed', 'is_chinese', 'is_english', 'db_dict','authentication_status', 'current_chat_id']:
        if s not in st.session_state:
            st.session_state['authentication_status'] = False
            st.session_state['current_word'] = False
            st.session_state['is_chinese'] = False
            st.session_state['is_english'] = True
            st.session_state['is_sealed'] = False
            st.session_state['db_dict'] = None
            st.session_state['current_chat_id'] = None

name, authentication_status, username = authenticator.login('Login', 'sidebar')

if authentication_status:
    st.session_state['authentication_status'] = True
elif authentication_status == False:
    st.sidebar.error('Username/password is incorrect')
elif authentication_status == None:
    st.sidebar.warning('Please enter your username and password')

if place_holder:
    top_radio_select = st.empty()
    top_radio_select_list = ['DICTIONARY', 'RADOM', 'M2W', 'BING', 'MIDJOURNEY']
    if st.session_state['authentication_status']: top_radio_select_list += ['CHAT_GPT', 'AIGC', 'UPDATE', 'REPORT', 'BINANCE', 'EXPENDITURE', 'DATABASE']
    top_input = st.empty()
    news_upload_button = st.empty()
    channel_choosed = top_radio_select.radio(label=' ', options = top_radio_select_list, index=0, horizontal=True)
    if channel_choosed in ['DICTIONARY', 'UPDATE']:
        st.session_state['current_word'] = top_input.text_input(f"Input a word and press ENTER:", value = '', key='1')

        # Languare detecting
        word_language = detect_language(st.session_state['current_word'])
        if word_language and word_language == 'Chinese': 
            st.session_state['is_chinese'] = True
            st.session_state['is_english'] = False
        else:
            st.session_state['is_chinese'] = False
            st.session_state['is_english'] = True                    

if channel_choosed == 'MIDJOURNEY':
    article_info = st.empty()

    # Path to the directory containing the PNG files
    directory_path = "json_datas/discord_img"

    # Get the list of PNG files in the directory and sort by modification time in descending order
    png_files = sorted([f for f in os.listdir(directory_path) if f.endswith('.png')], key=lambda f: os.path.getmtime(os.path.join(directory_path, f)), reverse=True)
    png_files = png_files[:30]
    # Divide the PNG files into groups of three
    png_groups = [png_files[i:i+3] for i in range(0, len(png_files), 3)]

    # Display each group of three PNG files in a row of three columns
    for group in png_groups:
        col1, col2, col3 = st.columns(3)
        with col1:
            if len(group) > 0:
                st.image(os.path.join(directory_path, group[0]), use_column_width=True)
        with col2:
            if len(group) > 1:
                st.image(os.path.join(directory_path, group[1]), use_column_width=True)
        with col3:
            if len(group) > 2:
                st.image(os.path.join(directory_path, group[2]), use_column_width=True)

    # Center the images on the page
    st.markdown('<style>div.row-widget.stHorizontal {flex-direction:row;justify-content:center;}</style>', unsafe_allow_html=True)

if channel_choosed == 'BINANCE':
    action_side = st.selectbox("What you want to do from Binance?", ['DEPOSIT', 'WITHDRAW'], index=0)

    if action_side == 'DEPOSIT':
        coin = st.text_input("input the COIN symbol you want to deposit:", key='1')
        
        if coin:
            wd_dp = get_withdraw_and_deposit_network(coin)
            if wd_dp and type(wd_dp) is not str: 
                _, network_list = wd_dp
                if network_list:
                    try: eth_index = network_list.index('ETH')
                    except: eth_index = 0
                    chose_network = st.selectbox("choose the NETWORK for the COIN you want to deposit:", network_list, index=eth_index, key='2')
                    if chose_network:
                        data = get_deposit_address(coin, chose_network, wd_dp)
                        if data and type(data) is dict:
                            st.code(f"Address for depositing {data.get('coin')} on {chose_network} network to binance is: {data.get('address')}")

    if action_side == 'WITHDRAW':

        df = pd.read_sql_query(f"SELECT eth_address FROM db_address_watchlist WHERE is_mine=1 AND is_deleted=0", remote_db_engine)
        ADDRESS_LIST = df['eth_address'].tolist()

        to_address = st.selectbox("to_address", ['OTHER_ADDRESS']+ADDRESS_LIST, index=0)
        if to_address == 'OTHER_ADDRESS':
            to_address = ''
            input_address = st.text_input("input an ETH address first", key='1')
            if input_address:
                try: 
                    to_address = web3.toChecksumAddress(input_address)
                except Exception as e:
                    print(f"ERROR : web3.toChecksumAddress() failed.")
                    st.error(f"You need to input a legit ETH address here.")

        if to_address: 
            st.code(f"{to_address} : ADDRESS checked.")
            df = get_balances_realtime_value_dataframe()
            coin_balances = {row['coin']: row['balance'] for _, row in df.iterrows()}
            with st.expander(f"click for BALANCES details......"):
                st.write(coin_balances)
            coin_balance_list = list(coin_balances.keys())
            usdt_index = coin_balance_list.index('USDT')
            chose_coin = st.selectbox("choose the coin you want to withdraw:", coin_balance_list, index=usdt_index, key='5')

            if chose_coin:
                chose_coin_balance = coin_balances[chose_coin]
                st.code(f"{chose_coin} balance is: {chose_coin_balance}")
                amount = st.text_input("withdraw amount", key='2')
                if amount:
                    try: 
                        amount = float(amount)
                        if amount <= chose_coin_balance: 
                            memo = st.text_area("memo", key='3')
                            otp_code = st.text_input("one time passcode", key='4')
                            if otp_code:
                                is_valid = validate_otp('st_binance', otp_code)
                                if is_valid:
                                    if st.button("CONFIRM WITHDRAW") and memo:
                                        try:
                                            with_draw_task_added = creat_task_for_db_withdraw_task(chose_coin, amount, to_address, bot_owner_chat_id, 'eth', memo)
                                            if with_draw_task_added: st.write(with_draw_task_added)
                                        except Exception as e: st.error(e)
                                else: st.error(f"ERROR : one time passcode WRONG.")
                        else: st.error(f"Your balance is INSUFFICIENT for this withdraw.")
                    except: 
                        st.error(f"You need to input a NUMBER here")

if channel_choosed == 'REPORT':
    report_info = st.empty()
    if st.session_state['authentication_status']:
        try: report, today_words_count, today_essential_words_list, df_category_list, sealed_words_list = st_english_study_report()
        except: report_info.error(f"Reading REPORT failed!")
        else:
            report_info.info(report)
            if today_essential_words_list:
                db_dict = st_find_ranks_for_synonyms(today_essential_words_list)
                if db_dict and type(db_dict) is dict:
                    synonyms_list = [f"{k}({int(v)})" for k, v in db_dict.items() if not math.isnan(v)]
                    if synonyms_list:
                        with st.expander(f"Click to CHECK today's essential words with ranks"):
                            st.caption(f"{' | '.join(synonyms_list)}")
            notes
    else: report_info.info("OWNER ONLY!")

if place_holder:
    column_left, column_mid = st.columns(2)
    audio_word = st.empty()
    chatgpt_info = st.empty()
    synonyms_info = st.empty()
    audio_gpt = st.empty()

    external_url = st.empty()
    detail_expander = st.empty()

    sentence_info = st.empty()
    sentence_audio = st.empty()
    chinese_search = st.empty()
    origin_info = st.empty()
    note_info = st.empty()
    sentences_from_db_expander = st.empty()
    aler_message_1 = st.empty()
    choose_for_next_command = st.empty()
    aler_message_2 = st.empty()
    
    next_rand_word_button = st.empty()
    if st.session_state['authentication_status']:
        value_input = st.empty()
        confirm_button = st.empty()
    if st.session_state['authentication_status'] and channel_choosed == 'UPDATE' and st.session_state['is_english']:
        db_update_container = st.empty()

if channel_choosed == 'RADOM': 
    df_random = pd.read_sql_query(f"SELECT `word` FROM `db_daily_words` WHERE `rank` > 6666 ORDER BY RAND() LIMIT 1", db_engine)

    st.session_state['current_word'] = df_random['word'].values[0]

    st.button('NEXT RANDOM WORD')

def get_dictionary(input_text):
    responsed_content = ''

    if st.session_state.get('is_chinese'):
        returned_for_chinese = st_check_from_chinese(input_text)
        if not returned_for_chinese: return
        with chinese_search.container():
            for k, v in returned_for_chinese.items():
                    st.title(k)
                    for ke, va in v.items():
                        st.code(ke, language='python')
                        try:
                            tts_file_name = generate_or_read_tts(folder = 'word_tts', content = k)
                            if tts_file_name:
                                try:
                                    with open(tts_file_name, 'rb') as tts_audio: st.audio(tts_audio)
                                except: pass
                        except: pass
                        st.success(va)
        return 
    if not st.session_state.get('is_english'): return

    word_dict = st_find_ranks_for_word(input_text)
    if not word_dict: 
        try: output_text = chat_gpt_word_correction(input_text, chatgpt_key=openai_key)
        except: return
        if not output_text: return
        st.code(f"CHATGPT replied: {output_text}")
        if len(output_text.split()) == 1: word_dict = st_find_ranks_for_word(output_text)
        if not word_dict: return

    input_text = word_dict.get('word')
    if not input_text: return

    if word_dict.get('sealed', ''): st.session_state['is_sealed'] = True
    else: st.session_state['is_sealed'] = False

    word_category = [key.upper() for key, value in word_dict.items() if value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
    word_category_str = ' / '.join(word_category)
    
    responsed_content = word_dict.get('chat_gpt_explanation')
    
    if st.session_state['is_sealed']:
        column_left.title(input_text.upper())
    elif word_category and responsed_content:
        column_left.title(input_text.capitalize())
    else: column_left.title(input_text.lower())

    with column_mid:
        phonetic = 'NONE' if not word_dict.get('us-phonetic') else word_dict.get('us-phonetic') 
        category = word_category_str if word_category_str else word_dict.get('tag') if word_dict.get('tag') else 'NONE'
        st.metric(label=phonetic, value=f"Rank: {word_dict.get('rank', 'NONE')}", delta=category)

    # tts_file_name = generate_or_read_tts_11_labs(folder = 'word_tts', content = input_text)
    tts_file_name = generate_or_read_tts(folder = 'word_tts', content = input_text)
    if tts_file_name:
        try:
            with open(tts_file_name, 'rb') as tts_audio: audio_word.audio(tts_audio)
        except: pass

    if responsed_content:
        chatgpt_info.success(f"EXPLANATION from ChatGPT: \n\n{responsed_content}")
        tts_file_name = generate_or_read_tts_11_labs(folder = 'sentences_tts', content = responsed_content)
        # tts_file_name = generate_or_read_tts(folder = 'sentences_tts', content = responsed_content)
        if tts_file_name:
            try:
                with open(tts_file_name, 'rb') as tts: audio_gpt.audio(tts)
            except: pass

    if not responsed_content:
        try:
            responsed_content = chat_gpt_regular(f"What is the English explanation of {input_text}")
            if responsed_content:
                chatgpt_info.success(f"EXPLANATION from ChatGPT: \n\n{responsed_content}")
                tts_file_name = generate_or_read_tts_11_labs(folder = 'sentences_tts', content = responsed_content)
                if tts_file_name:
                    try:
                        with open(tts_file_name, 'rb') as tts: audio_gpt.audio(tts)
                    except: pass
                try: update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, 'chat_gpt_explanation', responsed_content)
                except: pass
        except: pass

    if word_dict.get('synonyms'): synonyms_info.code(f"SYNONYMS: {word_dict.get('synonyms')}")

    yurl =  f"http://mobile.youdao.com/dict?le=eng&q={input_text}"
    youdao_url = f"[Youdao]({yurl})"
    gurl = f'https://translate.google.com/?sl=en&tl=zh-CN&text={input_text}%0A&op=translate'
    google_url = f"[Google Translate]({gurl})"
    surl = f"https://www.google.com/search?q={input_text}"
    search_url = f"[Google Search]({surl})"
    purl = f"https://www.playphrase.me/#/search?q={input_text}"
    playphrase_url = f"[Playphrase]({purl})"
    external_link = ' | '.join([youdao_url, google_url, search_url, playphrase_url])
    external_url.write(external_link)

    with detail_expander.expander(f"Click for DETAILS of {input_text}......"):
        for k, v in word_dict.items():
            if v and type(v) is str and v.lower() != 'none' and k not in ['word', 'us-phonetic', 'catogory', 'synonyms', 'note', 'origin', 'gre', 'toefl', 'sat', 'gmat', 'chat_gpt_explanation']:
                word_key, word_value = st.columns([1,9])
                word_key.write(f"{E2C_DICT.get(k)}:")
                word_value.write(v)

        try:
            more_words = st_check_for_more(input_text)
            if more_words: 
                more_words = {k: v for k , v in more_words.items() if k.lower() != input_text.lower()}
                if more_words: more_words
        except: pass
    return input_text, word_dict, responsed_content

# Function to create a download link for a DataFrame
def create_download_link(df, title = "Download CSV file", filename = "table_name.csv"):  
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'data:file/csv;base64,{b64}'
    st.markdown(f'<a href="{href}" download="{filename}">{title}</a>', unsafe_allow_html=True)


# dictionary, random and update
if st.session_state['current_word'] and channel_choosed in ['DICTIONARY', 'RADOM', 'UPDATE']:
    input_text = st.session_state['current_word']
    word_dict_key_list = ['chinese', 'chat_gpt_explanation', 'us-phonetic', 'origin', 'synonyms', 'phrase', 'tag', 'derivative', 'relevant', 'note', 'memo', 'scenario', 'sentence', 'toefl', 'gre', 'gmat', 'sat', 'sealed']
    if len(input_text.split()) == 1:
        dictionary_return = get_dictionary(input_text)
        if dictionary_return:
            input_text, word_dict, responsed_content = dictionary_return
            if st.session_state['authentication_status'] and channel_choosed in ['UPDATE']:
                with db_update_container.container():
                    update_success_info = st.empty()
                    priority_show = ['chinese', 'synonyms']
                    priority_show_columns = ['us-phonetic', 'toefl', 'gre', 'gmat', 'sat', 'sealed']
                    priority_show_columns_1 = ['tag', 'phrase', 'derivative', 'relevant', 'sat']
                    priority_show_1 = ['memo', 'scenario', 'sentence', 'chat_gpt_explanation', 'note', 'origin']
                    for k, v in word_dict.items():
                        if k in priority_show: 
                            new_value = st.text_input(f"{k}:", value=v, key=hash_md5(k+str(v)))
                            
                            if k == 'chinese' and st.button('CONFIRM CHANGE', key=hash_sha256(k+str(v))):
                                new_value = new_value.replace("，", "、")
                                r = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, k, new_value)
                                if r: update_success_info.info(f'{k.upper()} was just UPDATED.')

                            if k == 'synonyms':
                                col1, col2 = st.columns(2)
                                if col1.button('CONFIRM CHANGE', key=hash_sha256(k+str(v))):
                                
                                    r = manually_update_synonyms_to_database(input_text, new_value)
                                    if r: synonyms_info.code(f"SYNONYMS: {r}")

                                if col2.button('UPDATE SYNONYMS FROM CHATGPT', key=hash_sha256(k+str(v)+'1')):
                                    new_synonyms = ''
                                    try: new_synonyms = chat_gpt_word_synonyms(input_text, chatgpt_key = openai_key)
                                    except Exception as e: synonyms_info.error(f"ERROR : synonyms update from chat_gpt() failed: \n{e}")
                                    
                                    if new_synonyms:
                                        try: 
                                            updated_synonyms = append_synonyms_to_database(input_text, new_synonyms)
                                            if updated_synonyms: synonyms_info.code(f"UPDATED SYNONYMS: {updated_synonyms}")
                                        except: pass

                    i = 0
                    columns_index = st.columns(len(priority_show_columns))
                    for k, v in word_dict.items():
                        if k in priority_show_columns: 
                            with columns_index[i]:
                                i += 1
                                new_value = st.text_input(f"{k}:", value=v, key=hash_md5(k+str(v)+str(i)))
                                dict_edit_confirmed = st.button('CONFIRM CHANGE', key=hash_sha256(k+str(v)+str(i)))
                                if dict_edit_confirmed:
                                    r = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, k, new_value)
                                    if r: update_success_info.info(f'{k.upper()} was just UPDATED.')
                    x = 0
                    columns_index_1 = st.columns(len(priority_show_columns_1))
                    for k, v in word_dict.items():
                        if k in priority_show_columns_1: 
                            with columns_index_1[x]:
                                x += 1
                                new_value = st.text_input(f"{k}:", value=v, key=hash_md5(k+str(v)+str(x)))
                                dict_edit_confirmed = st.button('CONFIRM CHANGE', key=hash_sha256(k+str(v)+str(x)))
                                if dict_edit_confirmed:
                                    r = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, k, new_value)
                                    if r: update_success_info.info(f'{k.upper()} was just UPDATED.')
                    for k, v in word_dict.items():
                        if k in priority_show_1: 
                            new_value = st.text_input(f"{k}:", value=v, key=hash_md5(k+str(v)))
                            dict_edit_confirmed = st.button('CONFIRM CHANGE', key=hash_sha256(k+str(v)))
                            if dict_edit_confirmed:
                                r = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, k, new_value)
                                if r: update_success_info.info(f'{k.upper()} was just UPDATED.')
                    with st.expander(f"Click for MORE columns......"):
                        for k, v in word_dict.items():
                            if k in priority_show + priority_show_columns + priority_show_columns_1 + priority_show_1: continue
                            new_value = st.text_input(f"{k}:", value=v, key=hash_md5(k+str(v)))
                            dict_edit_confirmed = st.button('CONFIRM CHANGE', key=hash_sha256(k+str(v)))
                            if dict_edit_confirmed:
                                r = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, k, new_value)
                                if r: update_success_info.info(f'{k.upper()} was just UPDATED.')

            else:
                note = word_dict.get('note', '') 
                if not note and st.session_state['authentication_status']:
                    try: note = chat_gpt_word_synonyms(input_text, chatgpt_key = openai_key)
                    except: pass
                    if note:
                        try:
                            update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, 'note', note)
                            aler_message_1.info('NOTE was just updated')
                        except: pass
                if note: 
                    # note_info.code(note, language='python')
                    if not word_dict.get('synonyms', ''):
                        try: 
                            updated_synonyms = append_synonyms_to_database(input_text, note)
                            if updated_synonyms: synonyms_info.code(f"SYNONYMS: {updated_synonyms}")
                        except: pass

                origin = word_dict.get('origin', '') 
                if not origin and st.session_state['authentication_status']:
                    try: origin = chat_gpt_regular(f"What's the root or lemma or origin of word: {input_text}, And what's their Chinese meaning.")
                    except: pass
                    if origin:
                        try:
                            db_daily_words_update_stutas = update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, 'origin', origin)
                            if db_daily_words_update_stutas: aler_message_1.info(f'ORIGIN of {input_text} was just updated.')
                        except: pass
                if origin: 
                    origin = origin.replace('\n\n', '\n')
                    origin_info.success(f"ROOTs from ChatGPT: \n\n{origin}")
                    if not st.session_state['is_sealed']:  
                        try: update_or_insert_data(db_engine, 'db_daily_words', 'word', input_text, 'sealed', 1)
                        except: pass
                # sentences from database
                try:
                    sentences_dict = st_check_for_sentences(input_text)
                    if sentences_dict:                             
                        with sentences_from_db_expander.expander(f"Click to CHECK {len(sentences_dict)} examples(s) of {input_text}:"):
                            for k, v in sentences_dict.items():
                                if not k or not v: continue
                                st.success(k)
                                try:
                                    with open(v, 'rb') as ad: st.audio(ad)
                                except: pass
                except: aler_message_1.error(f"Retrive EXAMPLES failed...")

        else: 
            if not st.session_state['is_chinese']:
                aler_message_1.error(f"Can NOT find information for: {input_text}")
                if st.session_state['authentication_status']:
                    update_value = value_input.text_input("Please add new value or edit the current value:", value=input_text, key='dict')
                    dict_edit_confirmed = confirm_button.button('CONFIRM CREATE')
                    if dict_edit_confirmed:
                        r = {}
                        try: r = st_instert_new_word(input_text)
                        except: pass
                        if r.get('word') == input_text: aler_message_1.info(f'WORD {input_text} was newly added.')
    elif st.session_state['is_english']:
        input_text = escape_quotes(input_text)
        tts_file_name = st_update_sentences(input_text)
        sentence_info.success(input_text)
        if tts_file_name:
            with open(tts_file_name, 'rb') as ad: sentence_audio.audio(ad)

if channel_choosed == 'CHAT_GPT':
    selected_funciton = st.selectbox("What you want to do:", ['AI_CHAT', 'STORY_FORK', 'AI_CHAT_HISTORY', 'AI_ARTICLE', 'ALICE_CHAT', 'TELEGRAM_CHAT'], index=0)

    if selected_funciton == 'AI_CHAT':
        system_prompt_default = ['You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work.']

        df = pd.read_sql_table("pre_prompt_examples", db_engine)
        df = df.sort_values(by=['id'], ascending=False)
        pre_prompt_list = df['prompt'].to_list()

        chose_pre_prompt = st.selectbox("请为 ChatGPT 选择一个人设（System Prompt）:", system_prompt_default + pre_prompt_list, index=0)

        system_prompt = st.text_area("您可以修改 ChatGPT 的人设（System Prompt）:", value = chose_pre_prompt + ' ', key='3_ai_chat_system_prompt', height=80)

        user_prompt = st.text_area("请修改 ChatGPT 的提问事例（User）:", value = "Who won the world series in 2020?", key='3_ai_chat_user_prompt', height=20)
        assistant_prompt = st.text_area("请修改 ChatGPT 的回复事例（Assistant）:", value = "The Los Angeles Dodgers won the World Series in 2020.", key='3_ai_chat_assistant_prompt', height=20)

        chatgpt_key_tier = st.selectbox("请选择 ChatGPT 的 API 级别:", ['FREE', 'PLATINUM'], index=0)
        chatgpt_key = openai_key if chatgpt_key_tier == 'PLATINUM' else OPENAI_API_KEY_FREE

        df_model_id = OPENAI_MODEL_LIST_PLATINUM if chatgpt_key_tier == 'PLATINUM' else OPENAI_MODEL_LIST_FREE
        df_model_id_index = df_model_id.index('gpt-3.5-turbo') if 'gpt-3.5-turbo' in df_model_id else 0
        dynamic_model = st.selectbox(f"请选择 ChatGPT ({chatgpt_key_tier}) 的模型（Totally {len(df_model_id)} Models）:", df_model_id, index=df_model_id_index)

        question_text = st.text_area("请输入您的问题或者请求（Prompt）:", value = ' ', key='3_ai_chat_prompt', height=160)
        error = False

        col1, col2, col3 = st.columns(3)

        if col1.button("SUBMIT QUESTION"):
            question_text = question_text.strip('\n').strip()
            need_to_sync_to_db = False
            responsed_content = ''
            response_date = ''

            df = pd.read_sql_query(f'SELECT * FROM `ai_chat_history` WHERE LOWER(`question_input`) = "{question_text.lower()}"', db_engine)
            if not df.empty: 
                if debug: print(f"DEBUG : Already asked, get response from database.")
                responsed_content = df.iloc[0]['response_output']
                response_date = df.iloc[0]['update_time']
                need_to_sync_to_db = False
            elif question_text and system_prompt and user_prompt and assistant_prompt and dynamic_model and chatgpt_key:
                try: 
                    responsed_content = chat_gpt_full(question_text, system_prompt, user_prompt, assistant_prompt, dynamic_model, chatgpt_key)
                    response_date = datetime.now()
                    responsed_content = responsed_content.strip('\n').strip()
                    need_to_sync_to_db = True
                except: error = True
            
            if responsed_content and response_date: 
                st.code(f"CHAT_GPT Rseponsed:", language='python')
                st.write(responsed_content)
                st.caption(f"Responsed time & date: {str(response_date).split('.')[0]}")
                news_words_rank_1 = st.empty()
                news_words_rank_2 = st.empty()
                ai_audio_position = st.empty()
                words_list_chinese = st.empty()
                error_info = st.empty()

                if not error and len(responsed_content.split()) < 500:
                    tts_file_name = ''
                    
                    try: word_language = detect_language(responsed_content)
                    except: word_language = 'Chinese'

                    is_chinese = True
                    if word_language != 'Chinese': 
                        is_chinese = False

                        news_words_list = extract_words(responsed_content)
                        # st.caption(news_words_list)
                        db_dict_1, db_dict_2, db_dict_3 = {}, {}, {}
                        try: db_dict = st_find_ranks_for_news_words(news_words_list)
                        except: pass
                        if db_dict: db_dict_1, db_dict_2, db_dict_3 = db_dict 
                        if db_dict_1:
                            words_list_with_rank_1 = [f"{k}({int(v)})" for k, v in db_dict_1.items() if not math.isnan(v)]
                            if words_list_with_rank_1: news_words_rank_1.code(f"TOEFL/GRE/GMAT/SAT:  {' | '.join(words_list_with_rank_1)}", language='python')
                        if db_dict_2:
                            words_list_with_rank_2 = [f"{k}({int(v)})" for k, v in db_dict_2.items() if not math.isnan(v)]
                            if words_list_with_rank_2:news_words_rank_2.code(f"OTHER WORDS:  {' | '.join(words_list_with_rank_2)}", language='python')

                        if db_dict_3:
                            words_list_meaning = [f"{k} : {v[:80]}" for k, v in db_dict_3.items() if v]
                            if words_list_meaning:
                                with words_list_chinese.expander("CLICK to check words meaning"):
                                    st.write(words_list_meaning)

                    try:
                        tts_file_name = generate_or_read_tts('ai_chat', responsed_content, is_chinese)
                        if tts_file_name:
                            with open(tts_file_name, 'rb') as tts: ai_audio_position.audio(tts)
                    except: error_info.error(f"FAILED to load audio file.")

                else: error_info.code(f"Respond is TOO LONG for telegram or audio.")

                page_content = f"---created by Laogege:\n\nI asked ChatGPT:\n{question_text}\n\nChatGPT-4 replied:\n{responsed_content}"

                if need_to_sync_to_db and not error:
                    command_conn = db_engine.connect()
                    # command_conn.execute("CREATE TABLE IF NOT EXISTS ai_chat_history (id INT AUTO_INCREMENT PRIMARY KEY, `question_input` TEXT DEFAULT NULL, `response_output` TEXT DEFAULT NULL, `update_time` DATETIME)")
                    try: command_conn.execute("INSERT INTO ai_chat_history (`question_input`, `response_output`, `update_time`) VALUES (%s, %s, %s)", (question_text, responsed_content, datetime.now()))
                    except Exception as e: error_info.error(f"FAILED to insert info to: ai_chat_history database.")
                    command_conn.close()

        if col2.button("INSERT TO PRE_PROMPT TABLE"):
            try: r = update_or_insert_data(db_engine, 'pre_prompt_examples', 'prompt', question_text, 'prompt', question_text)
            except: st.error(f"FAILED to INSERT to pre_prompt_examples table.")
            if r: st.success(f"Successfully INSERTED to pre_prompt_examples table.")

        if col3.button("DELETE FROM PRE_PROMPT TABLE"):
            try: 
                conn.execute(f"DELETE FROM pre_prompt_examples WHERE `prompt` = '{chose_pre_prompt}'")
                st.success(f"Successfully DELETED from ai_chat_history table.")
            except: st.error(f"FAILED to DELETE from pre_prompt_examples table.")

    if selected_funciton == 'STORY_FORK':

        selected_actions = st.selectbox("ACTION: ", ['READ_STORIES', 'CREATE_NEW_STORY'], index=0, key='story_fork_action')
        if selected_actions == 'READ_STORIES':
            # create a story_genre list from db_story_fork
            story_genre_list = pd.read_sql_query("SELECT DISTINCT `story_genre` FROM `db_story_fork`", db_engine)
            story_genre_list = story_genre_list['story_genre'].tolist()
            story_genre_list = [i for i in story_genre_list if i]
            selected_genre = st.selectbox("SELECT GENRE: ", story_genre_list, index=0, key='story_fork_genre')
            if selected_genre:
                # create a story_title list from db_story_fork
                story_title_list = pd.read_sql_query(f"SELECT DISTINCT `story_title` FROM `db_story_fork` WHERE `story_genre` = '{selected_genre}'", db_engine)
                story_title_list = story_title_list['story_title'].tolist()
                story_title_list = [i for i in story_title_list if i]
                selected_title = st.selectbox("SELECT TITLE: ", story_title_list, index=0, key='story_fork_title')
                if selected_title:
                    # create a story_chapter list from db_story_fork
                    story_chapter_list = pd.read_sql_query(f"SELECT DISTINCT `story_chapter` FROM `db_story_fork` WHERE `story_genre` = '{selected_genre}' AND `story_title` = '{selected_title}'", db_engine)
                    story_chapter_list = story_chapter_list['story_chapter'].tolist()
                    selected_chapter = st.selectbox("SELECT CHAPTER: ", story_chapter_list, index=0, key='story_fork_chapter')
                    df_chapter_content = pd.read_sql_query(f"SELECT * FROM `db_story_fork` WHERE `story_genre` = '{selected_genre}' AND `story_title` = '{selected_title}' AND `story_chapter` = {selected_chapter}", db_engine)
                    # df_chapter_content
                    for i in df_chapter_content['chapter_content'].index:
                        st.code(f"CHAPTER {selected_chapter}\nForked by {df_chapter_content.iloc[i]['fork_ethaddress']}\nForked time: {df_chapter_content.iloc[i]['fork_time']}\nForked hash: {df_chapter_content.iloc[i]['fork_hash']}")
                        with st.expander("Check user prompt that inpired this chapter."):
                            st.info(df_chapter_content.iloc[i]['story_prompt'])
                        st.success(df_chapter_content.iloc[i]['chapter_content'])

        if selected_actions == 'CREATE_NEW_STORY':
            st.session_state['user_input_prompt'] = st.text_area("PROMPT (anything in your mind about this story that will inspire AI): ", value='', key='story_fork_new_content_prompt')
            st.code(f"创作一个章节大概需要 3~5 分钟，请不要关闭页面，等待 AI 生成内容。")
            if st.session_state.get('user_input_prompt'):
                system_prompt='''
你是非常著名的小说家，你读过上万本经典小说，自己写过上百本各种题材的小说，大部分都成为了当代热门的畅销小说。你写的小说文笔流畅，情节生动，人物刻画栩栩如生，每人物在你的笔下都展现出了丰满的任性特质。不管是什么样的题材，你都能游刃有余，充分展现出该题材所定义的特性和特质。现在，一位资深读者想找你合作，他会提供一些关键信息和要求给你，请尽量按照他的要求来创作第一章。有几点注意事项：

1) 第一章仅仅是故事的开篇，不需要在第一章推进太多情节，只要让读者通过第一章了解故事的大体风格和叙事方向即可，结尾的时候引入一个让人浮想联翩的情节，让读者迫不及待想要阅读下一章；

2) 请从下面列表中选出一个你认为合适该小说的题材（只需选择一个最合适的）: 'FANTASY', 'HORROR', 'ROMANCE', 'MYSTERY', 'THRILLER', 'SCIENCE_FICTION', 'HISTORY', 'BIOGRAPHY', 'MEMOIR', 'NONFICTION', 'FANFICTION'；

3) 给出一个你认为合适的小说标题；

4) 要针对本章节的内容，按照时间顺序罗列出本章节的情节纪要，后续章节的创作过程中，你不会看到历史章节的内容，但是你会看到历史章节的核心情节纪要，后续的创作要参考前面所有章节的纪要来避免内容冲突或者重复；

5) 请按照以下格式回复:

TITLE: 你建议的小说标题
GENRE: 你建议的小说题材
CONTENT: 你草拟的小说大纲
SUMMARY: 本章的情节纪要
'''
                user_prompt='''
帮我创作一个新的单纯少女爱上霸道总裁的故事，类似于《五十度灰》
'''
                assistant_prompt='''
TITLE: 我的霸道总裁男友

GENRE: ROMANCE

CONTENT:
第一章：不经意的安排

我用一种很挫败的心情看着镜子里的自己，愁容满面。该死的头发，你就不能服帖点。还有（恼火的）的凯瑟琳 · 卡瓦纳，就因为她生病了，我就得代替她去做这件痛苦的事！哎，本来我现在应该是在复习下个星期的期末考试的而不是现在这样费劲脑汁让我的头发变得服帖顺滑点。坚决不能头发没干就睡觉，坚决不能头发没干就睡觉，我对自己碎碎念暗示了几下之后，又尝试用梳子把头发再梳了一次，然后我转了转眼睛略带愤怒的盯着镜子里的自己，发现里面一个脸色苍白的棕发女孩，也用一个大的有点出奇的蓝眼睛盯着我。。。好吧我放弃了。现在我只能选择扎个马尾辫来搞定我这自由散漫生长的头发，希望看上去至少有那么点可人儿吧。

凯特是我的室友，明明有那么多日子她却刚好今天很不幸地被流感击倒，总之她事先为学生报纸安排的采访是去不了，而且需要采访的那些人是我从来没有听过的，都是身价百万的企业家和商业大亨。因为流感她不得不让我代替她去。本来期末考试还完全没有复习过，正准备临时抱下佛脚，另外还有一篇散文需要写。所以正常情况下，今天下午我应该是在准备期末考试和散文而不是现在这样开车跑165英里去西雅图市区见格雷集团神秘莫测的CEO。这个CEO挺特立独行的同时她还是我们学校主要的捐助者之一。他的时间应该是很宝贵的至少宝贵过我，不过他居然同意凯特的采访邀请!这简直是中了头奖，凯特当时告诉我说。可是我却很讨厌这个课外活动。

凯特在客厅的沙发上缩成一团。：“真的很抱歉，安娜！我花了九个月才获得这个采访许可，如果不去，我又要再多花六个月重新去确定采访日期，到那个时候我们俩都毕业了！作为编辑，我不能眼睁睁的看着它泡汤。求求你啦，安娜，帮帮我，代替我去吧！”凯特忍着发炎疼痛的喉咙用它沙哑尖锐的声音求我。可是她哪里像感冒很严重的样子。就算生病了，她看上去还是很妖娆美丽，略带金黄的红色头发柔软的搭在肩上，还有她明亮的绿眼睛即使现在眼眶有点红还流着鼻涕都让她看上去很美丽。我直接无视这突如其来的同情。

“好吧好吧，我会去的，凯特。所以你现在快躺到床上去，需要给你拿点奈奎尔或泰诺吗”
“奈奎尔吧，谢了。这是准备的问题和迷你磁盘记录器。按这里就是开始录音，你到时做好记录，最后我会统一把这些整理出来”
“可是我对他一无所知啊！”我小声嘀咕，尝试抑制住不断上升的恐惧，可惜完全没用。
“你最好全部看一遍问题哈，快走吧，开车需要挺久的，我不希望你迟到”

整理好我的小背包，我面带苦色的对她笑了一下，朝着门外的车走去。我不敢相信我让凯特成功说服了我，事实上凯特可以说服任何一个去做任何事儿。她将是一位很厉害的记者。她心思缜密、坚强、有着极佳的说服力很善辩，而且非常漂亮。同时她也是我最亲密最好的闺蜜。

SUMMARY:
故事的女主角安娜被室友凯特（凯瑟琳 · 卡瓦纳）求助，代替生病的凯特去采访格雷集团神秘莫测的CEO。
安娜对这次采访一无所知，但还是决定去完成任务。
凯特非常漂亮，同时也是安娜最亲密最好的闺蜜。
'''
                new_generated_content = chat_gpt_full(st.session_state['user_input_prompt'], system_prompt, user_prompt, assistant_prompt, 'gpt-4', openai_key)

                if new_generated_content:
                    st.success(f"GENERATED CONTENT: \n\n{new_generated_content}")

                    st.session_state['new_title'] = new_generated_content.split('TITLE:')[1].split('\n')[0].strip()
                    suggested_genre = new_generated_content.split('GENRE:')[1].split('\n')[0].upper().strip()
                    new_generated_content = new_generated_content.split('CONTENT:')[1]
                    st.session_state['chapter_content_area'] = new_generated_content.split('SUMMARY:')[0].strip()
                    st.session_state['chapter_summary_area'] = new_generated_content.split('SUMMARY:')[1].strip()

                    GENRE_LIST = ['FANTASY', 'HORROR', 'ROMANCE', 'MYSTERY', 'THRILLER', 'SCIENCE_FICTION', 'HISTORY', 'BIOGRAPHY', 'MEMOIR', 'NONFICTION', 'FANFICTION', 'OTHER']

                    st.session_state['chose_genre'] = suggested_genre if suggested_genre in GENRE_LIST else st.selectbox("CHOOSE_A_GENRE: ", [] + GENRE_LIST, index=0, key='story_fork_new_genre')
                    if st.session_state['chose_genre']:
                        st.code(f"Title: {st.session_state['new_title']}, Genre: {st.session_state['chose_genre']}", language='python')

                        st.session_state['user_name'] = 'leowang'
                        # user_uuid = str(uuid.uuid4())
                        st.session_state['user_uuid'] = '5d1c1b91-fc05-4404-a82a-92774cda80ee'
                        # uses haslib to generate a hash for new_generated_content
                        st.session_state['new_generated_content_hash'] = hashlib.sha256(st.session_state['chapter_content_area'].encode('utf-8')).hexdigest()
                        st.session_state['fork_hash_previous'] = 'ORIGIN'
                        st.session_state['fork_ethaddress'] = '0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'

                        st.session_state['chapter_content_area'] = st.session_state['chapter_content_area'].replace("'", "\\'")
                        st.session_state['chapter_content_area'] = st.session_state['chapter_content_area'].replace('"', '\\"')

                        st.session_state['chapter_summary_area'] = st.session_state['chapter_summary_area'].replace("'", "\\'")
                        st.session_state['chapter_summary_area'] = st.session_state['chapter_summary_area'].replace('"', '\\"')

                        # '''CREATE TABLE IF NOT EXISTS db_story_fork (
                        #     id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        #     story_prompt TEXT,
                        #     story_title VARCHAR(255),
                        #     story_genre VARCHAR(255),
                        #     story_original_author_uuid VARCHAR(255),
                        #     story_original_author_name VARCHAR(255),
                        #     story_created_time DATETIME,
                        #     story_chapter INT UNSIGNED,
                        #     fork_hash_previous VARCHAR(255),
                        #     fork_hash VARCHAR(255),
                        #     fork_ethaddress VARCHAR(255),
                        #     fork_user_uuid VARCHAR(255),
                        #     fork_time DATETIME,
                        #     chapter_content TEXT,
                        #     chapter_summary TEXT
                        # );'''

                        insert_conn = db_engine.connect()
                        insert_conn.execute(f"INSERT INTO `db_story_fork` (`story_prompt`, `story_title`, `story_genre`, `story_original_author_uuid`, `story_original_author_name`, `story_created_time`, `story_chapter`, `fork_hash_previous`, `fork_hash`, `fork_ethaddress`, `fork_user_uuid`, `fork_time`, `chapter_content`, `chapter_summary`) VALUES ('{st.session_state['user_input_prompt']}', '{st.session_state['new_title']}', '{st.session_state['chose_genre']}', '{st.session_state['user_uuid']}', '{st.session_state['user_name']}', '{datetime.now()}', 1, '{st.session_state['fork_hash_previous']}', '{st.session_state['new_generated_content_hash']}', '{st.session_state['fork_ethaddress']}', '{st.session_state['user_uuid']}', '{datetime.now()}', '{st.session_state['chapter_content_area']}', '{st.session_state['chapter_summary_area']}')")
                        insert_conn.close()

                        df = pd.read_sql_query("SELECT * FROM `db_story_fork` ORDER BY `id` DESC LIMIT 1", db_engine)
                        # created a dict from df
                        df_dict = df.iloc[0].to_dict()

                        del df_dict['chapter_content']
                        with st.expander(f"STORY FORKED AND SUBMITTED SUCCESSFULLY!"):
                            st.write(df_dict)

    if selected_funciton == 'AI_ARTICLE':
        article_info = st.empty()
        try: chat_gpt_article_for_today()
        except: pass
        df = pd.read_sql_query("SELECT * FROM `db_daily_articles` ORDER BY `id` DESC LIMIT 5", db_engine)
        if not df.empty:
            for i in range(df.shape[0]):
                st.code(f"CHAT_GPT ARTICLE from {df.iloc[i]['update_time']}:", language='python')
                try:
                    input_sentence = str(df.iloc[i]['article']).lower()
                    tts_file_name = st_update_sentences(input_sentence)
                    if tts_file_name:
                        with open(tts_file_name, 'rb') as ad: st.audio(ad)
                except: pass
                st.success(df.iloc[i]['article'])
        else: article_info.error(f"NO ARTICLE FOR TODAY")

    if selected_funciton == 'AI_CHAT_HISTORY':
        next_button, first_page = st.columns(2)
        offset = st.session_state.get('offset', 0)
        df = pd.read_sql_query(f'SELECT * FROM `ai_chat_history` ORDER BY update_time DESC LIMIT 10 OFFSET {offset}', db_engine)
        if not df.empty:
            for i in range(df.shape[0]):
                index_msg = f"{df.iloc[i]['update_time']} | PROMPT : \n{df.iloc[i]['question_input']}"
                st.code(index_msg, language='python')
                responsed_content = df.iloc[i]['response_output']
                st.write(responsed_content)
                
                if len(responsed_content.split()) < 500:
                    try: word_language = detect_language(responsed_content)
                    except: word_language = 'Chinese'

                    is_chinese = True if word_language == 'Chinese' else False

                    try:
                        tts_file_name = generate_or_read_tts('ai_chat', responsed_content, is_chinese)
                        if tts_file_name:
                            with open(tts_file_name, 'rb') as tts: st.audio(tts)
                    except: st.error(f"FAILED to load audio file.")

            if offset > 0:
                if first_page.button('GO BACK TO FIRST PAGE'):
                    offset = 0
                    st.session_state['offset'] = offset
            if next_button.button('NEXT 10 HISTORY CHAT'):
                offset += 10
                st.session_state['offset'] = offset

    if selected_funciton == 'TELEGRAM_CHAT':
        #读出 alice_chat_history 表单历史记录
        df_all = pd.read_sql_query("SELECT * FROM `telegram_chat_history`", db_engine)
        if not df_all.empty:
            # 按照 chat_id 分组并在页面上显示
            df_grouped = df_all.groupby('chat_id')
            # 将所有的 chat_id 放到一个列表中
            chat_id_list = df_grouped.groups.keys()
            select_chat_id = st.selectbox("请选择您想查看的对话用户:", chat_id_list, index=0)
            # 读出 select_chat_id 的所有历史记录
            df_selected = df_grouped.get_group(select_chat_id)
            st.session_state['current_chat_id'] = select_chat_id
            # 显示出 select_chat_id 的所有历史记录
            i = 0
            index_msg = f"chat_id: {df_selected.iloc[i]['chat_id']} | {df_selected.iloc[i]['update_time']} | {df_selected.iloc[i]['username']} | {df_selected.iloc[i]['first_name']} | {df_selected.iloc[i]['last_name']} | {df_selected.iloc[i]['from_id']}"
            st.code(index_msg, language='python')

            for i in range(df_selected.shape[0]): st.code(f"{str(df_selected.iloc[i]['username']).upper()}:\n\n{df_selected.iloc[i]['msg_text']}", language='python')

    if selected_funciton == 'ALICE_CHAT':
        #读出 alice_chat_history 表单历史记录
        df_all = pd.read_sql_query("SELECT * FROM `alice_chat_history`", db_engine)
        if not df_all.empty:
            # 按照 chat_id 分组并在页面上显示
            df_grouped = df_all.groupby('chat_id')
            # 将所有的 chat_id 放到一个列表中
            chat_id_list = df_grouped.groups.keys()
            select_chat_id = st.selectbox("请选择您想查看的对话用户:", chat_id_list, index=0)
            # 读出 select_chat_id 的所有历史记录
            df_selected = df_grouped.get_group(select_chat_id)
            st.session_state['current_chat_id'] = select_chat_id
            # 显示出 select_chat_id 的所有历史记录
            i = 0
            index_msg = f"chat_id: {df_selected.iloc[i]['chat_id']} | {df_selected.iloc[i]['update_time']} | {df_selected.iloc[i]['username']} | {df_selected.iloc[i]['first_name']} | {df_selected.iloc[i]['last_name']} | {df_selected.iloc[i]['from_id']}"
            if df_selected.iloc[i]['black_list'] == 1: index_msg += " | this user was BLACKLISTED"
            st.code(index_msg, language='python')

            for i in range(df_selected.shape[0]): st.code(f"{str(df_selected.iloc[i]['username']).upper()}:\n\n{df_selected.iloc[i]['msg_text']}", language='python')
            
            col1, col2 = st.columns(2)
            bl_user = col1.button('ADD_THIS_USER_TO_BLACKLIST')
            if bl_user:
                try:
                    bl_conn = db_engine.connect()
                    bl_conn.execute(f"UPDATE `alice_chat_history` SET `black_list`=1 WHERE `chat_id`='{df_selected.iloc[i]['chat_id']}'")
                    bl_conn.close()
                    st.success(f"Successfully blacklisted {st.session_state['current_chat_id']}: {df_selected.iloc[i]['username']}")
                except: st.error(f"FAILED to blacklist {st.session_state['current_chat_id']}: {df_selected.iloc[i]['username']}")

            wl_user = col2.button('ADD_THIS_USER_TO_WHITELIST')
            if wl_user:
                try:
                    bl_conn = db_engine.connect()
                    bl_conn.execute(f"UPDATE `alice_chat_history` SET `black_list`=0 WHERE `chat_id`='{df_selected.iloc[i]['chat_id']}'")
                    bl_conn.close()
                    st.success(f"Successfully whitelisted {st.session_state['current_chat_id']}: {df_selected.iloc[i]['username']}")
                except: st.error(f"FAILED to whitelisted {st.session_state['current_chat_id']}: {df_selected.iloc[i]['username']}")

if channel_choosed == 'EXPENDITURE':
    total_expenditures = st.empty()

    if st.session_state['authentication_status']:
        
        df = pd.read_sql_query(f"SELECT * FROM home_expends WHERE is_deleted=0", remote_db_engine)
        total_costs = df['total_value'].sum()
        total_expenditures.code(f"You have totally spend {format_number(total_costs)} USD in USA since 2022-10-24.", language='python')

        # Define the input fields for the home_expends table
        TAG_LIST = [
            'furnitures',
            'electronic product',
            'fitness',
            'education',
            'insurance',
            'smoke',
            'english study',
            'auto & transport',
            'bills & utilities',
            'business',
            'charitable donations',
            'dining & drinks',
            'entertainment & rec.',
            'family care',
            'fees',
            'gifts',
            'groceries',
            'health & medical',
            'home & garden',
            'legal',
            'loan payment',
            'shopping',
            'pets',
            'software & tech',
            'taxes',
            'travel & vacation'
        ]

        # Define the input fields for the home_expends table
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        name = col1.text_input("Name")
        tag = col2.selectbox("Tag", TAG_LIST, index=1)
        brand = col3.text_input("Brand", value='Amazon')
        platform = col4.text_input("Platform", value="amazon")
        price = col5.number_input("Price", step=0.01, format="%.2f")
        quantity = col6.number_input("Quantity", step=1, value=1)
        renew = col7.selectbox("Renew", ["m", "y", "n"], index=2)
        protection = col8.number_input("Protection", step=1, value=0)

        # Define additional input fields for the home_expends table
        full_name = st.text_area("Full Name")
        memo = st.text_area("Memo")

        # Calculate the total value based on price and quantity
        total_value = price * quantity

        # Define a button to submit the form
        if st.button("SUBMIT EXPENDITURE"):
            # Insert the data into the MySQL database
            command_conn = remote_db_engine.connect()
            try:
                command_conn.execute("INSERT INTO home_expends (name, tag, brand, platform, price, quantity, renew, full_name, protection, memo, total_value, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, tag, brand, platform, price, quantity, renew, full_name, protection, memo, total_value, datetime.now()))
                st.success("Expenditure added successfully!")
            except Exception as e:
                st.error("Error occurred while adding expenditure: {}".format(e))
            command_conn.close()

        with st.expander("Show all the expenditure records by month"):
            df['year_month'] = df['update_time'].dt.strftime('%Y-%m')

            df_grouped = df.groupby('year_month')
            total_expenses_by_month = df_grouped['total_value'].sum()
            total_expenses_by_month = total_expenses_by_month.sort_index()

            fig, ax = plt.subplots()
            ax.bar(total_expenses_by_month.index, total_expenses_by_month.values)
            ax.set_title('Total Expenses by Month')
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Expenses')
            for i, v in enumerate(total_expenses_by_month.values):
                ax.text(i, v + 100, f"${v:,.2f}", ha='center', fontsize=8)
            st.pyplot(fig)

            # Add a button to download the bar plot as an image file
            buffer = io.BytesIO()
            fig.canvas.print_png(buffer)
            st.download_button(
                label="Download Plot as PNG",
                data=buffer.getvalue(),
                file_name='plot.png',
                mime='image/png'
            )

    else: report_info.info("OWNER ONLY!")

if channel_choosed == 'DATABASE':
    # st.title('CHECK ANY DATABASE INFO:')
    database_choosed = st.selectbox('Choose your target DATABASE', ['REMOTE', 'LOCAL'], index=1, key='1')
    use_db_engine = remote_db_engine if database_choosed == 'REMOTE' else db_engine

    table_list = show_all_tables(use_db_engine)
    default_ix = table_list.index('prompt_examples')
    table_choosed = st.selectbox('Choose your target TABLE', table_list, index=default_ix, key='2')

    if table_choosed == 'avatar_user_info':
        # 将 avatar_user_info 的 column 读出来生成一个列表
        df = pd.read_sql_query(f'SELECT * FROM {table_choosed}', use_db_engine)
        col = df.columns.tolist()
        col_choosed = st.selectbox('Choose your target COLUMN', col, index=0, key='avatar_1')
        update_column = st.text_area("UPDATE Content/Value", key='avatar_2')


    if table_choosed == 'notes_and_memos':
        input_notes = st.text_input("Enter the notes your want to store:", key='7')
        if st.button('Insert the note') and input_notes:
            try: 
                r = update_table_notes_and_memos(input_notes)
                if r: st.success(f"Successfully inserted.")
            except Exception as e: st.error(f"ERROR : update_table_notes_and_memos() failed: \n\n{e}")

    if table_choosed == 'email_assistant_whitelist':
        email_address = st.text_input("Enter the email your want to add to whitelist:", key='7e')
        if st.button('Insert the email_whitelist') and email_address:
            try: 
                r = add_email_to_whitelist(email_address)
                if r: st.success(f"SUCCESSFULLY add {email_address} to whitelist")
            except: st.error(f"FAILED add {email_address} to whitelist")

    if table_choosed == 'prompt_examples':
        input_notes = st.text_input("Enter the prompt your want to store:", key='10')
        if st.button('Insert the prompt') and input_notes:
            try: 
                r = add_prompt_and_words(input_notes)
                if r: st.success(f"Successfully inserted.")
            except Exception as e: st.error(f"ERROR : add_prompt_and_words() failed: \n\n{e}")

    if table_choosed == 'pre_prompt_examples':
        input_pre_prompt = st.text_input("Enter the pre_prompt your want to store:", key='10_pre')
        if st.button('Insert the pre_prompt') and input_pre_prompt:
            try: 

                try: r = update_or_insert_data(db_engine, 'pre_prompt_examples', 'prompt', input_pre_prompt, 'prompt', input_pre_prompt)
                except: pass

                if r: st.success(f"Successfully inserted.")
            except Exception as e: st.error(f"ERROR : add_pre_prompt_and_words() failed: \n\n{e}")

    if table_choosed == 'svb_creditcard_chuck':
        col1, col2 = st.columns(2)
        input_amount = col1.text_input("Enter the amount:", key='8')
        input_date_string = col2.text_input("Enter the date:", key='9')
        try:
            total_amount = calculate_total_amount_svb_creditcard_chuck()
            if total_amount: st.code(f"Total amount chuck used: {total_amount}")
        except Exception as e: st.error(f"ERROR : calculate_total_amount_svb_creditcard_chuck() failed:\n\n{e}")

        if input_amount:
            input_amount = str(input_amount).replace(',', '')
            try: input_amount = float(input_amount)
            except: 
                input_amount = ''
                st.error(f"Please input a float number")

        if st.button('Insert the payments_note') and input_amount and input_date_string:
            try: 

                r = update_svb_creditcard_chuck(input_amount, input_date_string)
                if r: 
                    st.success(f"Successfully inserted.")                    
            except Exception as e: st.error(f"ERROR : update_svb_creditcard_chuck() failed: \n\n{e}")

    if table_choosed == 'one_time_passcode_key':
        col1, col2 = st.columns(2)
        app_name = col1.text_input("Enter the app_name:", key='81')
        otp_key = col2.text_input("Enter otp_key:", key='91')

        if st.button('Insert the otp_key') and app_name and otp_key:
            try: 

                r = add_otp_key(app_name, otp_key)
                if r: 
                    st.success(f"Successfully inserted.")                    
            except Exception as e: st.error(f"ERROR : add_otp_key() failed: \n\n{e}")

    df = pd.read_sql_query(f'SELECT * FROM {table_choosed}', use_db_engine)
    col = df.columns.tolist()
    if 'update_time' in col:
        df = df.sort_values(by=['update_time'], ascending=False)
    df

    # Display the download button
    if st.button('Create download link for CSV file'):
        create_download_link(df, filename=table_choosed+'.csv')

    with st.expander('Click here to edit a row'):
        columns_list = df.columns.tolist()
        columns_list_integer = [col for col in columns_list if df[col].dtype == 'int64']
        if not columns_list_integer:
            st.warning('No integer columns are available to use as an identifier.')
        if columns_list_integer:
            column_choosed_identify = st.selectbox('Choose the COLUMN to use as an identifier', columns_list_integer, index=0, key='4')
            value_input_identify = st.text_input(f"Enter the value to identify the row in {column_choosed_identify}", key='5')
            if value_input_identify and value_input_identify.isdigit():
                column_choosed = st.selectbox('Choose the target COLUMN to edit', columns_list, index=0, key='3')
                value_input = st.text_input("Enter the new value for the selected column:", key='6')
                if st.button('Confirm the change') and value_input:
                    try:
                        edit_conn = use_db_engine.connect()
                        if value_input.isdigit():
                            edit_conn.execute(f"UPDATE {table_choosed} SET `{column_choosed}`={value_input} WHERE `{column_choosed_identify}`={value_input_identify}")
                        else:
                            edit_conn.execute(f"UPDATE {table_choosed} SET `{column_choosed}`='{value_input}' WHERE `{column_choosed_identify}`={value_input_identify}")
                        edit_conn.close()
                        st.code(f"{column_choosed} of {column_choosed_identify} {value_input_identify} has been updated successfully.")
                    except Exception as e:
                        st.error(f"Failed to update the column due to an error:\n\n{e}")

def upload_and_store_img():
    uploaded_file = st.file_uploader("Choose a image to upload", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        base_path = 'json_datas/img/did_img/'
        filename = uploaded_file.name
        name, ext = os.path.splitext(filename)

        bytes_data = uploaded_file.getvalue()

        i = 1
        while os.path.exists(os.path.join(base_path, filename)):
            name, ext = os.path.splitext(filename)
            name = name.split('_')[0]
            filename = f"{name}_{i}{ext}"
            i += 1

        filepath = os.path.join(base_path, filename)
        with open(filepath, 'wb') as f:
            f.write(bytes_data)

        return filepath

def upload_voice_file():
    real_type = ["wav", "mp3", "m4a"]
    uploaded_file = st.file_uploader("Choose the m4a file you want to convert to wav", type=real_type)
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        base_path = 'json_datas/clone_voice'
        filename = uploaded_file.name
        filepath = os.path.join(base_path, filename)

        i = 1
        while os.path.exists(os.path.join(base_path, filename)):
            name, ext = os.path.splitext(filename)
            name = name.split('_')[0]
            filename = f"{name}_{i}{ext}"
            filepath = os.path.join(base_path, filename)
            i += 1

        with open(filepath, 'wb+') as f:
            f.write(bytes_data)

        if str(filepath).endswith('.m4a'):
            out_put = convert_m4a_to_wav(filepath)
            try: os.remove(filepath)
            except: st.error(f"FAILED removing {filepath}")
            return out_put

        return filepath

def download_video(url):
    # Download the file from the URL
    r = requests.get(url)
    # Save the file to the directory with a timestamp-based name
    file_name = os.path.join("json_datas/video/did_video/", str(datetime.now().timestamp()) + ".mp4")
    with open(file_name, "wb") as f:
        f.write(r.content)
    # Return the file name
    return file_name

if channel_choosed == 'M2W':
    try: 
        out_put = upload_voice_file()
        if out_put: 
            st.code(f"UPLOADED : {out_put}")
            # out_put = convert_m4a_to_wav(filepath)
            st.success(f"CONVERTED : {out_put}")
            with open(out_put, 'rb') as audio_file:
                audio_contents = audio_file.read()
                # st.audio(audio_contents)
            st.download_button(
                label="Download WAV Audio",
                data=audio_contents,
                file_name='converted_from_m4a.wav',
                mime="audio/wav"
            )
    except Exception as e: st.error(e)

if channel_choosed == 'AIGC':
    selected_funciton = st.selectbox("What you want to do:", ['PROMPT_ENGINEER', 'CREATE_AUDIO', 'CREATE_VIDEO', 'UPLOAD_IMAGE', 'UPLOAD_VOICE'], index=0, key='00')

    if selected_funciton == 'UPLOAD_VOICE':
        functions_choosed = st.radio(label=' ', options = ['CLONE_NEW_VOICE', 'UPDATE_CURRENT_VOICE'], index=0, horizontal=True)

        clone_voice_list = get_latest_file(path = 'json_datas/clone_voice')
        filepath = st.selectbox("Choose from current audio files:", ['UPLOAD_NEW_CLONE_VOICE'] + clone_voice_list, index=0, key='01')

        if functions_choosed in ['CLONE_NEW_VOICE']:
            if filepath == 'UPLOAD_NEW_CLONE_VOICE':
                try: filepath = upload_voice_file()
                except Exception as e: st.error(e)
            if filepath and filepath != 'UPLOAD_NEW_CLONE_VOICE':
                try:
                    r = elevenlabs_add_voice(filepath)
                    if r: st.code(r)
                except Exception as e: st.error(e)

        if functions_choosed in ['UPDATE_CURRENT_VOICE']:
            voice_id = ''
            voices_dict = get_elevenlabs_voices()

            voice_id_list = list(voices_dict.keys())
            my_english_voice_index = voice_id_list.index('my_english_voice')
            voice_id_name = st.selectbox("Choose your voice to update:", voice_id_list, index=my_english_voice_index, key='03')
            if voice_id_name: voice_id = voices_dict.get(voice_id_name)

            if voice_id and voice_id_name:
                if filepath == 'UPLOAD_NEW_CLONE_VOICE':
                    try: filepath = upload_voice_file()
                    except Exception as e: st.error(e)
                if filepath and filepath != 'UPLOAD_NEW_CLONE_VOICE':
                    try: 
                        r = elevenlabs_update_voice(voice_id, voice_id_name, filepath)
                        if r: st.code(r)
                    except Exception as e: st.error(e)

    if selected_funciton == 'UPLOAD_IMAGE':
        st.session_state['latest_file'] = ''
        info_placeholder = st.empty()

        if not st.session_state['latest_file']: 
            img_list = get_latest_file(path = 'json_datas/img/did_img/')
            st.session_state['latest_file'] = img_list[0] if img_list else ''

        if st.session_state['latest_file']: 
            info_placeholder.code(f"Latest uploaded image: {st.session_state['latest_file']}")
            st.image(st.session_state['latest_file'])

        try: 
            filepath = upload_and_store_img()
            if filepath: info_placeholder.code(f"UPLOADED : {filepath}")
        except Exception as e: st.error(e)

    if selected_funciton in ['CREATE_VIDEO', 'CREATE_AUDIO']:
            voice_id = ''
            voices_dict = get_elevenlabs_voices()

            voice_id_list = list(voices_dict.keys())
            my_english_voice_index = voice_id_list.index('my_english_voice')

            img_list = get_files_list(path = 'json_datas/img/did_img/')
            default_img_index = len(img_list) - 1 if not st.session_state.get('latest_file') else 0

            voice_col, img_col = st.columns(2)
            voice_id_name = voice_col.selectbox("Choose your voice:", voice_id_list, index=my_english_voice_index, key='000')

            if voice_id_name: voice_id = voices_dict.get(voice_id_name)

            img_name = img_col.selectbox("Choose your image:", img_list, index=default_img_index, key='01')
            contents = st.text_area(f"Paste the contents you want to speak out:", value = '', key='1', height=150)
            # if debug: st.code(f"voice_name : {voice_id_name} | voice_id : {voice_id}")


            word_language = detect_language(contents)
            if word_language != 'Chinese': 

                news_words_list = extract_words(contents)
                db_dict_1, db_dict_2, db_dict_3 = {}, {}, {}
                if not st.session_state['db_dict']:
                    try: st.session_state['db_dict'] = st_find_ranks_for_news_words(news_words_list)
                    except: pass

                if st.session_state['db_dict']: db_dict_1, db_dict_2, db_dict_3 = st.session_state['db_dict'] 
                if debug: print(f"DEBUG : db_dict_1 : {len(db_dict_1)} | db_dict_2 : {len(db_dict_2)} | db_dict_3 : {len(db_dict_3)}")

                if db_dict_1:
                    words_list_with_rank_1 = [f"{k}({int(v)})" for k, v in db_dict_1.items() if not math.isnan(v)]
                    if words_list_with_rank_1: st.code(f"TOEFL/GRE/GMAT/SAT:  {' | '.join(words_list_with_rank_1)}", language='python')
                if db_dict_2:
                    words_list_with_rank_2 = [f"{k}({int(v)})" for k, v in db_dict_2.items() if not math.isnan(v)]
                    if words_list_with_rank_2:st.code(f"OTHER WORDS:  {' | '.join(words_list_with_rank_2)}", language='python')
                if db_dict_3:
                    words_list_meaning = [f"{k} : {v[:50]}" for k, v in db_dict_3.items() if v]
                    if words_list_meaning:
                        with st.expander("CLICK to check words Chinese meaning"):
                            st.write(words_list_meaning)

                if st.button('Generate your voice file from 11Labs', key='2') and contents and voice_id:
                    tts_file_name = generate_or_read_tts_11_labs('leo_voice', contents, voice_id)
                    if tts_file_name:
                        with open(tts_file_name, 'rb') as audio_file:
                            audio_contents = audio_file.read()
                            st.audio(audio_contents)
                        try: 
                            r = get_elevenlabs_userinfo()
                            if r: 
                                del r['xi_api_key']
                                st.code(f"remain character: {r.get('subscription').get('character_limit') - r.get('subscription').get('character_count')} | used character: {r.get('subscription').get('character_count')} |  limit character: {r.get('subscription').get('character_limit')}")
                                with st.expander('Click to check elevenlabs user info.'):
                                    st.write(r)
                        except Exception as e: st.error(e)
                        
                        mp3_file_name = '_'.join(str(contents).split()[:6])
                        st.download_button(
                            label="Download Audio",
                            data=audio_contents,
                            file_name=f'{mp3_file_name}_.mp3',
                            mime="audio/wav"
                        )

                        if selected_funciton in ['CREATE_VIDEO'] and img_name:
                            img_file_name = f'json_datas/img/did_img/{img_name}'
                            img_url = did_upload_img(img_file_name)
                            if img_url: 
                                st.success(f"Image uploaded, url: {img_url}")
                                audio_url = did_upload_audio(tts_file_name)
                                if audio_url: 
                                    st.success(f"Audio uploaded, url: {audio_url}")
                                    video_id = did_create_talkinghead(img_url, audio_url)
                                    if video_id: 
                                        st.success(f"Video created, id: {video_id}")
                                        waiting_count = st.empty()
                                        break_button = st.empty()
                                        i = 0
                                        while True:
                                            i += 1
                                            if break_button.button("BREAK", key=f'3_{str(i)}'): break
                                            waiting_loop = waiting_count.code(f"Waiting for content generating, {10 * i} s...")
                                            time.sleep(10 * i)
                                            result_url = did_get_talkinghead(video_id)
                                            if result_url:
                                                st.write(f"[DOWNLOAD_VIDEO]({result_url})") 
                                                file_name = download_video(result_url)
                                                if file_name: st.video(file_name)
                                                r = did_get_credits()
                                                waiting_count.code(r)
                                                break
    
    if selected_funciton == 'PROMPT_ENGINEER':
        input_notes = st.text_input("Enter the prompt your want to store:", key='10')
        if st.button('Insert the prompt') and input_notes:
            try: 
                word_list = add_prompt_and_words(input_notes)
                if word_list: 
                    st.success(f"Successfully inserted.")
                    st.write(word_list)
            except Exception as e: st.error(f"ERROR : add_prompt_and_words() failed: \n\n{e}")
        
        df = pd.read_sql_table("prompt_examples", db_engine)
        df = df.sort_values(by=['id'], ascending=False)
        prompt_list = df['prompt'].to_list()
        chose_prompt = st.selectbox("Choose a prompt from prompt_list:", [f'TOTALLY_{len(prompt_list)}_PROMPTS'] + prompt_list, index=0, key='010')
        with st.expander('Click to check the meanings of prompt_words:'):
            try:
                chose_prompt_words_list = words_from_chose_prompt(chose_prompt)
                if chose_prompt_words_list: st.write(chose_prompt_words_list)
            except Exception as e: st.error(f"ERROR : read words_from_chose_prompt() failed: \n\n{e}")

        if not chose_prompt.startswith('TOTALLY'):
            streamlit_filepath_list = generative_ai_replicate(chose_prompt, chat_id='')
            if streamlit_filepath_list: st.image(streamlit_filepath_list[0])

        with st.expander('Click to check the prompt_words table:'):
            df_word = pd.read_sql_query("SELECT * FROM `prompt_words` WHERE `word_rank` > 3000", db_engine)
            st.write(df_word)

if channel_choosed in ['BING']:
    query = top_input.text_input(f"What would you like to search:", value = '', key='BING_SEARCH')
    if query:
        filepath = bing_search(query, mkt='en-US')
        if filepath: 
            snippet_total = [f"Today's top news about {query}\n\n"]
            with open(filepath, 'r') as file:
                i = 1
                for line in file:
                    if line in ['WEBPAGES', 'NEWS', 'VIDEOS']: st.title(line)
                    if 'NAME: ' in line: st.subheader(line.replace('NAME: ', ''))
                    if 'SNIPPET: ' in line: 
                        st.success(line.replace('SNIPPET: ', ''))
                        snippet_total.append(line.replace('-','').replace('SNIPPET: ', f'{str(i)}. '))
                        i += 1
                    if 'IMAGE: ' in line: st.image(line.replace('IMAGE: ', ''), width=512)
                    if 'DATE:' in line: st.code(f"{line.replace('DATE: ', '')}")
                    if 'URL:' in line: st.write(f"{line.replace('URL: ', '')}")

            snippet_text_filepath = filepath.replace('.txt', '_snippet.txt')
            with open(snippet_text_filepath, 'w') as file:
                for line in snippet_total:
                    file.write(line + '\n')
            try:
                filepath_news_mp3 = create_news_podcast(filepath = snippet_text_filepath, prompt = '', leo_voice = False)
                filepath_news_txt = filepath_news_mp3.replace('.mp3', '.txt')

                with open(filepath_news_txt, 'r') as f:
                    text_contents = f.read()

                st.success(text_contents)
                st.audio(filepath_news_mp3)

                try: 
                    send_msg(text_contents, chat_id=bot_owner_chat_id)
                    send_audio(filepath_news_mp3, chat_id=bot_owner_chat_id)
                except Exception as e: st.error(f"ERROR : send_msg() failed: \n\n{e}")

                try: send_email_with_attachments(text_contents, 'preangelleo@gmail.com', subject=query, attachments=[filepath_news_txt, filepath_news_mp3, snippet_text_filepath, filepath], smtp_username=GMAIL_LAOGEGECODING_ADDRESS, smtp_password=GMAIL_LAOGEGECODING_PASSWD)
                except Exception as e: st.error(f"ERROR : send_email_with_attachments() failed: \n\n{e}")

            except Exception as e: st.error(f"ERROR : create_news_podcast() failed: \n\n{e}")


st.write(" ")
st.info(f"Laogege's coding...")


