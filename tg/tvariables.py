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

    MAX_CONVERSATION_PER_MONTH = int(MAX_CONVERSATION_PER_MONTH)

    # 查看当前目录并决定 TELEGRAM_BOT_RUNNING 的值
    TELEGRAM_BOT_RUNNING = BOT_TOKEN
    TELEGRAM_BOT_NAME = BOT_USERNAME
    BOT_OWNER_LIST = [BOTOWNER_CHAT_ID, BOTCREATER_CHAT_ID]

    openai.api_key = OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    ELEVENLABS_API = os.getenv("ELEVEN_API_KEY")
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
    STABILITY_URL = f"https://api.stability.ai/v1/"

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
    if debug: print(f"DEBUG: detect_english()")
    result = chardet.detect(text.encode())
    encoding = result['encoding']
    if encoding == 'ascii': return True
    lang = detect(text)
    if lang == 'en': return True

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

def chat_gpt_full(prompt, system_prompt='', user_prompt='', assistant_prompt='', dynamic_model='', chatgpt_key=''):
    if not prompt:
        return

    if not dynamic_model:
        dynamic_model = "gpt-3.5-turbo"
    if not system_prompt:
        system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work."
    if not user_prompt:
        user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt:
        assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."
    if not chatgpt_key:
        chatgpt_key = OPENAI_API_KEY

    if debug:
        print(f"DEBUG: chat_gpt() prompt length: {len(prompt.split())}")

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
    if not chat_id: return print(f"DEBUG: no chat_id, noly print:\n\n{message}")
    if debug: print(f"DEBUG: send_msg() to {chat_id}, length: {len(message.split())}")

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
    return True

def send_audio(audio_path, chat_id, base_url=telegram_base_url):
    if not audio_path or not chat_id: return
    if debug: print(f"DEBUG: send_audio()")

    url = base_url + 'sendAudio'
    # send the audio message to the user
    try:
        with open(audio_path, 'rb') as audio_file:
            requests.post(url, data={'chat_id': chat_id}, files={'audio': audio_file})
    except Exception as e: print(f"ERROR : send_audio() failed : {e}")
    return

def send_img(chat_id, file_path, description='', base_url=telegram_base_url):
    if not file_path or not chat_id: return
    method = "sendPhoto?"
    try: files = {'photo': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_img() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = base_url + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR : send_img() failed : \n{e}")
    return r

def send_file(chat_id, file_path, description='', base_url=telegram_base_url):
    if not file_path or not chat_id: return
    method = "sendDocument?"
    try: files = {'document': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_file() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = base_url + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR : send_file() failed : \n{e}")
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

def chat_gpt_english(prompt):
    if not prompt: return

    try:
        if debug: print(f"DEBUG: {OPENAI_MODEL} Amy the English teacher is working length: {len(prompt.split())}...")
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": english_system_prompt},
                {"role": "user", "content": english_user_prompt},
                {"role": "assistant", "content": english_assistant_prompt},
                {"role": "user", "content": 'Vector database technology has continued to improve, offering better performance and more personalized user experiences for customers.'},
                {"role": "assistant", "content": '/英译中:\n矢量数据库技术一直在不断改进，为客户提供更佳的性能和更个性化的用户体验。'},
                {"role": "user", "content": '''To address the challenges of digital intelligance in digital economy, artificial intelligence generate content (AIGC) has emerge. AIGC use artificial intalligence to assist or replace manual content generation by generating content based on userinputted keywords or requirements. '''},
                {"role": "assistant", "content": '''
英译中:
为了应对数字经济中的数字智能挑战，人工智能生成内容（AIGC）已经涌现。AIGC利用人工智能来辅助或取代人工内容生成，通过基于用户输入的关键词或需求来生成内容。

英文中的修改建议：
"digital intelligance" 应改为 "digital intelligence"
"intalligence" 应改为 "intelligence"
"userinputted" 应改为 "user-inputted"
"has emerge." 应改为 "has emerged"

修改后的英文句子：
To address the challenges of digital intelligence in the digital economy, artificial intelligence generated content (AIGC) has emerged. AIGC uses artificial intelligence to assist or replace manual content generation by generating content based on user-inputted keywords or requirements. '''},
                {"role": "user", "content": '''vector database'''},
                {"role": "assistant", "content": '''
Vector Database（矢量数据库）

释义:
矢量数据库是一种地理信息系统（GIS）数据库，用于存储、管理和查询地理空间数据中的矢量数据。矢量数据是由点、线和多边形组成的地理要素，用以表示现实世界中的地理位置、形状和属性。

相关信息:
与矢量数据库相对的是栅格数据库，栅格数据库用于存储栅格数据（像素化的数据），如遥感图像、数字高程模型等。矢量数据库更适用于表示具有清晰边界的地理特征，如道路、建筑物和行政区划，而栅格数据库适用于表示有连续变化的地理数据，如气候和植被等。'''},
                {"role": "user", "content": '''LLaMA'''},
                {"role": "assistant", "content": '''
LLaMA stands for "Large Language Model Assistant." It refers to an AI language model, like ChatGPT, which is designed to assist users with various tasks by generating human-like text based on the input provided. These large language models can be used for answering questions, providing explanations, generating content, and more.

LLaMA 是 "Large Language Model Assistant（大型语言模型助手）" 的缩写。它指的是像 ChatGPT 这样的人工智能语言模型，旨在通过根据提供的输入生成类似人类的文本来协助用户完成各种任务。这些大型语言模型可用于回答问题、提供解释、生成内容等。
'''},
                {"role": "user", "content": prompt},
                ]
            )
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()
        return reply
    
    except Exception as e: print(f"DEBUG: Amy the English teacher length: {len(prompt.split())} ERROR: \n\n{e}")
    
    return 

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


def get_transaction_hash_old(hash_tx, chain='eth'):
    function_url = "https://deep-index.moralis.io/api/v2/"
    method = "transaction/"
    url = function_url + method + hash_tx
    params = {"chain": chain}
    headers = {"accept": "application/json", "X-API-Key": MORALIS_API}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200: return r.json()
    else: return print(r.text)


import requests

def get_transaction_details(transaction_hash, chain='eth'):
    url = f'https://deep-index.moralis.io/api/v2/transaction/{transaction_hash}?chain={chain}'
    headers = {'accept': 'application/json', 'X-API-Key': MORALIS_API}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Request failed with status code: {response.status_code}')
        return None

'''return
{'block_hash': '0x76f7106dcecd0487db6c9179137671545faf6d8264853d5aeed3ab1f8a4b2883',
 'block_number': '15754667',
 'block_timestamp': '2022-10-15T16:19:11.000Z',
 'from_address': '0x5e278a70193f214c3536fd6f1d298a5eaef52795',
 'gas': '89000',
 'gas_price': '31000000000',
 'hash': '0x2f2aee699508938bcedda3a618bf753d1c7d54add00d8535c396d55faf6bf60f',
 'input': '0xa9059cbb000000000000000000000000376fa5c248eecb0110023efadd8317691b07ede10000000000000000000000000000000000000000000000000000000a8d949d40',
 'logs': [{'address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
           'block_hash': '0x76f7106dcecd0487db6c9179137671545faf6d8264853d5aeed3ab1f8a4b2883',
           'block_number': '15754667',
           'block_timestamp': '2022-10-15T16:19:11.000Z',
           'data': '0x0000000000000000000000000000000000000000000000000000000a8d949d40',
           'log_index': '66',
           'topic0': '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
           'topic1': '0x0000000000000000000000005e278a70193f214c3536fd6f1d298a5eaef52795',
           'topic2': '0x000000000000000000000000376fa5c248eecb0110023efadd8317691b07ede1',
           'topic3': None,
           'transaction_hash': '0x2f2aee699508938bcedda3a618bf753d1c7d54add00d8535c396d55faf6bf60f',
           'transaction_index': '43',
           'transaction_value': '0',
           'transfer_index': [15754667, 43, 66]}],
 'nonce': '10',
 'receipt_contract_address': None,
 'receipt_cumulative_gas_used': '2818433',
 'receipt_gas_used': '48537',
 'receipt_root': None,
 'receipt_status': '1',
 'to_address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
 'transaction_index': '43',
 'transfer_index': [15754667, 43],
 'value': '0'}'''


# 通过 hash_tx 查询转账信息
def get_transactions_info_by_hash_tx(hash_tx, chat_id, chain='eth'):
    hash_tx = str(hash_tx).lower()
    if not hash_tx.startswith('0x') and len(hash_tx) == 64: hash_tx = '0x' + hash_tx
    if len(hash_tx) != 66: return send_msg(f"输入的 hash_tx 长度不对, 请回复正确的 Transaction_Hash: 0x开头, 一共 66 位字符 😃", chat_id)
    trans_info = get_transaction_details(hash_tx, chain=chain)
    
    if debug: print(f"DEBUG: get_transaction_hash() 执行完毕, trans_info: \n\n{trans_info}")
    if not trans_info: return send_msg(f"抱歉, 无法查询到 {hash_tx} 的转账信息, 请检查输入是否正确.", chat_id)

    if not trans_info.get('input'): return send_msg(f"抱歉, 插到的信息有问题, 无法正确读取.", chat_id)
    if trans_info.get('value') != '0': return send_msg(f"抱歉, 这是一笔 ETH 转账, 不是 ERC20 代币转账.\n{hash_tx}", chat_id)
    token_address = trans_info.get('to_address')
    
    # 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息
    coin_list_df = get_token_info_from_db_cmc_total_supply(token_address)
    if coin_list_df.empty: return send_msg(f"抱歉, {token_address} 不在我的数据库里, 不清楚这是个什么币子, 无法查询. 😰", chat_id)
    token_address = coin_list_df.iloc[0]['token_address']
    imple_address = coin_list_df.iloc[0]['imple_address']
    coin = coin_list_df.iloc[0]['symbol']
    decimals = int(coin_list_df.iloc[0]['decimals'])
	
    if debug: print(f"DEBUG: get_token_info_from_db_cmc_total_supply() 执行完毕, token_address: {token_address}, coin: {coin}, decimals: {decimals}")

    # Dealing with erc20_symbol and ABI
    ABI = get_token_abi(imple_address)
    contract = web3.eth.contract(token_address, abi=ABI)
    from_address = trans_info['from_address']
    from_address = web3.to_checksum_address(from_address)
    from_addr_balance_wei = contract.functions.balanceOf(from_address).call()
    from_addr_balance = float(from_addr_balance_wei / 10 ** decimals)
    func_obj, func_params = contract.decode_function_input(trans_info.get('input'))
    '''return : {'to': '0x376FA5C248EECB0110023efADD8317691B07EDe1', 'value': 56195000000}'''
    # df = pd.read_sql_query(f"SELECT * FROM db_token_symbol_and_price WHERE coin='ETH'", engine)
    # eth_price = float(df.iloc[0]['price']) if not df.empty else gp('ETH').get('price')
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
            df_taged_address = pd.read_sql_query(f"SELECT address, tag FROM db_address_tag_record", engine)
            from_address_tag = df_taged_address.loc[df_taged_address['address']==from_address.lower()]
            to_address_tag = df_taged_address.loc[df_taged_address['address']==to_address.lower()]
            r = {
                '转账通证': coin,
                '转账金额': format_number(func_params['value']),
                '发出地址': f"{from_address[:5]}...{from_address[-6:]}" if from_address_tag.empty else from_address_tag.iloc[0]['tag'],
                '目标地址': f"{to_address[:5]}...{to_address[-6:]}" if to_address_tag.empty else to_address_tag.iloc[0]['tag'],
                '确认时间': ' '.join(str(trans_info['block_timestamp']).split('.')[0].split('T'))
                }
            # 用 '\n' join k: v from r
            r = '\n'.join([f"{k}: {v}" for k, v in r.items()])
            send_msg(r, chat_id)
        return func_params
    except Exception as e: print('DEBUG: get_transactions_info_by_hash_tx() error: ', e)
    return


if __name__ == '__main__':
    print(f"tvariables.py is running...")