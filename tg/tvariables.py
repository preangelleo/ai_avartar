# -*- coding: utf-8 -*-
from prompt_template import *
from bot_init import *

owner_parameters_dict = get_owner_parameters()

if place_holder:
    # Get the environment variables
    USER_AVATAR_NAME = owner_parameters_dict.get('USER_AVATAR_NAME')
    UBUNTU_SERVER_IP_ADDRESS = owner_parameters_dict.get('UBUNTU_SERVER_IP_ADDRESS')
    DOMAIN_NAME = owner_parameters_dict.get('DOMAIN_NAME')
    OPENAI_API_KEY = owner_parameters_dict.get('OPENAI_API_KEY')
    BOT_TOKEN = owner_parameters_dict.get('BOT_TOKEN')
    BOT_USERNAME = owner_parameters_dict.get('BOT_USERNAME')
    USER_TELEGRAM_LINK = owner_parameters_dict.get('USER_TELEGRAM_LINK')
    BOTOWNER_CHAT_ID = owner_parameters_dict.get('BOTOWNER_CHAT_ID')
    BOTCREATER_CHAT_ID = owner_parameters_dict.get('BOTCREATER_CHAT_ID')
    REPLICATE_KEY = owner_parameters_dict.get('REPLICATE_KEY')
    STABILITY_API_KEY = owner_parameters_dict.get('STABILITY_API_KEY')
    OPENAI_MODEL = owner_parameters_dict.get('OPENAI_MODEL')
    WOLFRAM_ALPHA_APPID = owner_parameters_dict.get('WOLFRAM_ALPHA_APPID')
    MAX_CONVERSATION_PER_MONTH = owner_parameters_dict.get('MAX_CONVERSATION_PER_MONTH')
    PINECONE_FREE = owner_parameters_dict.get('PINECONE_FREE')
    PINECONE_FREE_ENV = owner_parameters_dict.get('PINECONE_FREE_ENV')
    INFURA_KEY = owner_parameters_dict.get('INFURA_KEY')
    CMC_PA_API = owner_parameters_dict.get('CMC_PA_API')
    FINNHUB_API = owner_parameters_dict.get('FINNHUB_API')
    ETHERSCAN_API = owner_parameters_dict.get('ETHERSCAN_API')
    MORALIS_API = owner_parameters_dict.get('MORALIS_API')
    MORALIS_ID = owner_parameters_dict.get('MORALIS_ID')
    MORALIS_APP_ID = owner_parameters_dict.get('MORALIS_APP_ID')
    DEBANK_API = owner_parameters_dict.get('DEBANK_API')
    MONTHLY_FEE = float(owner_parameters_dict.get('MONTHLY_FEE'))
    REFILL_TEASER = owner_parameters_dict.get('REFILL_TEASER')
    ELEVEN_API_KEY = owner_parameters_dict.get('ELEVEN_API_KEY')
    ELEVENLABS_STATUS = owner_parameters_dict.get('ELEVENLABS_STATUS') # 0 is false, 1 is true

    # 查看当前目录并决定 TELEGRAM_BOT_RUNNING 的值
    TELEGRAM_BOT_RUNNING = BOT_TOKEN
    TELEGRAM_BOT_NAME = BOT_USERNAME
    BOT_OWNER_LIST = [BOTOWNER_CHAT_ID, BOTCREATER_CHAT_ID]

    openai.api_key = OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    ELEVENLABS_API = os.getenv("ELEVEN_API_KEY")
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
    STABILITY_URL = f"https://api.stability.ai/v1/"

    ETHERSCAN_WALLET_URL_PREFIX = 'https://etherscan.io/address/'
    ETHERSCAN_TX_URL_PREFIX = 'https://etherscan.io/tx/'
    ETHERSCAN_TOKEN_URL_PREFIX = 'https://etherscan.io/token/'

    BOTCREATER_TELEGRAM_HANDLE = '@laogege6'

    # Telegram base URL
    telegram_base_url = "https://api.telegram.org/bot" + TELEGRAM_BOT_RUNNING + "/"    
    # initialize pinecone
    pinecone.init(api_key=PINECONE_FREE,  environment=PINECONE_FREE_ENV)

    os.environ["WOLFRAM_ALPHA_APPID"] = os.getenv('WOLFRAM_ALPHA_APPID')
    wolfram = WolframAlphaAPIWrapper()
    wikipedia = WikipediaAPIWrapper()

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

    avatar_png = 'files/images/512.png'
    avatar_command_png = 'files/images/avatar_command.png'
    avatar_create = f"如果您也希望拥有一个像 @{TELEGRAM_BOT_NAME} 这样的 <AI分身> 来服务您的朋友们, 以您的语气陪他们/她们聊天, 帮他们完成 OpenAI 大语言模型可以做的一切任务, 可以点击 /more_information 了解, 非诚勿扰, 谢谢! 😋"
    avatar_more_information = "<AI分身> 电报机器人由酷爱 Python 的老哥哥 @laogege6 利用业余时间开发创造 😊:\n\n- 技术服务费: 100美金/月;\n- 支持 USDT 等各种付款方式;\n- 需要您提供自己的 OpenAI API;\n- 需要您在 @BotFather 开通机器人账号;\n- 您可以随时修改 <AI分身> 的人设背景;\n- 您可以自由修改 <AI分身> 的语调语气.\n\n详情邮件咨询:\nadmin@leonardohuang.com"

def convert_to_local_timezone(timestamp, local_time_zone='America/Los_Angeles'):
    utc_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_timezone = pytz.timezone('UTC')
    local_timezone = pytz.timezone(local_time_zone)  # Replace with your local timezone

    local_timestamp = utc_timezone.localize(utc_timestamp).astimezone(local_timezone)
    formatted_timestamp = local_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_timestamp

def bing_search(query, mkt='en-US'):
    '''
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    '''
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    # Construct a request
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': BING_SEARCH_API_KEY}

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        folder = 'files/bing_search'
        if not os.path.exists(folder): os.makedirs(folder)
        query = query.lower()

        query_name = query.replace(',', '')
        query_name = query_name.replace(' ', '_')
        query_name = query_name.replace('?', '')
        query_name = query_name.replace('!', '')
        query_name = query_name.replace('(', '')
        query_name = query_name.replace(')', '')
        query_name = query_name.replace('\'', '')
        query_name = query_name.replace('\"', '')
        query_name = query_name.replace(':', '')
        query_name = query_name.replace(';', '')
        query_name = query_name.replace('+', '')
        query_name = query_name.replace('=', '')
        query_name = query_name.replace('*', '')
        query_name = query_name.replace('&', '')
        query_name = query_name.replace('%', '')
        query_name = query_name.replace('$', '')
        query_name = query_name.replace('#', '')
        query_name = query_name.replace('@', '')
        query_name = query_name.replace('~', '')
        query_name = query_name.replace('`', '')
        query_name = query_name.replace('^', '')
        query_name = query_name.replace('/', '')
        query_name = query_name.replace('\\', '')
        query_name = query_name.replace('|', '')
        query_name = query_name.replace('<', '')
        query_name = query_name.replace('>', '')
        query_name = query_name.replace('[', '')
        query_name = query_name.replace(']', '')
        query_name = query_name.replace('{', '')
        query_name = query_name.replace('}', '')
        query_name = query_name.replace('’', '')
        query_name = query_name.replace('‘', '')
        query_name = query_name.replace('“', '')
        query_name = query_name.replace('”', '')

        file_path = f'{folder}/{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()[0])}-{query_name[:66]}.txt'
        if os.path.isfile(file_path): os.remove(file_path)

        with open(file_path, 'a') as file:
            for k, v in response.json().items():
                if k in ['news']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('description'):
                                    file.write('snippet: '.upper() +
                                               c.get('description') + '\n')
                                if c.get('url'):
                                    file.write('url: '.upper() +
                                               c.get('url') + '\n')
                                if c.get('image'):
                                    file.write(
                                        'image: '.upper() + c.get('image').get('contentUrl').split('?')[0] + '\n')
                                if c.get('datePublished'):
                                    file.write('DATE: '.upper() + c.get('datePublished').split('T')[
                                               0] + ' ' + c.get('datePublished').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')

                if k in ['videos']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('description'):
                                    file.write('snippet: '.upper() +
                                               c.get('description') + '\n')
                                if c.get('contentUrl'):
                                    file.write('url: '.upper() +
                                               c.get('contentUrl') + '\n')
                                if c.get('datePublished'):
                                    file.write('DATE: '.upper() + c.get('datePublished').split('T')[
                                               0] + ' ' + c.get('datePublished').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')

                if k in ['webPages']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('snippet'):
                                    file.write('snippet: '.upper() +
                                               c.get('snippet') + '\n')
                                if c.get('url'):
                                    file.write('url: '.upper() +
                                               c.get('url') + '\n')
                                if c.get('dateLastCrawled'):
                                    file.write('DATE: '.upper() + c.get('dateLastCrawled').split('T')[
                                               0] + ' ' + c.get('dateLastCrawled').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')
            return file_path

    except Exception as e:
        print(f"ERROR: Bing search failed: {e}")
        return    
    
def format_number(num):
    if not num:
        return 0
    if type(num) is dict:
        print(num)
        return 0
    if type(num) is not str and not float and not int:
        return num
    if type(num) is str:
        try:
            num = float(num)
        except Exception as e:
            return num
    positive = 1 if num >= 0 else -1
    num = abs(num)
    if num >= 1000:
        num = int(num)
        num = num * positive
        num = format(num, ',')
        return num
    if num >= 100:
        num = int(num)
        return num * positive
    if num >= 1:
        num = round(num, 2)
        return num * positive
    if num < 0.0001:
        if debug:
            print("DEBUG: format_number() no_need_to_change: ", num)
        return num * positive
    if num < 1:
        after_0_num = str(num).split('.')[-1]
        list_number = list(after_0_num)
        for i in range(len(list_number)):
            if int(list_number[i]) != 0:
                zero_num = i
                break
        num = round(num, zero_num + 3)
        return num * positive

def hash_md5(content):
    hashed_content = hashlib.md5(str(content).encode('utf-8')).hexdigest()
    return hashed_content

def hash_sha256(content):
    hashed_content = hashlib.sha256(str(content).encode('utf-8')).hexdigest()
    return hashed_content

def is_english(text):
    result = chardet.detect(text.encode())
    encoding = result['encoding']
    if encoding == 'ascii': return True
    lang = detect(text)
    if lang == 'en': return True

def markdown_wallet_address(wallet_address):
    markdown_address = f'[{wallet_address[:6]}...{wallet_address[-7:]}]({ETHERSCAN_WALLET_URL_PREFIX}{wallet_address})'
    return markdown_address

def markdown_transaction_hash(hash_tx):
    markdown_tx = f'[{hash_tx[:6]}......{hash_tx[-7:]}]({ETHERSCAN_TX_URL_PREFIX}{hash_tx})'
    return markdown_tx

def markdown_token_address(token_address):
    markdown_token = f'[{token_address[:6]}...{token_address[-7:]}]({ETHERSCAN_TOKEN_URL_PREFIX}{token_address})'
    return markdown_token

def markdown_tokentnxs(address):
    markdown_token = f'[{address[:6]}...{address[-7:]}]({ETHERSCAN_TOKEN_URL_PREFIX}{address}#tokentxns)'
    return markdown_token

def chat_gpt_regular(prompt, chatgpt_key=OPENAI_API_KEY, use_model=OPENAI_MODEL):
    if not prompt: return

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key

    response = openai.ChatCompletion.create(
        model=use_model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply

def chat_gpt_full(prompt, system_prompt='', user_prompt='', assistant_prompt='', dynamic_model=OPENAI_MODEL, chatgpt_key=OPENAI_API_KEY):
    if not prompt: return
    if not system_prompt: system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work."
    if not user_prompt: user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt: assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key
    if debug: print(f"DEBUG: {dynamic_model} 正在创作...")
    response = openai.ChatCompletion.create(
        model=dynamic_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply

def send_msg(message, chat_id, parse_mode='', base_url=telegram_base_url):
    if not message: return
    if not chat_id: return print(f"DEBUG: NO chat_id, only print:\n\n{message}")

    url = base_url + "sendMessage"
    payload = {
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
        "disable_notification": True,
        "reply_to_message_id": None,
        "chat_id": chat_id
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try: requests.post(url, json=payload, headers=headers)
    except Exception as e: return print(f"ERROR: send_msg() failed for:\n{e}\n\nOriginal message:\n{message}")
    if debug: print(f"DEBUG: send_msg(): chat_id: {chat_id} : {message}")
    return True

def send_audio(audio_path, chat_id, base_url=telegram_base_url):
    if not audio_path or not chat_id: return
    if debug: print(f"DEBUG: send_audio()")

    url = base_url + 'sendAudio'
    # send the audio message to the user
    try:
        with open(audio_path, 'rb') as audio_file:
            requests.post(url, data={'chat_id': chat_id}, files={'audio': audio_file})
    except Exception as e: print(f"ERROR: send_audio() failed : {e}")
    return

def send_img(chat_id, file_path, description='', base_url=telegram_base_url):
    if not file_path or not chat_id: return
    method = "sendPhoto?"
    try: files = {'photo': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_img() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = base_url + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR: send_img() failed : \n{e}")
    return r

def send_file(chat_id, file_path, description='', base_url=telegram_base_url):
    if not file_path or not chat_id: return
    method = "sendDocument?"
    try: files = {'document': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_file() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = base_url + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR: send_file() failed : \n{e}")
    return r

def tg_get_file_path(file_id):
    url = telegram_base_url + "getFile"
    payload = { "file_id": file_id}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200: return
        return response.json()['result']
    except Exception as e: return print(f"ERROR: tg_get_file_path() failed: \n{e}")

def replicate_img_to_caption(file_path):
    if debug: print(f"DEBUG: replicate_img_to_caption()")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_KEY

    model = replicate.models.get("salesforce/blip")
    version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
    inputs = {'image': open(file_path, "rb"), 'task': "image_captioning"}

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    output = ''
    try: output = version.predict(**inputs)
    except: pass
    return output

def convert_mp3_to_wav(mp3_file_path):
    if debug: print(f"DEBUG: convert_mp3_to_wav()")
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

# Using openai whisper api to convert voice to text
def from_voice_to_text(audio_path):
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
    if audio_path.endswith('ogg'):
        audio_path_mp3 = audio_path.replace('.ogg', '.mp3')
        command = f"ffmpeg -i {audio_path} {audio_path_mp3}"
        subprocess.run(command, shell=True)
    else: audio_path_mp3 = audio_path
    if debug: print(f"DEBUG: from_voice_to_text() audio_path_mp3: {audio_path_mp3}")

    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        'model': 'whisper-1',
    }
    with open(audio_path_mp3, 'rb') as f: 
        files = {'file': f}
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code != 200:
        raise Exception(f"Request to OpenAI failed with status {response.status_code}, {response.text}")
    '''
    {
    "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."
    }
    '''
    return response.json().get('text')

def from_voice_to_text_azure(audio_file_path):
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
    local_file_folder_name = f"files/audio/{file_unique_id}.ogg"
    # Get the file path of the voice message using the Telegram Bot API
    file_path_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_RUNNING}/getFile?file_id={file_id}"
    try: file_path_response = requests.get(file_path_url).json()
    except Exception as e: return print(f"ERROR: deal_with_voice_to_text() download failed: \n{e}")

    file_path = file_path_response["result"]["file_path"]
    # Download the voice message to your Ubuntu folder
    voice_message_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_RUNNING}/{file_path}"
    try:
        with open(local_file_folder_name, "wb") as f:
            response = requests.get(voice_message_url)
            f.write(response.content)
        text = from_voice_to_text(local_file_folder_name)
        if text: return text
    except Exception as e:  print(f"ERROR: from_voice_to_text() 2 FAILED of: \n\n{e}")
    return

def create_midjourney_prompt(prompt):

    system_prompt = midjourney_prompt_fomula if 'fomula' in prompt else midjourney_prompt_1
    prompt = prompt.replace('fomula', '').strip()

    try: beautiful_midjourney_prompt = chat_gpt_full(prompt, system_prompt, midjourney_user_prompt_fomula, midjourney_assistant_prompt_fomula, dynamic_model=OPENAI_MODEL, chatgpt_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"ERROR: create_midjourney_prompt() failed with error: \n{e}")
        return

    return beautiful_midjourney_prompt

def stability_generate_image(text_prompts, cfg_scale=7, clip_guidance_preset="FAST_BLUE", height=512, width=512, samples=1, steps=30, engine_id="stable-diffusion-xl-beta-v2-2-2"):
    response = requests.post(
        f"{STABILITY_URL}generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_prompts
                }
            ],
            "cfg_scale": cfg_scale,
            "clip_guidance_preset": clip_guidance_preset,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    file_path_list = []
    working_folder = 'files/images/dream_studio/'
    if not os.path.exists(working_folder): os.makedirs(working_folder)

    for i, image in enumerate(data["artifacts"]):

        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = hashlib.md5(
            (text_prompts+'_'+str(i)+'_'+str(current_timestamp)).encode()).hexdigest()
        filename_txt = filename + '.txt'
        filename_pic = filename + '.png'
        filepath_txt = f'{working_folder}/{filename_txt}'
        filepath_pic = f'{working_folder}/{filename_pic}'

        with open(filepath_pic, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
            file_path_list.append(filepath_pic)

        with open(filepath_txt, 'w') as f:
            f.write('\n'.join([str(i), text_prompts, current_timestamp, filename,
                    filepath_txt, filepath_pic]))

    return file_path_list

def st_find_ranks_for_word(key_word):
    df = pd.read_sql_query(f'SELECT * FROM db_daily_words WHERE word = "{key_word}"', engine)
    if df.empty: return 
    word_dict = df.iloc[0].to_dict()
    return word_dict

def chat_gpt_english(prompt, gpt_model=OPENAI_MODEL):
    if not prompt: return
    if debug: logging.info(f"chat_gpt_english() user prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": english_system_prompt},
            {"role": "user", "content": english_user_prompt},
            {"role": "assistant", "content": english_assistant_prompt},
            # {"role": "user", "content": 'Vector database technology has continued to improve, offering better performance and more personalized user experiences for customers.'},
            # {"role": "assistant", "content": '/英译中:\n矢量数据库技术一直在不断改进, 为客户提供更佳的性能和更个性化的用户体验。'},
            # {"role": "user", "content": '''To address the challenges of digital intelligance in digital economy, artificial intelligence generate content (AIGC) has emerge. AIGC use artificial intalligence to assist or replace manual content generation by generating content based on userinputted keywords or requirements. '''},
            # {"role": "assistant", "content": english_assistant_prompt_2},
            # {"role": "user", "content": '''vector database'''},
            # {"role": "assistant", "content": english_assistant_prompt_3},
            # {"role": "user", "content": '''LLaMA'''},
            # {"role": "assistant", "content": english_assistant_prompt_4},
            {"role": "user", "content": prompt},
            ]
        )
    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()
    return reply

# 定义一个 chat_gpt_english() 的前置函数, 先检查用户的 prompt 是否在历史数据库中出现过, 如果出现过就直接调用相应的 explanation_gpt, 如果没有记录就调用 chat_gpt_english() 生成新的 explanation 发给用户 from_id 并记录到数据库中
def chat_gpt_english_explanation(chat_id, prompt, gpt_model=OPENAI_MODEL):
    if not chat_id or not prompt: return
    prompt = prompt.lower().strip()
    with Session() as session:
        # 如果 fronm_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        explanation_exists = session.query(exists().where(GptEnglishExplanation.word == prompt)).scalar()
        if not explanation_exists:
            send_msg(f"收到, 我我去找 EnglishGPT 老师咨询一下 {prompt} 的意思, 然后再来告诉你 😗, 1 分钟以内答复你哈...", chat_id, parse_mode='', base_url=telegram_base_url)
            gpt_explanation=chat_gpt_english(prompt, gpt_model)
            new_explanation = GptEnglishExplanation(word=prompt, explanation=gpt_explanation, update_time=datetime.now(), gpt_model=gpt_model)
            session.add(new_explanation)
            session.commit()
        else: gpt_explanation = session.query(GptEnglishExplanation.explanation).filter(GptEnglishExplanation.word == prompt).first()[0]
    if gpt_explanation: send_msg(gpt_explanation, chat_id)
    return

'''    class GptStory(Base):
        __tablename__ = 'gpt_story'

        id = Column(Integer, primary_key=True, autoincrement=True)
        prompt = Column(Text)
        title = Column(String(255))
        story = Column(Text)
        gpt_model = Column(String(30))
        from_id = Column(String(255))
        chat_id = Column(String(255))
        update_time = Column(DateTime)
        '''

# 定义一个 GptStory 数据库插入函数, 用于记录用户的 prompt, title, story, gpt_mode, from_id, chat_id, update_time
def insert_gpt_story(prompt, title, story, gpt_model, from_id, chat_id):
    if not prompt or not story or not gpt_model or not from_id or not chat_id: return
    with Session() as session:
        new_story = GptStory(prompt=prompt, story=story, title=title, gpt_model=gpt_model, from_id=from_id, chat_id=chat_id, update_time=datetime.now())
        session.add(new_story)
        session.commit()
    return

# 定义一个 GptStory 数据库查询函数, 用于查询 from_id 用户的最新的一条 story 和 title
def get_gpt_story(from_id):
    if not from_id: return
    with Session() as session:
        story_exists = session.query(exists().where(GptStory.from_id == from_id)).scalar()
        if not story_exists: return
        title = session.query(GptStory.title).filter(GptStory.from_id == from_id).order_by(GptStory.update_time.desc()).first()[0]
        story = session.query(GptStory.story).filter(GptStory.from_id == from_id).order_by(GptStory.update_time.desc()).first()[0]
    return title, story

def chat_gpt_write_story(chat_id, from_id, prompt, gpt_model=OPENAI_MODEL):
    if not prompt: return
    try:
        if debug: logging.info(f"chat_gpt_write_story() user prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": kids_story_system_prompt},
                {"role": "user", "content": kids_story_user_prompt},
                {"role": "assistant", "content": kids_story_assistant_prompt},
                {"role": "user", "content": prompt},
                ]
            )
        story = response['choices'][0]['message']['content']
        story = story.strip('\n').strip()
        title = story.split('\n')[0]
        title = str(title).capitalize()
        insert_gpt_story(prompt, title, story, gpt_model, from_id, chat_id)
        send_msg(story, chat_id)
        send_msg(confirm_read_story_guide, chat_id)
        return 
    
    except Exception as e: logging.error(f"chat_gpt_write_story():\n\n{e}") 
    return 

# Mark user is_paid
def mark_user_is_paid(from_id, next_payment_time):
    if not from_id: return
    with Session() as session:
        # 如果 fronm_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        user_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if not user_exists:
            new_user = UserPriority(user_from_id=from_id, is_paid=1, next_payment_time=next_payment_time)
            session.add(new_user)
            session.commit()
            print(f"DEBUG: mark_user_is_paid() {from_id} 已经插入到 avatar_user_priority 表中, is_paid = 1, next_payment_time = {next_payment_time}")
            return True
        session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update({"is_paid": 1, "next_payment_time": next_payment_time})
        session.commit()
        print(f"DEBUG: mark_user_is_paid() {from_id} 已经更新到 avatar_user_priority 表中, is_paid = 1, next_payment_time = {next_payment_time}")
        return True

# Mark user is not paid
def mark_user_is_not_paid(from_id):
    if not from_id: return
    with Session() as session:
        # 如果 from_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        user_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if not user_exists:
            new_user = UserPriority(user_from_id=from_id, is_paid=0)
            session.add(new_user)
            session.commit()
            print(f"DEBUG: mark_user_is_not_paid() {from_id} 已经插入到 avatar_user_priority 表中, is_paid = 0")
            return True
        session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update({"is_paid": 0})
        session.commit()
        print(f"DEBUG: mark_user_is_not_paid() {from_id} 已经更新到 avatar_user_priority 表中, is_paid = 0")
        return True

'''
class UserPriority(Base):
    __tablename__ = 'avatar_user_priority'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_from_id = Column(String(255), unique=True)
    priority = Column(Integer, default=0)
    is_blacklist = Column(Integer, default=0)
    free_until = Column(DateTime, default=datetime.now())
    is_admin = Column(Integer, default=0)
    is_owner = Column(Integer, default=0)
    is_vip = Column(Integer, default=0)
    is_paid = Column(Integer, default=0)
    is_active = Column(Integer, default=0)
    is_deleted = Column(Integer, default=0)
    update_time = Column(DateTime, default=datetime.now())
    next_payment_time = Column(DateTime, default=datetime.now())
    '''
# 从 UserPriority 表中查询给定 from_id 的用户的优先级, 返回一个字典
def get_user_priority(from_id):
    if not from_id: return None
    user_priority = {}
    try:
        query = f'SELECT * FROM avatar_user_priority WHERE user_from_id = "{from_id}"'
        result = pd.read_sql_query(query, engine)
        if not result.empty: user_priority = result.iloc[0].to_dict()
    except Exception as e: print(f"ERROR: get_user_priority() failed: {e}")
    return user_priority


# 从 Coinmarketcap 查询给定 token 的 cmc_rank、price、market_cap、volume_24h、 percent_change_24h、market_cap、fully_diluted_market_cap、circulating_supply、total_supply、last_updated 等数据, 返回一个字典
def get_token_info_from_coinmarketcap_output_chinese(token_symbol):
    token_info = get_token_info_from_coinmarketcap(token_symbol)
    if not token_info: return {}
    output_dict = {
        '名称': token_info['name'],
        '排名': token_info['cmc_rank'],
        '现价': f"{format_number(token_info['quote']['USD']['price'])} usd/{token_symbol.lower()}",
        '交易量': f"{format_number(token_info['quote']['USD']['volume_24h'])} usd",
        '流通市值': f"{format_number(token_info['quote']['USD']['market_cap'])} usd | {token_info['circulating_supply'] / token_info['total_supply'] * 100:.1f}%",
        '24小时波动': f"{token_info['quote']['USD']['percent_change_24h']:.2f}%",
        '全流通市值': f"{format_number(token_info['quote']['USD']['fully_diluted_market_cap'])} usd",
        '代币总发行': f"{format_number(token_info['total_supply'])} {token_symbol.lower()}",
        '本次更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    # 用 '\n' join k: v
    output_dict_str = '\n'.join([f"{k}: {v}" for k, v in output_dict.items()])
    return output_dict_str

# 判断输入的 hash_tx 是否已经存在 avatar_crypto_payments 表中, 如果不存在, 则插入到表中
def insert_into_avatar_crypto_payments(from_id, coin, to_address, value, timestamp, hash_tx, user_title):
    if debug: print(f"DEBUG: insert_into_avatar_crypto_payments()")
    hash_tx = hash_tx.lower()
    coin = coin.upper()
    if coin not in ['USDT', 'USDC']: return
    # 如果 value 小于 1 则返回
    value = float(value)
    if value == 0:
        # 先将 hash_tx 数据插入表中, 以后再来更新 value 数据
        with Session() as session:
            # Query the table 'avatar_crypto_payments' to check if the hash_tx exists
            hash_tx_exists = session.query(exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
            if hash_tx_exists: 
                print(f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 但是 value 为 0, 不需要更新!")
                return

            update_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            new_crypto_payment = CryptoPayments(user_from_id=from_id, address=to_address, usdt_paid_in=0, usdc_paid_in=0, update_time=update_time, Hash_id=hash_tx)
            session.add(new_crypto_payment)
            session.commit()
            print(f"DEBUG: hash_tx {hash_tx} 已经插入到 avatar_crypto_payments 表中, value 为 0, 需要下次更新!")
            send_msg(f"亲爱的, 你的交易 Transaction Hash {markdown_transaction_hash(hash_tx)} 已经系统被记录下来了, 但是链上还没有确认成功, 请过几分钟等下你再点击 /check_payment 试试看, 谢谢亲! 如果系统查到链上已确认, 你就不会收到这条消息了。\n\n如果你看到链上确认成功了, 但是等了太久我都没有给你确认, 或者你总是收到这条消息, 请联系 {TELEGRAM_USERNAME} 手动帮你查看是否到账, 麻烦亲爱的了。😗", from_id, parse_mode='Markdown')
        return 
    
    else:
        # Create a new session
        with Session() as session:
            # Query the table 'avatar_crypto_payments' to check if the hash_tx exists
            hash_tx_exists = session.query(exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
            if hash_tx_exists: 
                # 判断 usdt_paid_in 和 usdc_paid_in 是否已经存在, 并且有一个等于 value, 如果是则返回
                crypto_payment = session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).first()
                if crypto_payment.usdt_paid_in == value or crypto_payment.usdc_paid_in == value: 
                    print(f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 且记录的 value 和新输入的 value 相等: {value}, 不需要更新!")
                    return
                else:
                    # 如果 usdt_paid_in 和 usdc_paid_in 都不等于 value, 则更新 usdt_paid_in 或 usdc_paid_in
                    if coin == 'USDT': session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).update({CryptoPayments.usdt_paid_in: value})
                    if coin == 'USDC': session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).update({CryptoPayments.usdc_paid_in: value})
                    print(f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 但是记录的 value 和新输入的 value 不相等: {value}, 表单已经更新!")
            else:
                update_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                # Insert the hash_tx into the table 'avatar_crypto_payments'
                usdt_paid_in = value if coin == 'USDT' else 0
                usdc_paid_in = value if coin == 'USDC' else 0

                new_crypto_payment = CryptoPayments(user_from_id=from_id, address=to_address, usdt_paid_in=usdt_paid_in, usdc_paid_in=usdc_paid_in, update_time=update_time, Hash_id=hash_tx)
                session.add(new_crypto_payment)
                session.commit()
                print(f"DEBUG: hash_tx {hash_tx} 已经插入到 avatar_crypto_payments 表中, value 为 {value}, 更新完毕!")

            next_payment_time = update_time + timedelta(days=(value / MONTHLY_FEE) * 31)
            if next_payment_time < datetime.now(): 
                mark_user_is_not_paid(from_id)
                return

            elif mark_user_is_paid(from_id, next_payment_time):
                send_msg(f"叮咚, {user_title} {from_id} 刚刚到账充值 {format_number(value)} {coin.lower()}\n\n充值地址: \n{markdown_wallet_address(to_address)}\n\n交易哈希:\n{markdown_transaction_hash(hash_tx)}", BOTOWNER_CHAT_ID, parse_mode='Markdown')
                send_msg(f"亲爱的, 你交来的公粮够我一阵子啦 😍😍😍, 下次交公粮的时间是: \n\n{next_payment_time} \n\n你可别忘了哦, 反正到时候我会提醒你哒, 么么哒 😘", from_id)
            
                next_payment_time_dict = {'last_paid_usd_value': value, 'last_paid_time': update_time, 'next_payment_time': next_payment_time}
                return next_payment_time_dict
    return

def check_incoming_transactions(wallet_address, token_address, chat_id, start_date=None):

    token_address = web3.to_checksum_address(token_address)
    wallet_address = web3.to_checksum_address(wallet_address)

    # 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息
    coin_list_df = get_token_info_from_db_cmc_total_supply(token_address)
    if coin_list_df.empty: 
        send_msg(f"抱歉, {token_address} 不在我的数据库里, 不清楚这是个什么币子, 无法查询. 😰", chat_id)
        return
    
    token_address = coin_list_df.iloc[0]['token_address']
    imple_address = coin_list_df.iloc[0]['imple_address']
    coin = coin_list_df.iloc[0]['symbol']
    decimals = int(coin_list_df.iloc[0]['decimals'])

    # Dealing with erc20_symbol and ABI
    ABI = get_token_abi(imple_address)
    
    # Create a contract instance for the ERC20 token
    token_contract = web3.eth.contract(address=token_address, abi=ABI)
    
    if start_date: start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    else: start_timestamp = int(datetime.now().timestamp())

    # Get the latest block number
    latest_block_number = web3.eth.block_number
    
    transactions = []
    # Iterate through each block from the latest to the earliest
    for block_number in range(latest_block_number):
        print(f'DEBUG: checking block_number: {block_number} / {latest_block_number}')
        block = web3.eth.get_block(block_number, full_transactions=True)
        for transaction in block.transactions:
            if transaction['to'] == wallet_address and transaction['input'] != '0x':
                tx_receipt = web3.eth.get_transaction_receipt(transaction['hash'])
                contract_address = tx_receipt['to']
                if contract_address.lower() == '0xtoken_contract_address'.lower():
                    input_data = transaction['input']
                    method_id = input_data[:10]
                    if method_id.lower() == '0xa9059cbb':  # Transfer method ID
                        token_address = '0x' + input_data[34:74]
                        if token_address.lower() == wallet_address.lower():
                            token_amount = int(input_data[74:], 16) / 10 ** 18
                            token_symbol = token_contract.functions.symbol().call()
                            if token_symbol.lower() == coin.lower() and block.timestamp >= start_timestamp:
                                transactions.append({
                                    'token_amount': token_amount,
                                    'block_number': block_number,
                                    'from_address': transaction['from'],
                                    'block_timestamp': block.timestamp,
                                    'transaction_hash': transaction['hash']
                                })
    
    return transactions

def get_internal_transactions(transaction_hash):
    url = f"https://deep-index.moralis.io/api/v2/transaction/{transaction_hash}/internal-transactions?chain=eth"
    headers = {
        "accept": "application/json",
        "X-API-Key": MORALIS_API
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle error case
        return None

''' return from get_internal_transactions()
[
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "523700",
        "gas_used": "29724",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da2000000000000000000000000f1837f9d36e2052496d0983ade9fdb4855d29aa6000000000000000000000000000000000000000000000000000000000bebc200",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "493825",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da200000000000000000000000066e1ccd77ff59bd17379c895a2320ad0d8c7f127000000000000000000000000000000000000000000000000000000001dcd6500",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "466411",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da2000000000000000000000000d74b5fdd0d8de1f1345f4d50a76b9303d85c12700000000000000000000000000000000000000000000000000000000013d92d40",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "438997",
        "gas_used": "10124",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da20000000000000000000000001fe9613aa4d6600bd9133df9c9dc35db80dd74560000000000000000000000000000000000000000000000000000000005f5e100",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "428416",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da2000000000000000000000000cb95b2cd2fcd8fd98a5d4dd7a618d834f0f66ebc0000000000000000000000000000000000000000000000000000000008954400",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "401002",
        "gas_used": "10124",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da20000000000000000000000005e278a70193f214c3536fd6f1d298a5eaef5279500000000000000000000000000000000000000000000000000000000ee6b2800",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "390421",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da2000000000000000000000000946bec3d83ace597d589b5b19dc447ddd69893b800000000000000000000000000000000000000000000000000000000f8e42020",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "363007",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da20000000000000000000000005fa75f28ca27dad4220e4cf074cff75598fa81300000000000000000000000000000000000000000000000000000000087b64770",
        "output": ""
    },
    {
        "transaction_hash": "0x4916b179936f2a9cd9d65a3433b32ece96bfbe5cad81951763b20d366bbfc1fd",
        "block_number": 17163179,
        "block_hash": "0x2bf2019595a5b551820d28a045c0b533479689f4851ce60d7a6f4bd825947544",
        "type": "CALL",
        "from": "0xa4994144a9217e3779bda588798eff546b69defb",
        "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "value": "0",
        "gas": "335594",
        "gas_used": "27224",
        "input": "0x23b872dd0000000000000000000000001308e4e09ecdeea174a7e160e74da8dda41d1da2000000000000000000000000c46d4d0e6c8fd624b46d73ca88baef2903dbb7160000000000000000000000000000000000000000000000000000000069e89450",
        "output": ""
    }
]
'''

def get_transaction_details(transaction_hash, chain='eth'):
    url = f'https://deep-index.moralis.io/api/v2/transaction/{transaction_hash}?chain={chain}'
    headers = {'accept': 'application/json', 'X-API-Key': MORALIS_API}
    response = requests.get(url, headers=headers)
    # print(response.status_code, response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Request failed with status code: {response.status_code}')
        return None

# 通过 hash_tx 查询转账信息
def get_transactions_info_by_hash_tx(hash_tx, chat_id, user_title, chain='eth'):
    hash_tx = str(hash_tx).lower()
    if not hash_tx.startswith('0x') and len(hash_tx) == 64: hash_tx = '0x' + hash_tx
    if len(hash_tx) != 66: 
        return send_msg(f"输入的 hash_tx 长度不对, 请回复正确的 Transaction_Hash: 0x开头, 一共 66 位字符 😃", chat_id)
    trans_info = get_transaction_details(hash_tx, chain=chain)

    if not trans_info: 
        send_msg(f"抱歉, 无法查询到 {hash_tx} 的转账信息, 请检查输入是否正确. 😰", chat_id)
        return 
    if not trans_info.get('input'): 
        send_msg(f"抱歉, 查到的信息有问题, 无法正确读取. 😰", chat_id)
        return 
    if trans_info.get('value') != '0': 

        '''
            {
                "hash": "0x76e669a454257ac506d62ef55b6123b7a6c592b276922aa051eac5b00a9dad97",
                "nonce": "92",
                "transaction_index": "113",
                "from_address": "0x5e278a70193f214c3536fd6f1d298a5eaef52795",
                "to_address": "0x4408d8991d9f4419a53487fe2027223ba5cf2207",
                "value": "7800000000000000000",
                "gas": "21000",
                "gas_price": "16198064885",
                "input": "0x",
                "receipt_cumulative_gas_used": "14258140",
                "receipt_gas_used": "21000",
                "receipt_contract_address": null,
                "receipt_root": null,
                "receipt_status": "1",
                "block_timestamp": "2023-03-24T23:33:11.000Z",
                "block_number": "16900645",
                "block_hash": "0xa9adb1f2efa884db49704aaa4067c52dd8987b454074476f4e6eb0da0b0c2bce",
                "transfer_index": [
                    16900645,
                    113
                ],
                "logs": [],
                "decoded_call": null
            }
            '''

        eth_value = int(trans_info.get('value')) / 1_000_000_000_000_000_000
        send_msg(f"亲爱的, 这是一笔 ETH 转账 🤩:\n\n转账数额: {format_number(eth_value)} eth\n转账地址: {markdown_wallet_address(trans_info.get('from_address'))}\n收款地址: {markdown_wallet_address(trans_info.get('to_address'))}\n交易确认: {markdown_transaction_hash(hash_tx)}", chat_id, parse_mode='Markdown', base_url=telegram_base_url)

        return 
    
    token_address = trans_info.get('to_address')
    
    # 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息
    coin_list_df = get_token_info_from_db_cmc_total_supply(token_address)
    if coin_list_df.empty: 

        internal_trans_list = get_internal_transactions(hash_tx)
        if type(internal_trans_list) != list: 
            send_msg(f"抱歉, {markdown_token_address(token_address)} 不在我的数据库里, 不清楚这是个什么币子, 无法查询. 😰", chat_id, parse_mode='Markdown')
            return
        # 将 internal_trans_list 保存为 Json 文件, 在 files/transactions 文件夹下保存文件, filename=hash_tx.json, 并用 send_file 发给用户
        file_path = f"files/transactions/{hash_tx}.json"
        with open(file_path, 'w') as f: json.dump(internal_trans_list, f, indent=2)
        send_file(chat_id, file_path)
        send_msg(f"亲爱的, 发的的这个看起来是一个智能合约交互的记录, 有点复杂, 我保存下来发给你看看吧. 我也看不明白, 建议你可以点击下面的链接去 Etherscan 页面上看看, 那边的解读清晰一点哈 😅, 抱歉我帮不了你啊, 我还不够厉害, 我还要继续学习, 继续努力。不行你把文件内容拷贝黏贴给 ChatGPT, 让他帮你解读一下这个智能合约的交互怎么回事, 是什么样的交互, 交易金额多大。\n\n{markdown_transaction_hash(hash_tx)}", chat_id, parse_mode='Markdown', base_url=telegram_base_url)
        return 
    
    token_address = coin_list_df.iloc[0]['token_address']
    imple_address = coin_list_df.iloc[0]['imple_address']
    coin = coin_list_df.iloc[0]['symbol']
    decimals = int(coin_list_df.iloc[0]['decimals'])
	
    if debug: print(f"DEBUG: 找到输入的 HashId 交易的币种是: {coin}, decimals: {decimals}")

    # Dealing with erc20_symbol and ABI
    ABI = get_token_abi(imple_address)
    contract = web3.eth.contract(token_address, abi=ABI)
    from_address = trans_info['from_address']
    from_address = web3.to_checksum_address(from_address)
    from_addr_balance_wei = contract.functions.balanceOf(from_address).call()
    from_addr_balance = float(from_addr_balance_wei / 10 ** decimals)
    func_obj, func_params = contract.decode_function_input(trans_info.get('input'))
    '''return : {'to': '0x376FA5C248EECB0110023efADD8317691B07EDe1', 'value': 56195000000}'''
    try:
        func_params['value'] = func_params.get('amount') if 'amount' in func_params else func_params.get('_value') if '_value' in func_params else func_params.get('value')
        func_params['to'] = func_params.get('recipient') if 'recipient' in func_params else func_params.get('_to') if '_to' in func_params else func_params.get('to')
        func_params['value'] = float(float(func_params.get('value')) / (10 ** decimals)) if func_params.get('value') else 0
        func_params['status'] = True if trans_info.get('receipt_status') == '1' else False
        func_params['data'] = trans_info.get('input')
        # func_params['gas_cost'] = float(trans_info['receipt_cumulative_gas_used']) * eth_price * 1_000_000_000
        func_params['from_address'] = from_address
        func_params['from_addr_balance'] = from_addr_balance + func_params['value']
        func_params['token_address'] = token_address
        func_params['decimals'] = decimals
        func_params['coin'] = coin
        func_params['block_timestamp'] = trans_info['block_timestamp']
        to_address = func_params.get('to')
        if chat_id:
            r = {
                '转账通证': coin,
                '转账金额': format_number(func_params['value']),
                '发出地址': markdown_wallet_address(from_address),
                '目标地址': markdown_wallet_address(to_address),
                '确认时间': ' '.join(str(trans_info['block_timestamp']).split('.')[0].split('T'))
                }
            # 用 '\n' join k: v from r
            r = '\n'.join([f"{k}: {v}" for k, v in r.items()])
            send_msg(r, chat_id, parse_mode='Markdown')

        # 检查 to_address 是否在 table avatar_eth_wallet, 如果在, 说明这是用户的充值地址, 需要本次交易的信息写入 avatar_crypto_payments
        from_id = get_from_id_by_eth_address(to_address)
        if from_id and from_id in [chat_id] + BOT_OWNER_LIST:

            '''func_params:
            {"to": "0x5e278a70193F214C3536FD6f1D298a5eaeF52795", "value": 100.0, "status": true, "data": "0xa9059cbb0000000000000000000000005e278a70193f214c3536fd6f1d298a5eaef527950000000000000000000000000000000000000000000000000000000005f5e100", "from_address": "0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377", "from_addr_balance": 2512.718824, "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6, "coin": "USDC", "block_timestamp": "2023-03-11T22:25:59.000Z"}'''

            '''class CryptoPayments(Base):
                    __tablename__ = 'avatar_crypto_payments'

                    id = Column(Integer, primary_key=True, autoincrement=True)
                    user_from_id = Column(String(255))
                    address = Column(String(255))
                    usdt_paid_in = Column(Float, default=0)
                    usdc_paid_in = Column(Float, default=0)
                    eth_paid_in = Column(Float, default=0)
                    update_time = Column(DateTime)
                    Hash_id = Column(Text)
            '''

            # 将最新获取的交易信息写入 avatar_crypto_payments
            try: 
                func_params['value'] = 0 if not func_params['status'] else func_params['value']
                next_payment_time_dict= insert_into_avatar_crypto_payments(from_id, coin, to_address, func_params['value'], func_params['block_timestamp'], hash_tx, user_title)
            except Exception as e: print(f"ERROR: insert_into_avatar_crypto_payments() failed: \n{e}")
            
        return next_payment_time_dict
    except Exception as e: print('DEBUG: get_transactions_info_by_hash_tx() error: ', e)
    return

# 计算用户下次需要续费的时间是哪天, 返回一个 datetime 对象
def update_user_next_payment_date(user_from_id, user_title):
    if debug: print(f"DEBUG: update_user_next_payment_date()")
    # Create a new session
    with Session() as session:
        # 用 pandas 从表单中读出 from_id 对应最后一笔 crypto payment 的数据, 判断 usdt_paid_in 和 usdc_paid_in 哪个不是 0, 并将不为零的 value 和 update_time 读出一并返回
        crypto_payments = session.query(CryptoPayments).filter(CryptoPayments.user_from_id == user_from_id).order_by(CryptoPayments.id.desc()).first()
        if crypto_payments:
            value = crypto_payments.usdt_paid_in if crypto_payments.usdt_paid_in else crypto_payments.usdc_paid_in if crypto_payments.usdc_paid_in else 0
            if value:  
                # 计算下次下次缴费时间
                x = value / MONTHLY_FEE
                next_payment_time = crypto_payments.update_time + timedelta(days=x * 31)
                if next_payment_time > datetime.now():
                    next_payment_time_dict = {'last_paid_usd_value': value, 'last_paid_time': crypto_payments.update_time, 'next_payment_time': next_payment_time}
                    return next_payment_time_dict
            if crypto_payments.Hash_id: return get_transactions_info_by_hash_tx(crypto_payments.Hash_id, user_from_id, user_title, chain='eth')
    return 
    
def get_outgoing_transactions_from_address_in_24h(wallet_address):
    url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/verbose"
    
    # Get the date and time 24 hours ago
    from_date = datetime.now() - timedelta(days=1)
    from_date_formatted = datetime.strftime(from_date, "%Y-%m-%dT%H:%M:%S")

    headers = {
        'accept': 'application/json',
        'X-API-Key': MORALIS_API,
    }
    
    params = {
        'chain': 'eth',
        'from_date': from_date_formatted
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200: return response.json()
    else: return None

def read_outgoing_transaction_in_24h_result(wallet_address):
    result = get_outgoing_transactions_from_address_in_24h(wallet_address)

    transaction_list = []
    
    for transaction in result['result']:
        if not transaction.get('logs'): continue

        decoded_event = transaction['logs'][0]['decoded_event']
        token_address = transaction['logs'][0]['address']
        if token_address.lower() not in [USDT_ERC20.lower(), USDC_ERC20.lower()]: continue

        token_name = 'USDT' if token_address.lower() == USDT_ERC20.lower() else 'USDC'

        transfer_info = {}
        for param in decoded_event['params']:
            transfer_info[param['name']] = param['value']

        timestamp = convert_to_local_timezone(transaction['block_timestamp'])

        transaction_info = {
            '币种名称': token_name,  # Replace with your function to retrieve the token name
            '发起地址': markdown_wallet_address(transfer_info['from']),
            '收币地址': markdown_wallet_address(transfer_info['to']),
            '转账数量': format_number(int(transfer_info['value']) / (10 ** USDT_ERC20_DECIMALS)),  # Replace with your function to retrieve the token decimals
            '西岸时间': timestamp,
        }
        
        transaction_list.append(transaction_info)

    return transaction_list

def read_and_send_24h_outgoing_trans(wallet_address, chat_id):
    # wallet_address = web3.to_checksum_address(wallet_address)
    transaction_list =  read_outgoing_transaction_in_24h_result(wallet_address)
    if not transaction_list: return

    total_transactions_count = len(transaction_list)
    msg_info = f"亲爱的, {wallet_address[:5]}...{wallet_address[-5:]} 钱包地址 24 小时内一共有 {total_transactions_count} 笔 USDT/USDC 转出记录😍, 倒序排列如下: "
    send_msg(msg_info, chat_id)
    if total_transactions_count > 10: transaction_list = transaction_list[:10]
    i = 0
    for transaction in transaction_list:
        i += 1
        r = '\n'.join([f"{k}: {v}" for k, v in transaction.items()])
        send_msg(f"第{i}笔:\n{r}", chat_id, parse_mode='Markdown', base_url=telegram_base_url)
    if total_transactions_count > 10: send_msg(f"还有 {total_transactions_count - 10} 笔转账记录, 请到 Etherscan 上查看哈:\n{markdown_wallet_address(wallet_address)}", chat_id, parse_mode='Markdown', base_url=telegram_base_url)
    return

def microsoft_azure_tts(text, voice='zh-CN-YunxiNeural', output_filename='output.wav'):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=output_filename)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted: return output_filename
    return False

def create_news_podcast(filepath = '', prompt = '', openai_model=OPENAI_MODEL):
    if not filepath and not prompt: return 

    if filepath and not prompt: 
        with open(filepath, 'r') as f: prompt = f.read()

    if not prompt: return

    message = chat_gpt_full(prompt, news_reporter_system_prompt, news_reporter_user_prompt, news_reporter_assistant_prompt, openai_model, OPENAI_API_KEY)

    filepath_news = filepath.replace('_snippet.txt', '_news.txt')
    with open(filepath_news, 'w') as f: f.write(message)

    filepath_news_mp3 = filepath_news.replace('.txt', '.mp3')
    if filepath_news: filepath_news_mp3 = microsoft_azure_tts(message, 'en-US-JaneNeural', filepath_news_mp3)

    return filepath_news_mp3

# 通过 ffmpeg 合并英文语音文件和中文语音文件
def merge_audio_files(audio_files):
    if len(audio_files) == 1: return audio_files[0]
    if len(audio_files) == 0: return None
    merged_audio = audio_files[0].replace('.mp3', '_merged.mp3')
    cmd = f"ffmpeg -i {audio_files[0]} -i {audio_files[1]} -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[out]' -map '[out]' {merged_audio}"
    os.system(cmd)
    return merged_audio

def create_news_and_audio_from_bing_search(query, chat_id, parse_mode='', base_url=telegram_base_url):
    filepath = bing_search(query, mkt='en-US')

    snippet_total = [f"Today's top news about {query}\n\n"]
    with open(filepath, 'r') as file:
        i = 1
        for line in file:
            if 'SNIPPET: ' in line: 
                snippet_total.append(line.replace('-','').replace('SNIPPET: ', f'{str(i)}. '))
                i += 1

    snippet_text_filepath = filepath.replace('.txt', '_snippet.txt')
    with open(snippet_text_filepath, 'w') as file:
        for line in snippet_total:
            file.write(line + '\n')

    filepath_news_mp3 = create_news_podcast(snippet_text_filepath, prompt = '')
    filepath_news_txt = filepath_news_mp3.replace('.mp3', '.txt')
    with open(filepath_news_txt, 'r') as f: text_contents = f.read()

    send_msg(text_contents, chat_id, parse_mode, base_url)

    # filepath_news_txt_cn = filepath_news_txt.replace('.txt', '_cn.txt')
    text_cn = chat_gpt_regular(f"{translate_report_prompt}{text_contents}", OPENAI_API_KEY, OPENAI_MODEL)

    # 将中文文本添加至英文文本的末尾
    with open(filepath_news_txt, 'a') as file: file.write(text_cn)
    # with open(filepath_news_txt_cn, 'w') as file: file.write(text_cn)
    send_msg(text_cn, chat_id, parse_mode=parse_mode, base_url=base_url)
    send_file(chat_id, filepath_news_txt, description='中英文内容 Text 文件', base_url=base_url)

    filepath_news_mp3_cn = filepath_news_mp3.replace('.mp3', '_cn.mp3')
    filepath_news_mp3_cn = microsoft_azure_tts(text_cn, 'zh-CN-YunxiNeural', filepath_news_mp3_cn)

    merged_audio = merge_audio_files([filepath_news_mp3, filepath_news_mp3_cn])
    send_audio(merged_audio, chat_id, base_url=base_url)

    # 基于 text_contents 写一段 英文 Tweet 和一段中文 Tweet
    tweet_content = chat_gpt_regular(f"{tweet_pre_prompt_for_report}{text_contents}")
    send_msg(tweet_content, chat_id, parse_mode=parse_mode, base_url=base_url)

    return

# 定义一个TTS 函数, 判断输入的内容是中文还是英文, 然后调用不同的 TTS API 创建并返回filepath, 如果提供了 chat_id, 则将 filepath send_audio 给用户
def create_audio_from_text(text, chat_id=''):
    if not text: return 
    filepath = f"files/audio/{chat_id}_{text[:10]}.mp3" if chat_id else f"files/audio/no_chat_id_{text[:10]}.mp3"

    if is_english(text):  new_filepath = microsoft_azure_tts(text, 'en-US-JennyNeural', filepath)
    else:  new_filepath = microsoft_azure_tts(text, 'zh-CN-YunxiNeural', filepath)
    if new_filepath and os.path.isfile(new_filepath): 
        send_audio(new_filepath, chat_id)
        return new_filepath

def convert_m4a_to_wav(m4a_file):
    if debug: print(f"DEBUG: convert_m4a_to_wav() {m4a_file}")
    # Set output file name based on M4A file name
    output_file = m4a_file[:-4] + '.wav'

    # Convert the M4A file to WAV using FFmpeg
    os.system(f'ffmpeg -y -i {m4a_file} -acodec pcm_s16le -ar 44100 {output_file}')

    # Print success message
    if debug: print(f'DEBUG: convert_m4a_to_wav() output : {output_file}')
    return output_file


def get_elevenlabs_userinfo(elevenlabs_api_key):
    url = "https://api.elevenlabs.io/v1/user"
    headers = {
        "accept": "application/json",
        "xi-api-key": elevenlabs_api_key
    }
    response = requests.get(url, headers=headers)
    return response.json().get('subscription', {})
'''
{
  "subscription": {
    "tier": "creator",
    "character_count": 18107,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
  },
  "is_new_user": true,
  "xi_api_key": "7506563f79bd85dbf7dade0cc8412b42",
  "can_use_delayed_payment_methods": false
}
'''
# r = get_elevenlabs_userinfo()
# print(json.dumps(r, indent=2))

'''
    class ElevenLabsUser(Base):
        __tablename__ = 'elevenlabs_user'

        id = Column(Integer, primary_key=True, autoincrement=True)
        from_id = Column(String(255))
        elevenlabs_api_key = Column(String(255))
        voice_id = Column(Text)
        last_time_voice_id = Column(String(255))
        original_voice_filepath = Column(String(255))
        test_count = Column(Integer, default=0)

        '''
# 当用户每次提交 elevenlabs_api_key 的时候, 需要检查用户输入的 elevenlabs_api_key 是否有效, 并将 get_elevenlabs_userinfo 返回的结果中的 subscription 写入数据库, 再通过 get_elevenlabs_voices 获得目前的 voice_id dict
def check_and_save_elevenlabs_api_key(elevenlabs_api_key, from_id):
    subscription = get_elevenlabs_userinfo(elevenlabs_api_key)
    if subscription:
        if subscription.get('status') == 'active' and subscription.get('can_use_instant_voice_cloning') == True:
            if debug: print(f"DEBUG: check_elevenlabs_api_key() subscription: {subscription}")
            # 将 from_id, elevenlabs_api_key 插入ElevenLabsUser
            with Session() as session:
                # 如果表单不存在则创建表单
                Base.metadata.create_all(engine, checkfirst=True)
                # 检查 from_id 是否在 ElevenLabsUser 表中, 如果不在, 则创建新的记录, 如果在, 则更新 elevenlabs_api_key
                elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
                if not elevenlabs_user:
                    elevenlabs_user = ElevenLabsUser(from_id=from_id, elevenlabs_api_key=elevenlabs_api_key)
                    session.add(elevenlabs_user)
                else: 
                    # 更新 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key
                    session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'elevenlabs_api_key': elevenlabs_api_key})
                session.commit()
            send_msg(elevenlabs_apikey_saved, from_id)
            return subscription
        else: 
            subscription_string = '\n'.join([f"{k}: {v}" for k, v in subscription.items()])
            failed_notice = f"{elevenlabs_not_activate}\n\n你的订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
            return send_msg(failed_notice, from_id)
    else: return send_msg(elevenlabs_not_activate, from_id)

# 根据 from_id 读取用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id
def get_elevenlabs_api_key(from_id):
    with Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id 和 user_title
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if elevenlabs_user: return elevenlabs_user.elevenlabs_api_key, elevenlabs_user.original_voice_filepath, elevenlabs_user.voice_id, elevenlabs_user.user_title
        else: return None, None, None, None

# 将 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段更新为 1, user_title 更新为 user_title
def update_elevenlabs_user_ready_to_clone(from_id, user_title):
    with Session() as session:
        # 如果用户存在, 则更新 ready_to_clone 字段为 1, 如果不存在则顺便创建
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if not elevenlabs_user:
            elevenlabs_user = ElevenLabsUser(from_id=from_id, ready_to_clone=1, user_title=user_title)
            session.add(elevenlabs_user)
        else:
            session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'ready_to_clone': 1, 'user_title': user_title})
        session.commit()
    return True

# 将输入的 original_voice_filepath 和 from_id 和 user_title 更新到 ElevenLabsUser 表中
def update_elevenlabs_user_original_voice_filepath(original_voice_filepath, from_id, user_title):
    with Session() as session:
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'original_voice_filepath': original_voice_filepath, 'user_title': user_title})
        session.commit()
    return True

# 并将 ready_to_clone 字段更新为 0
def update_elevenlabs_user_ready_to_clone_to_0(from_id, user_title, cmd = 'close_clone_voice'):
    
    with Session() as session:
        # 读取表中的 original_voice_filepath, 如果为空, 则说明用户没有上传过语音文件, 返回 False
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if not elevenlabs_user: 
            # 将 from_id, user_title 插入ElevenLabsUser
            elevenlabs_user = ElevenLabsUser(from_id=from_id, ready_to_clone=0, user_title=user_title)
            session.add(elevenlabs_user)
            session.commit()

        if not elevenlabs_user.original_voice_filepath and cmd == 'confirm_my_voice': 
            send_msg("你还没有上传过语音素材文件哦, 克隆还没成功呢, 请先上传语音文件再点击:\n/confirm_my_voice\n\n如果不想克隆你的声音了, 请点击:\n/close_clone_voice", from_id)
            return 

        # 更新 ready_to_clone 字段为 0
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'ready_to_clone': 0})
        session.commit()
    if cmd == 'close_clone_voice': send_msg(f"@{user_title} 你已经成功关闭了克隆声音功能, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。", from_id)
    if cmd == 'confirm_my_voice': send_msg(f"@{user_title}, 你的声音训练素材已经保存好了, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。", from_id)
    return True

# 检查 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段是否为 1
def elevenlabs_user_ready_to_clone(from_id):
    with Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 ready_to_clone = 1 的记录, 如果无记录, 说明用户不存在或者 ready_to_clone 字段不为 1, 返回 False, 否则返回 True
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id, ElevenLabsUser.ready_to_clone == 1).first()
        if not elevenlabs_user: return False
        else: return True

# 将 voice_id 添加到 ElevenLabsUser 表中
def update_elevenlabs_user_voice_id(voice_id, from_id):
    with Session() as session:
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'voice_id': voice_id})
        session.commit()
    return voice_id


# 为 elevenlabs 添加新的 voice
def elevenlabs_add_voice(name, from_id, original_voice_filepath, elevenlabs_api_key):
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {
    "Accept": "application/json",
    "xi-api-key": elevenlabs_api_key
    }
    data = {
        'name': name,
        'labels': '{"accent": "American"}',
        'description': from_id
    }
    files = [
        ('files', (f'{original_voice_filepath}', open(f'{original_voice_filepath}', 'rb'), 'audio/mpeg'))
    ]

    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.text)
    voice_id = response.json().get('voice_id', None)
    if voice_id: return update_elevenlabs_user_voice_id(voice_id, from_id)


# r = elevenlabs_add_voice()
# print(json.dumps(r, indent=2))

def elevenlabs_update_voice(voice_id, voice_name, audio_file_path, user_eleven_labs_api_key):
    curl_command = (f"curl -X 'POST' "
                    f"'https://api.elevenlabs.io/v1/voices/{voice_id}/edit' "
                    f"-H 'accept: application/json' "
                    f"-H 'xi-api-key: {user_eleven_labs_api_key}' "
                    f"-H 'Content-Type: multipart/form-data' "
                    f"-F 'name={voice_name}' "
                    f"-F 'files=@{audio_file_path};type=audio/wav' "
                    f"-F 'labels='")

    # Execute the curl command
    process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode != 0: raise Exception(f"Curl command failed: {stderr.decode('utf-8')}")

    # Parse the JSON response
    response = json.loads(stdout.decode('utf-8'))
    return response
# r = elevenlabs_update_voice(voice_id, voice_name, audio_file_path)
# print(json.dumps(r, indent=2))

def get_elevenlabs_voices(user_eleven_labs_api_key):
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {
        'accept': 'application/json',
        'xi-api-key': user_eleven_labs_api_key
    }
    response = requests.get(url, headers=headers).json()
    # if debug: print(f"DEBUG: {response}")
    voices_dict = {}
    for voice in response['voices']:
        if voice['category'] == 'cloned':
            voices_dict[voice['name']] = voice['voice_id']
    # if debug: print(f"DEBUG: {voices_dict}")
    return voices_dict
'''
{
  "nanyang": "9ljiVpdb6qpxKPTng736",
  "chaochao": "CCgIdKx0m0QHHQUgFAVR",
  "anthony": "F6sIjTfa5MRpZTJiUrWH",
  "frankhu": "OE7bDvPK9rylQqr62NeZ",
  "vivianliu": "OX0yg3cTsrvlqUdlAbH5",
  "my_english_voice": "YEhWVRrlzrtA9MzdS8vE",
  "leowang_slow": "eXhbluainLzpz4zVbWr0",
  "yuchen": "h3TnXnm8yL5bQdjZsiWE"
}
'''
# r = get_elevenlabs_voices()
# print(json.dumps(r, indent=2))

'''
{
  "subscription": {
    "tier": "creator",
    "character_count": 18107,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
  },
  "is_new_user": true,
  "xi_api_key": "7506563f79bd85dbf7dade0cc8412b42",
  "can_use_delayed_payment_methods": false
}
'''

def eleven_labs_tts(content, from_id, tts_file_name, voice_id, user_eleven_labs_api_key):
    if debug: print(f"DEBUG: eleven_labs_tts() voice_id: {voice_id}")

    subscription_started = get_elevenlabs_userinfo(user_eleven_labs_api_key)
    '''
    {
    "tier": "creator",
    "character_count": 21501,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
    }
    '''

    words_remained = subscription_started['character_limit'] - subscription_started['character_count']
    len_content = len(content)
    can_extend_character_limit = subscription_started['can_extend_character_limit']
    if len_content > words_remained and not can_extend_character_limit: 
        out_range = f'''
你的 Eleven Labs 每月可以合成语音的总单词量是 {format_number(subscription_started['character_limit'])}, 你本月已经使用的单词总数是 {format_number(subscription_started['character_count'])}, 你本次提交的单词总数是 {format_number(len_content)}, 超过了你的剩余可用额度 {format_number(words_remained)}, 与此同时你目前没有开通'即用即付(allowed_to_extend_character_limit)' 的功能, 建议如下:

1) 减少本次生成的内容单词数到 {format_number(words_remained)} 以下;

2) 激活即用即付的功能 (超出每月限量之后, 每 1000 个单词 0.3美金, 仅限 22 美金/月 级更高级别用户才可以激活此功能)

具体的激活方法如下:
登录 https://beta.elevenlabs.io/subscription 找到 Enable usage based billing (surpass 100000 characters), 把它右边的按钮打开即可。
'''
        send_msg(out_range, from_id, parse_mode='', base_url=telegram_base_url)
        return 
    
    API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {"xi-api-key": user_eleven_labs_api_key}
    data = {
        "text": content,
        "voice_settings": {
            "stability": 0.95,
            "similarity_boost": 0.95
        }
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        with open(tts_file_name, "wb") as f: f.write(response.content)

        if os.path.isfile(tts_file_name): send_audio(tts_file_name, from_id, base_url=telegram_base_url)

        subscription_finished = get_elevenlabs_userinfo(user_eleven_labs_api_key)
        '''
        {
        "tier": "creator",
        "character_count": 22083,
        "character_limit": 100000,
        "can_extend_character_limit": true,
        "allowed_to_extend_character_limit": true,
        "next_character_count_reset_unix": 1680361833,
        "voice_limit": 30,
        "professional_voice_limit": 1,
        "can_extend_voice_limit": false,
        "can_use_instant_voice_cloning": true,
        "can_use_professional_voice_cloning": true,
        "currency": "usd",
        "status": "active"
        }
        '''

        words_used = subscription_finished['character_count'] - subscription_started['character_count']

        usd_cost = ((words_used - words_remained) / 1000) * 0.3 if words_used > words_remained and can_extend_character_limit else 0
        usd_cost = round(usd_cost, 2)
        send_msg(f"本次调用 Eleven Labs API 合成语音一共用量 {format_number(words_used)} 个单词, 实际消费 {usd_cost} usd, 本月剩余可用单词数 {format_number(subscription_finished['character_limit'] - subscription_finished['character_count'])}", from_id, parse_mode='', base_url=telegram_base_url)
        ''' response dir
        ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
        '''
        # 将 response 的 text , reason, json 内容打印出来, 尝试过很多次, 打不出来, 可能没有文字内容, 只有音频内容, 反正音频内容是正常的。
        # print(response.text)
        # print(response.reason)
        # print(response.json())

        return True

def generate_clone_voice_audio_with_eleven_labs(content, from_id, user_title, folder='files/audio/clone_voice'):
    
    elevenlabs_api_key, original_voice_filepath, voice_id, user_title_read = get_elevenlabs_api_key(from_id)
    if not elevenlabs_api_key: 
        send_msg(eleven_labs_no_apikey_alert, from_id, parse_mode='', base_url=telegram_base_url)
        return False
    if not original_voice_filepath: 
        send_msg(eleven_labs_no_original_voice_alert, from_id, parse_mode='', base_url=telegram_base_url)
        return False
    if not user_title_read or user_title_read != user_title: update_elevenlabs_user_original_voice_filepath(original_voice_filepath, from_id, user_title)
    if not voice_id: 
        voice_id = elevenlabs_add_voice(name=user_title, from_id=from_id, original_voice_filepath=original_voice_filepath, elevenlabs_api_key=elevenlabs_api_key)
        if not voice_id: 
            subscription = get_elevenlabs_userinfo(elevenlabs_api_key)
            if subscription:
                subscription_string = '\n'.join([f"{k}: {v}" for k, v in subscription.items()])
                failed_notice = f"Eleven Labs 订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
                eleven_labs_add_voice_failed_alert = f"{user_title}, 用你的克隆声音创建音频失败了, 😭😭😭...\n\n{failed_notice}"
                send_msg(eleven_labs_add_voice_failed_alert, from_id, parse_mode='', base_url=telegram_base_url)
                # 发送错误信息以及相关参数给 BOTCREATER_CHAT_ID
                send_msg(f"ERROR: elevenlabs_add_voice() failed: \n\n@{user_title}\n/{from_id}\n{failed_notice}", BOTCREATER_CHAT_ID)
                return False

    user_folder = f"{folder}/{from_id}"
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    new_file_name = f"{from_id}_{user_title}_{hashed_content[-7:]}.mp3"
    tts_file_name = f"{user_folder}/{new_file_name}.mp3"
    if os.path.isfile(tts_file_name): 
        send_audio(tts_file_name, from_id, base_url=telegram_base_url)
        return True

    send_msg(f"正在用你的声音克隆语音哈, 请稍等 1 分钟, 做好了马上发给你哦 😘", from_id, parse_mode='', base_url=telegram_base_url)
    r = eleven_labs_tts(content, from_id, tts_file_name, voice_id, elevenlabs_api_key)
    if r: return True
    else:
        send_msg(f"{eleven_labs_tts_failed_alert}\n如果你的账号正常, 请转发本消息给 @laogege6 帮忙诊断一下把。", from_id, parse_mode='', base_url=telegram_base_url)
        return False


if __name__ == '__main__':
    print(f"tvariables.py is running...")

    # if BOTOWNER_CHAT_ID == BOTCREATER_CHAT_ID:
        # try: 
        #     user_title = 'Laogege'
        #     coin = 'USDT'
        #     to_address = '0x3E711058491fB0723c6De9fD7E0c1b6635DE4A57'
        #     hash_tx = '0x109b661b1025c8a2a34c4633e283970608745c0f64d6dc0f0976fb92b18c234e'
        #     time_stamp = '2023-03-11T22:25:59.000Z'
        #     value = 20000
        #     r = insert_into_avatar_crypto_payments(BOTOWNER_CHAT_ID, coin, to_address, value, time_stamp, hash_tx, user_title)
        #     if r: 
        #         send_msg(f"叮咚, {user_title} {BOTOWNER_CHAT_ID} 刚刚充值 {format_number(value)} {coin.lower()}\n\n充值地址: \n{markdown_wallet_address(to_address)}\n\n交易哈希:\n{markdown_transaction_hash(hash_tx)}", BOTOWNER_CHAT_ID, parse_mode='Markdown')
        #         next_payment_time_dict = update_user_next_payment_date(BOTOWNER_CHAT_ID, user_title)
        #         send_msg(f"亲爱的, 你交来的公粮够我一阵子啦 😍😍😍, 下次交公粮的时间是: \n\n{next_payment_time_dict['next_payment_time']} \n\n你可别忘了哦, 反正到时候我会提醒你哒, 么么哒 😘", BOTOWNER_CHAT_ID)
        # except Exception as e: print(f"ERROR: insert_into_avatar_crypto_payments() failed: \n{e}")