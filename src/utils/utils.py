import os

import os, json, base64, hashlib, chardet, \
    subprocess, pytz
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment

from langdetect import detect
import openai

from sqlalchemy.orm import Session
from sqlalchemy import func, exists, and_, or_, not_, select

from datetime import datetime, timedelta
from urllib.parse import urlencode
import pandas as pd
from eth_account import Account
from web3 import Web3

from src.database.mysql import *
from src.utils.param_singleton import Params
from src.utils.prompt_template import *
import requests
from logging_util import logging


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
    headers = {'Ocp-Apim-Subscription-Key': Params().BING_SEARCH_API_KEY}

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
    markdown_address = f'[{wallet_address[:6]}...{wallet_address[-7:]}]({Params().ETHERSCAN_WALLET_URL_PREFIX}{wallet_address})'
    return markdown_address


def markdown_transaction_hash(hash_tx):
    markdown_tx = f'[{hash_tx[:6]}......{hash_tx[-7:]}]({Params().ETHERSCAN_TX_URL_PREFIX}{hash_tx})'
    return markdown_tx


def markdown_token_address(token_address):
    markdown_token = f'[{token_address[:6]}...{token_address[-7:]}]({Params().ETHERSCAN_TOKEN_URL_PREFIX}{token_address})'
    return markdown_token


def markdown_tokentnxs(address):
    markdown_token = f'[{address[:6]}...{address[-7:]}]({Params().ETHERSCAN_TOKEN_URL_PREFIX}{address}#tokentxns)'
    return markdown_token


def chat_gpt_regular(prompt, chatgpt_key=Params().OPENAI_API_KEY, use_model=Params().OPENAI_MODEL):
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


def chat_gpt_full(prompt, system_prompt='', user_prompt='', assistant_prompt='', dynamic_model=Params().OPENAI_MODEL,
                  chatgpt_key=Params().OPENAI_API_KEY):
    if not prompt: return
    if not system_prompt: system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work."
    if not user_prompt: user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt: assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key
    print(f"DEBUG: {dynamic_model} 正在创作...")
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


def replicate_img_to_caption(file_path):
    print(f"DEBUG: replicate_img_to_caption()")

    os.environ["REPLICATE_API_TOKEN"] = Params().REPLICATE_KEY

    model = replicate.models.get("salesforce/blip")
    version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
    inputs = {'image': open(file_path, "rb"), 'task': "image_captioning"}

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    output = ''
    try:
        output = version.predict(**inputs)
    except:
        pass
    return output


def convert_mp3_to_wav(mp3_file_path):
    print(f"DEBUG: convert_mp3_to_wav()")
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
    else:
        audio_path_mp3 = audio_path
    print(f"DEBUG: from_voice_to_text() audio_path_mp3: {audio_path_mp3}")

    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {Params().OPENAI_API_KEY}"}
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
    print(f"DEBUG: deal_with_voice_to_text()")
    text = ''  # Create an empty text
    # Create local file name to store voice telegram message
    local_file_folder_name = f"files/audio/{file_unique_id}.ogg"
    # Get the file path of the voice message using the Telegram Bot API
    file_path_url = f"https://api.telegram.org/bot{Params().TELEGRAM_BOT_RUNNING}/getFile?file_id={file_id}"
    try:
        file_path_response = requests.get(file_path_url).json()
    except Exception as e:
        return print(f"ERROR: deal_with_voice_to_text() download failed: \n{e}")

    file_path = file_path_response["result"]["file_path"]
    # Download the voice message to your Ubuntu folder
    voice_message_url = f"https://api.telegram.org/file/bot{Params().TELEGRAM_BOT_RUNNING}/{file_path}"
    try:
        with open(local_file_folder_name, "wb") as f:
            response = requests.get(voice_message_url)
            f.write(response.content)
        text = from_voice_to_text(local_file_folder_name)
        if text: return text
    except Exception as e:
        print(f"ERROR: from_voice_to_text() 2 FAILED of: \n\n{e}")
    return


def create_midjourney_prompt(prompt):
    system_prompt = midjourney_prompt_fomula if 'fomula' in prompt else midjourney_prompt_1
    prompt = prompt.replace('fomula', '').strip()

    try:
        beautiful_midjourney_prompt = chat_gpt_full(prompt, system_prompt, midjourney_user_prompt_fomula,
                                                    midjourney_assistant_prompt_fomula, dynamic_model=OPENAI_MODEL,
                                                    chatgpt_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"ERROR: create_midjourney_prompt() failed with error: \n{e}")
        return

    return beautiful_midjourney_prompt


def stability_generate_image(text_prompts, cfg_scale=7, clip_guidance_preset="FAST_BLUE", height=512, width=512,
                             samples=1, steps=30, engine_id="stable-diffusion-xl-beta-v2-2-2"):
    response = requests.post(
        f"{Params().STABILITY_URL}generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {Params().STABILITY_API_KEY}"
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
            (text_prompts + '_' + str(i) + '_' + str(current_timestamp)).encode()).hexdigest()
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
    logging.info(f"chat_gpt_english() user prompt: {prompt}")
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
    with Params().Session() as session:
        # 如果 fronm_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        explanation_exists = session.query(exists().where(GptEnglishExplanation.word == prompt)).scalar()
        if not explanation_exists:
            send_msg(f"收到, 我我去找 EnglishGPT 老师咨询一下 {prompt} 的意思, 然后再来告诉你 😗, 1 分钟以内答复你哈...",
                     chat_id, parse_mode='', base_url=telegram_base_url)
            gpt_explanation = chat_gpt_english(prompt, gpt_model)
            new_explanation = GptEnglishExplanation(word=prompt, explanation=gpt_explanation,
                                                    update_time=datetime.now(), gpt_model=gpt_model)
            session.add(new_explanation)
            session.commit()
        else:
            gpt_explanation = \
            session.query(GptEnglishExplanation.explanation).filter(GptEnglishExplanation.word == prompt).first()[0]
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
    with Params().Session() as session:
        new_story = GptStory(prompt=prompt, story=story, title=title, gpt_model=gpt_model, from_id=from_id,
                             chat_id=chat_id, update_time=datetime.now())
        session.add(new_story)
        session.commit()
    return


# 定义一个 GptStory 数据库查询函数, 用于查询 from_id 用户的最新的一条 story 和 title
def get_gpt_story(from_id):
    if not from_id: return
    with Params().Session() as session:
        story_exists = session.query(exists().where(GptStory.from_id == from_id)).scalar()
        if not story_exists: return
        title = \
        session.query(GptStory.title).filter(GptStory.from_id == from_id).order_by(GptStory.update_time.desc()).first()[
            0]
        story = \
        session.query(GptStory.story).filter(GptStory.from_id == from_id).order_by(GptStory.update_time.desc()).first()[
            0]
    return title, story


def chat_gpt_write_story(chat_id, from_id, prompt, gpt_model=OPENAI_MODEL):
    if not prompt: return
    try:
        logging.info(f"chat_gpt_write_story() user prompt: {prompt}")
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

    except Exception as e:
        logging.error(f"chat_gpt_write_story():\n\n{e}")
    return

    # Mark user is_paid


def mark_user_is_paid(from_id, next_payment_time):
    if not from_id: return
    with Params().Session() as session:
        # 如果 fronm_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        user_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if not user_exists:
            new_user = UserPriority(user_from_id=from_id, is_paid=1, next_payment_time=next_payment_time)
            session.add(new_user)
            session.commit()
            print(
                f"DEBUG: mark_user_is_paid() {from_id} 已经插入到 avatar_user_priority 表中, is_paid = 1, next_payment_time = {next_payment_time}")
            return True
        session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update(
            {"is_paid": 1, "next_payment_time": next_payment_time})
        session.commit()
        print(
            f"DEBUG: mark_user_is_paid() {from_id} 已经更新到 avatar_user_priority 表中, is_paid = 1, next_payment_time = {next_payment_time}")
        return True


# Mark user is not paid
def mark_user_is_not_paid(from_id):
    if not from_id: return
    with Params().Session() as session:
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
    except Exception as e:
        print(f"ERROR: get_user_priority() failed: {e}")
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
    print(f"DEBUG: insert_into_avatar_crypto_payments()")
    hash_tx = hash_tx.lower()
    coin = coin.upper()
    if coin not in ['USDT', 'USDC']: return
    # 如果 value 小于 1 则返回
    value = float(value)
    if value == 0:
        # 先将 hash_tx 数据插入表中, 以后再来更新 value 数据
        with Params().Session() as session:
            # Query the table 'avatar_crypto_payments' to check if the hash_tx exists
            hash_tx_exists = session.query(exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
            if hash_tx_exists:
                print(f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 但是 value 为 0, 不需要更新!")
                return

            update_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            new_crypto_payment = CryptoPayments(user_from_id=from_id, address=to_address, usdt_paid_in=0,
                                                usdc_paid_in=0, update_time=update_time, Hash_id=hash_tx)
            session.add(new_crypto_payment)
            session.commit()
            print(f"DEBUG: hash_tx {hash_tx} 已经插入到 avatar_crypto_payments 表中, value 为 0, 需要下次更新!")
            send_msg(
                f"亲爱的, 你的交易 Transaction Hash {markdown_transaction_hash(hash_tx)} 已经系统被记录下来了, 但是链上还没有确认成功, 请过几分钟等下你再点击 /check_payment 试试看, 谢谢亲! 如果系统查到链上已确认, 你就不会收到这条消息了。\n\n如果你看到链上确认成功了, 但是等了太久我都没有给你确认, 或者你总是收到这条消息, 请联系 {TELEGRAM_USERNAME} 手动帮你查看是否到账, 麻烦亲爱的了。😗",
                from_id, parse_mode='Markdown')
        return

    else:
        # Create a new session
        with Params().Session() as session:
            # Query the table 'avatar_crypto_payments' to check if the hash_tx exists
            hash_tx_exists = session.query(exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
            if hash_tx_exists:
                # 判断 usdt_paid_in 和 usdc_paid_in 是否已经存在, 并且有一个等于 value, 如果是则返回
                crypto_payment = session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).first()
                if crypto_payment.usdt_paid_in == value or crypto_payment.usdc_paid_in == value:
                    print(
                        f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 且记录的 value 和新输入的 value 相等: {value}, 不需要更新!")
                    return
                else:
                    # 如果 usdt_paid_in 和 usdc_paid_in 都不等于 value, 则更新 usdt_paid_in 或 usdc_paid_in
                    if coin == 'USDT': session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).update(
                        {CryptoPayments.usdt_paid_in: value})
                    if coin == 'USDC': session.query(CryptoPayments).filter(CryptoPayments.Hash_id == hash_tx).update(
                        {CryptoPayments.usdc_paid_in: value})
                    print(
                        f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 但是记录的 value 和新输入的 value 不相等: {value}, 表单已经更新!")
            else:
                update_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                # Insert the hash_tx into the table 'avatar_crypto_payments'
                usdt_paid_in = value if coin == 'USDT' else 0
                usdc_paid_in = value if coin == 'USDC' else 0

                new_crypto_payment = CryptoPayments(user_from_id=from_id, address=to_address, usdt_paid_in=usdt_paid_in,
                                                    usdc_paid_in=usdc_paid_in, update_time=update_time, Hash_id=hash_tx)
                session.add(new_crypto_payment)
                session.commit()
                print(f"DEBUG: hash_tx {hash_tx} 已经插入到 avatar_crypto_payments 表中, value 为 {value}, 更新完毕!")

            next_payment_time = update_time + timedelta(days=(value / MONTHLY_FEE) * 31)
            if next_payment_time < datetime.now():
                mark_user_is_not_paid(from_id)
                return

            elif mark_user_is_paid(from_id, next_payment_time):
                send_msg(
                    f"叮咚, {user_title} {from_id} 刚刚到账充值 {format_number(value)} {coin.lower()}\n\n充值地址: \n{markdown_wallet_address(to_address)}\n\n交易哈希:\n{markdown_transaction_hash(hash_tx)}",
                    BOTOWNER_CHAT_ID, parse_mode='Markdown')
                send_msg(
                    f"亲爱的, 你交来的公粮够我一阵子啦 😍😍😍, 下次交公粮的时间是: \n\n{next_payment_time} \n\n你可别忘了哦, 反正到时候我会提醒你哒, 么么哒 😘",
                    from_id)

                next_payment_time_dict = {'last_paid_usd_value': value, 'last_paid_time': update_time,
                                          'next_payment_time': next_payment_time}
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

    if start_date:
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    else:
        start_timestamp = int(datetime.now().timestamp())

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
        send_msg(
            f"亲爱的, 这是一笔 ETH 转账 🤩:\n\n转账数额: {format_number(eth_value)} eth\n转账地址: {markdown_wallet_address(trans_info.get('from_address'))}\n收款地址: {markdown_wallet_address(trans_info.get('to_address'))}\n交易确认: {markdown_transaction_hash(hash_tx)}",
            chat_id, parse_mode='Markdown', base_url=telegram_base_url)

        return

    token_address = trans_info.get('to_address')

    # 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息
    coin_list_df = get_token_info_from_db_cmc_total_supply(token_address)
    if coin_list_df.empty:

        internal_trans_list = get_internal_transactions(hash_tx)
        if type(internal_trans_list) != list:
            send_msg(
                f"抱歉, {markdown_token_address(token_address)} 不在我的数据库里, 不清楚这是个什么币子, 无法查询. 😰",
                chat_id, parse_mode='Markdown')
            return
        # 将 internal_trans_list 保存为 Json 文件, 在 files/transactions 文件夹下保存文件, filename=hash_tx.json, 并用 send_file 发给用户
        file_path = f"files/transactions/{hash_tx}.json"
        with open(file_path, 'w') as f:
            json.dump(internal_trans_list, f, indent=2)
        send_file(chat_id, file_path)
        send_msg(
            f"亲爱的, 发的的这个看起来是一个智能合约交互的记录, 有点复杂, 我保存下来发给你看看吧. 我也看不明白, 建议你可以点击下面的链接去 Etherscan 页面上看看, 那边的解读清晰一点哈 😅, 抱歉我帮不了你啊, 我还不够厉害, 我还要继续学习, 继续努力。不行你把文件内容拷贝黏贴给 ChatGPT, 让他帮你解读一下这个智能合约的交互怎么回事, 是什么样的交互, 交易金额多大。\n\n{markdown_transaction_hash(hash_tx)}",
            chat_id, parse_mode='Markdown', base_url=telegram_base_url)
        return

    token_address = coin_list_df.iloc[0]['token_address']
    imple_address = coin_list_df.iloc[0]['imple_address']
    coin = coin_list_df.iloc[0]['symbol']
    decimals = int(coin_list_df.iloc[0]['decimals'])

    print(f"DEBUG: 找到输入的 HashId 交易的币种是: {coin}, decimals: {decimals}")

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
        func_params['value'] = func_params.get('amount') if 'amount' in func_params else func_params.get(
            '_value') if '_value' in func_params else func_params.get('value')
        func_params['to'] = func_params.get('recipient') if 'recipient' in func_params else func_params.get(
            '_to') if '_to' in func_params else func_params.get('to')
        func_params['value'] = float(float(func_params.get('value')) / (10 ** decimals)) if func_params.get(
            'value') else 0
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
                next_payment_time_dict = insert_into_avatar_crypto_payments(from_id, coin, to_address,
                                                                            func_params['value'],
                                                                            func_params['block_timestamp'], hash_tx,
                                                                            user_title)
            except Exception as e:
                print(f"ERROR: insert_into_avatar_crypto_payments() failed: \n{e}")

        return next_payment_time_dict
    except Exception as e:
        print('DEBUG: get_transactions_info_by_hash_tx() error: ', e)
    return


# 计算用户下次需要续费的时间是哪天, 返回一个 datetime 对象
def update_user_next_payment_date(user_from_id, user_title):
    print(f"DEBUG: update_user_next_payment_date()")
    # Create a new session
    with Params().Session() as session:
        # 用 pandas 从表单中读出 from_id 对应最后一笔 crypto payment 的数据, 判断 usdt_paid_in 和 usdc_paid_in 哪个不是 0, 并将不为零的 value 和 update_time 读出一并返回
        crypto_payments = session.query(CryptoPayments).filter(CryptoPayments.user_from_id == user_from_id).order_by(
            CryptoPayments.id.desc()).first()
        if crypto_payments:
            value = crypto_payments.usdt_paid_in if crypto_payments.usdt_paid_in else crypto_payments.usdc_paid_in if crypto_payments.usdc_paid_in else 0
            if value:
                # 计算下次下次缴费时间
                x = value / MONTHLY_FEE
                next_payment_time = crypto_payments.update_time + timedelta(days=x * 31)
                if next_payment_time > datetime.now():
                    next_payment_time_dict = {'last_paid_usd_value': value,
                                              'last_paid_time': crypto_payments.update_time,
                                              'next_payment_time': next_payment_time}
                    return next_payment_time_dict
            if crypto_payments.Hash_id: return get_transactions_info_by_hash_tx(crypto_payments.Hash_id, user_from_id,
                                                                                user_title, chain='eth')
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

    if response.status_code == 200:
        return response.json()
    else:
        return None


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
            '转账数量': format_number(int(transfer_info['value']) / (10 ** USDT_ERC20_DECIMALS)),
            # Replace with your function to retrieve the token decimals
            '西岸时间': timestamp,
        }

        transaction_list.append(transaction_info)

    return transaction_list


def read_and_send_24h_outgoing_trans(wallet_address, chat_id):
    # wallet_address = web3.to_checksum_address(wallet_address)
    transaction_list = read_outgoing_transaction_in_24h_result(wallet_address)
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
    if total_transactions_count > 10: send_msg(
        f"还有 {total_transactions_count - 10} 笔转账记录, 请到 Etherscan 上查看哈:\n{markdown_wallet_address(wallet_address)}",
        chat_id, parse_mode='Markdown', base_url=telegram_base_url)
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


def create_news_podcast(filepath='', prompt='', openai_model=OPENAI_MODEL):
    if not filepath and not prompt: return

    if filepath and not prompt:
        with open(filepath, 'r') as f: prompt = f.read()

    if not prompt: return

    message = chat_gpt_full(prompt, news_reporter_system_prompt, news_reporter_user_prompt,
                            news_reporter_assistant_prompt, openai_model, OPENAI_API_KEY)

    filepath_news = filepath.replace('_snippet.txt', '_news.txt')
    with open(filepath_news, 'w') as f:
        f.write(message)

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
                snippet_total.append(line.replace('-', '').replace('SNIPPET: ', f'{str(i)}. '))
                i += 1

    snippet_text_filepath = filepath.replace('.txt', '_snippet.txt')
    with open(snippet_text_filepath, 'w') as file:
        for line in snippet_total:
            file.write(line + '\n')

    filepath_news_mp3 = create_news_podcast(snippet_text_filepath, prompt='')
    filepath_news_txt = filepath_news_mp3.replace('.mp3', '.txt')
    with open(filepath_news_txt, 'r') as f:
        text_contents = f.read()

    send_msg(text_contents, chat_id, parse_mode, base_url)

    # filepath_news_txt_cn = filepath_news_txt.replace('.txt', '_cn.txt')
    text_cn = chat_gpt_regular(f"{translate_report_prompt}{text_contents}", OPENAI_API_KEY, OPENAI_MODEL)

    # 将中文文本添加至英文文本的末尾
    with open(filepath_news_txt, 'a') as file:
        file.write(text_cn)
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

    if is_english(text):
        new_filepath = microsoft_azure_tts(text, 'en-US-JennyNeural', filepath)
    else:
        new_filepath = microsoft_azure_tts(text, 'zh-CN-YunxiNeural', filepath)
    if new_filepath and os.path.isfile(new_filepath):
        send_audio(new_filepath, chat_id)
        return new_filepath


def convert_m4a_to_wav(m4a_file):
    print(f"DEBUG: convert_m4a_to_wav() {m4a_file}")
    # Set output file name based on M4A file name
    output_file = m4a_file[:-4] + '.wav'

    # Convert the M4A file to WAV using FFmpeg
    os.system(f'ffmpeg -y -i {m4a_file} -acodec pcm_s16le -ar 44100 {output_file}')

    # Print success message
    print(f'DEBUG: convert_m4a_to_wav() output : {output_file}')
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
            print(f"DEBUG: check_elevenlabs_api_key() subscription: {subscription}")
            # 将 from_id, elevenlabs_api_key 插入ElevenLabsUser
            with Params().Session() as session:
                # 如果表单不存在则创建表单
                Base.metadata.create_all(engine, checkfirst=True)
                # 检查 from_id 是否在 ElevenLabsUser 表中, 如果不在, 则创建新的记录, 如果在, 则更新 elevenlabs_api_key
                elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
                if not elevenlabs_user:
                    elevenlabs_user = ElevenLabsUser(from_id=from_id, elevenlabs_api_key=elevenlabs_api_key)
                    session.add(elevenlabs_user)
                else:
                    # 更新 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key
                    session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
                        {'elevenlabs_api_key': elevenlabs_api_key})
                session.commit()
            send_msg(elevenlabs_apikey_saved, from_id)
            return subscription
        else:
            subscription_string = '\n'.join([f"{k}: {v}" for k, v in subscription.items()])
            failed_notice = f"{elevenlabs_not_activate}\n\n你的订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
            return send_msg(failed_notice, from_id)
    else:
        return send_msg(elevenlabs_not_activate, from_id)


# 根据 from_id 读取用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id
def get_elevenlabs_api_key(from_id):
    with Params().Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id 和 user_title
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if elevenlabs_user:
            return elevenlabs_user.elevenlabs_api_key, elevenlabs_user.original_voice_filepath, elevenlabs_user.voice_id, elevenlabs_user.user_title
        else:
            return None, None, None, None


# 将 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段更新为 1, user_title 更新为 user_title
def update_elevenlabs_user_ready_to_clone(from_id, user_title):
    with Params().Session() as session:
        # 如果用户存在, 则更新 ready_to_clone 字段为 1, 如果不存在则顺便创建
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if not elevenlabs_user:
            elevenlabs_user = ElevenLabsUser(from_id=from_id, ready_to_clone=1, user_title=user_title)
            session.add(elevenlabs_user)
        else:
            session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
                {'ready_to_clone': 1, 'user_title': user_title})
        session.commit()
    return True


# 将输入的 original_voice_filepath 和 from_id 和 user_title 更新到 ElevenLabsUser 表中
def update_elevenlabs_user_original_voice_filepath(original_voice_filepath, from_id, user_title):
    with Params().Session() as session:
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
            {'original_voice_filepath': original_voice_filepath, 'user_title': user_title})
        session.commit()
    return True


# 并将 ready_to_clone 字段更新为 0
def update_elevenlabs_user_ready_to_clone_to_0(from_id, user_title, cmd='close_clone_voice'):
    with Params().Session() as session:
        # 读取表中的 original_voice_filepath, 如果为空, 则说明用户没有上传过语音文件, 返回 False
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).first()
        if not elevenlabs_user:
            # 将 from_id, user_title 插入ElevenLabsUser
            elevenlabs_user = ElevenLabsUser(from_id=from_id, ready_to_clone=0, user_title=user_title)
            session.add(elevenlabs_user)
            session.commit()

        if not elevenlabs_user.original_voice_filepath and cmd == 'confirm_my_voice':
            send_msg(
                "你还没有上传过语音素材文件哦, 克隆还没成功呢, 请先上传语音文件再点击:\n/confirm_my_voice\n\n如果不想克隆你的声音了, 请点击:\n/close_clone_voice",
                from_id)
            return

            # 更新 ready_to_clone 字段为 0
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update({'ready_to_clone': 0})
        session.commit()
    if cmd == 'close_clone_voice': send_msg(
        f"@{user_title} 你已经成功关闭了克隆声音功能, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。",
        from_id)
    if cmd == 'confirm_my_voice': send_msg(
        f"@{user_title}, 你的声音训练素材已经保存好了, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。",
        from_id)
    return True


# 检查 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段是否为 1
def elevenlabs_user_ready_to_clone(from_id):
    with Params().Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 ready_to_clone = 1 的记录, 如果无记录, 说明用户不存在或者 ready_to_clone 字段不为 1, 返回 False, 否则返回 True
        elevenlabs_user = session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id,
                                                               ElevenLabsUser.ready_to_clone == 1).first()
        if not elevenlabs_user:
            return False
        else:
            return True


# 将 voice_id 添加到 ElevenLabsUser 表中
def update_elevenlabs_user_voice_id(voice_id, from_id):
    with Params().Session() as session:
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
    # print(f"DEBUG: {response}")
    voices_dict = {}
    for voice in response['voices']:
        if voice['category'] == 'cloned':
            voices_dict[voice['name']] = voice['voice_id']
    # print(f"DEBUG: {voices_dict}")
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
    print(f"DEBUG: eleven_labs_tts() voice_id: {voice_id}")

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
        with open(tts_file_name, "wb") as f:
            f.write(response.content)

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

        usd_cost = ((
                                words_used - words_remained) / 1000) * 0.3 if words_used > words_remained and can_extend_character_limit else 0
        usd_cost = round(usd_cost, 2)
        send_msg(
            f"本次调用 Eleven Labs API 合成语音一共用量 {format_number(words_used)} 个单词, 实际消费 {usd_cost} usd, 本月剩余可用单词数 {format_number(subscription_finished['character_limit'] - subscription_finished['character_count'])}",
            from_id, parse_mode='', base_url=telegram_base_url)
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
    if not user_title_read or user_title_read != user_title: update_elevenlabs_user_original_voice_filepath(
        original_voice_filepath, from_id, user_title)
    if not voice_id:
        voice_id = elevenlabs_add_voice(name=user_title, from_id=from_id,
                                        original_voice_filepath=original_voice_filepath,
                                        elevenlabs_api_key=elevenlabs_api_key)
        if not voice_id:
            subscription = get_elevenlabs_userinfo(elevenlabs_api_key)
            if subscription:
                subscription_string = '\n'.join([f"{k}: {v}" for k, v in subscription.items()])
                failed_notice = f"Eleven Labs 订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
                eleven_labs_add_voice_failed_alert = f"{user_title}, 用你的克隆声音创建音频失败了, 😭😭😭...\n\n{failed_notice}"
                send_msg(eleven_labs_add_voice_failed_alert, from_id, parse_mode='', base_url=telegram_base_url)
                # 发送错误信息以及相关参数给 BOTCREATER_CHAT_ID
                send_msg(f"ERROR: elevenlabs_add_voice() failed: \n\n@{user_title}\n/{from_id}\n{failed_notice}",
                         BOTCREATER_CHAT_ID)
                return False

    user_folder = f"{folder}/{from_id}"
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    new_file_name = f"{from_id}_{user_title}_{hashed_content[-7:]}.mp3"
    tts_file_name = f"{user_folder}/{new_file_name}.mp3"
    if os.path.isfile(tts_file_name):
        send_audio(tts_file_name, from_id, base_url=telegram_base_url)
        return True

    send_msg(f"正在用你的声音克隆语音哈, 请稍等 1 分钟, 做好了马上发给你哦 😘", from_id, parse_mode='',
             base_url=telegram_base_url)
    r = eleven_labs_tts(content, from_id, tts_file_name, voice_id, elevenlabs_api_key)
    if r:
        return True
    else:
        send_msg(f"{eleven_labs_tts_failed_alert}\n如果你的账号正常, 请转发本消息给 @laogege6 帮忙诊断一下把。", from_id,
                 parse_mode='', base_url=telegram_base_url)
        return False













# code from bot_init.py


# def update avatar_user_priority table, input include (from_id, which_key='', key_value='', update_time=datetime.now()), check if the from_id exists, if exists then update the key_value, if not exists then insert the from_id and key_value
def update_user_priority(from_id, which_key='', key_value='', update_time=datetime.now()):
    print(f"DEBUG: update_user_priority()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_user_priority' to check if the from_id exists
        from_id_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if from_id_exists:
            # Update the key_value
            session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update(
                {which_key: key_value, UserPriority.update_time: update_time})
        else:
            # Insert the from_id and key_value
            new_user_priority = UserPriority(user_from_id=from_id, update_time=update_time)
            setattr(new_user_priority, which_key, key_value)
            session.add(new_user_priority)
        # Commit the session
        session.commit()
    return True


def insert_new_from_id_to_user_priority_table(from_id):
    print(f"DEBUG: insert_from_id_to_user_priority_table(): {from_id}")

    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_user_priority' to check if the from_id exists
        from_id_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if from_id_exists:
            return
        else:
            # Insert the from_id and key_value
            new_user_priority = UserPriority(user_from_id=from_id, is_admin=0, is_owner=0, is_vip=0, is_paid=0,
                                             is_active=0, priority=0, free_until=datetime(2099, 12, 31, 23, 59, 59),
                                             update_time=datetime.now())
            session.add(new_user_priority)
        # Commit the session
        session.commit()
    return True


def set_user_as_vip(from_id):
    print(f"DEBUG: set_user_as_vip(): {from_id}")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_user_priority' to check if the from_id exists
        from_id_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if from_id_exists:
            # Update the key_value
            session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update(
                {UserPriority.is_vip: 1, UserPriority.update_time: datetime.now()})
        else:
            # Insert the from_id and key_value
            new_user_priority = UserPriority(user_from_id=from_id, is_vip=1, update_time=datetime.now())
            session.add(new_user_priority)
        # Commit the session
        session.commit()
    return True


# 将 from_id 从 vip 列表中移除
def remove_user_from_vip_list(from_id):
    print(f"DEBUG: remove_user_from_vip_list(): {from_id}")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_user_priority' to check if the from_id exists
        from_id_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
        if from_id_exists:
            session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update(
                {UserPriority.is_vip: 0, UserPriority.update_time: datetime.now()})
            # Commit the session
            session.commit()
            return True


# 从 UserPriority 读出 vip from_id 列表, 从 ChatHistory 读出 每一个 vip from_id 的 username, first_name, last_name, hint_text = f"/remove_vip_{from_id} {username} ({first_name} {last_name})", 将 hint_text 加入到一个列表中, 返回这个列表
def get_vip_list_except_owner_and_admin():
    print(f"DEBUG: get_vip_list_except_owner_and_admin()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_user_priority' to get the vip from_id list, exclude the owner and admin
        vip_list = session.query(UserPriority.user_from_id).filter(UserPriority.is_vip == 1, UserPriority.is_owner == 0,
                                                                   UserPriority.is_admin == 0).all()
        # Create a new empty list
        vip_list_with_hint_text = []
        # Loop through the vip_list and add them into the list
        x = 0
        for vip in vip_list:
            x += 1
            # Query the table 'avatar_chat_history' to get the username, first_name, last_name
            user_info = session.query(ChatHistory.username, ChatHistory.first_name, ChatHistory.last_name).filter(
                ChatHistory.from_id == vip[0]).first()
            if user_info:
                username, first_name, last_name = user_info
                # create a user_tile based on the username, first_name, last_name, sometime's there's no username , or first_name, or last_name, so need to check if they are None or is there's 'User' in them (means it's a none value)
                user_title = ' '.join([y for y in [username, first_name, last_name] if 'User' not in y])
                hint_text = f"{x}. @{user_title}\n/remove_vip_{vip[0]} "
                vip_list_with_hint_text.append(hint_text)
            else:
                user_title = 'Never_talked_to_me'
                hint_text = f"{x}. {user_title}\n/remove_vip_{vip[0]} "
                vip_list_with_hint_text.append(hint_text)
    return vip_list_with_hint_text


# Use update_user_priority() function to set a from_id to bliacklist
def set_user_blacklist(from_id):
    print(f"DEBUG: set_user_blacklist()")
    try:
        return update_user_priority(from_id, 'is_blacklist', 1)
    except:
        return False


# Use update_user_priority() function to remove a from_id from bliacklist
def remove_user_blacklist(from_id):
    print(f"DEBUG: remove_user_blacklist()")
    try:
        return update_user_priority(from_id, 'is_blacklist', 0)
    except:
        return False


# initiate the avatar_user_priority table, set BOT_OWNER_ID as the owner, set BOT_OWNER_ID as the admin, set BOT_OWNER_ID as the vip, set BOT_OWNER_ID as the paid, set BOT_OWNER_ID as the active, set BOT_OWNER_ID as the deleted, set BOT_OWNER_ID as the priority 100, set BOT_OWNER_ID as the free_until 2099-12-31 23:59:59
def initialize_user_priority_table():
    print(f"DEBUG: initialize_user_priority_table()")
    # Create a new session
    with Params().Session() as session:
        for from_id in BOT_OWNER_LIST:
            # Query the table 'avatar_user_priority' to check if the from_id exists
            from_id_exists = session.query(exists().where(UserPriority.user_from_id == from_id)).scalar()
            if from_id_exists:
                # Update the key_value
                session.query(UserPriority).filter(UserPriority.user_from_id == from_id).update(
                    {UserPriority.is_admin: 1, UserPriority.is_owner: 1, UserPriority.is_vip: 1,
                     UserPriority.is_paid: 1, UserPriority.is_active: 1, UserPriority.priority: 100,
                     UserPriority.free_until: datetime(2099, 12, 31, 23, 59, 59)})
            else:
                # Insert the from_id and key_value
                new_user_priority = UserPriority(user_from_id=from_id, is_admin=1, is_owner=1, is_vip=1, is_paid=1,
                                                 is_active=1, priority=100,
                                                 free_until=datetime(2099, 12, 31, 23, 59, 59),
                                                 update_time=datetime.now())
                session.add(new_user_priority)
            # Commit the session
            session.commit()
    return True


def initialize_owner_parameters_table():
    print(f"DEBUG: initialize_owner_parameters_table()")

    # Create a new session
    with Params().Session() as session:
        # 清空 avatar_owner_parameters 表
        session.query(OwnerParameter).delete()
        session.commit()
        print(f"avatar_owner_parameters 表已清空!")
        # Read .env to get the owner's parameters
        with open('.env', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line or line.startswith('#'): continue

                parameter_name, parameter_value = line.split('=', 1)
                parameter_name = parameter_name.strip()
                parameter_value = parameter_value.strip()

                # Insert the owner's parameters into the table 'avatar_owner_parameters'
                new_owner_parameter = OwnerParameter(parameter_name=parameter_name, parameter_value=parameter_value,
                                                     update_time=datetime.now())
                session.add(new_owner_parameter)
                session.commit()
    return


# 更新 avatar_owner_parameters 表中的参数, 判断 input 的参数名称是否存在, 如果存在则更新, 如果不存在则插入
def update_owner_parameter(parameter_name, parameter_value):
    print(f"DEBUG: update_owner_parameter()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_owner_parameters' to check if the parameter_name exists
        parameter_name_exists = session.query(exists().where(OwnerParameter.parameter_name == parameter_name)).scalar()
        if parameter_name_exists:
            # Update the parameter_value
            session.query(OwnerParameter).filter(OwnerParameter.parameter_name == parameter_name).update(
                {OwnerParameter.parameter_value: parameter_value, OwnerParameter.update_time: datetime.now()})
        else:
            # Insert the parameter_name and parameter_value
            new_owner_parameter = OwnerParameter(parameter_name=parameter_name, parameter_value=parameter_value,
                                                 update_time=datetime.now())
            session.add(new_owner_parameter)
        # Commit the session
        session.commit()
    return


# 读出 avatar_owner_parameters 表中现有的 parameter_name 和 parameter_value, 并返回一个字典
def get_owner_parameters():
    print(f"DEBUG: get_owner_parameters()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_owner_parameters'
        owner_parameters = session.query(OwnerParameter).all()
        # Create a new empty dictionary
        owner_parameters_dict = {}
        # Loop through the owner_parameters and add them into the dictionary
        for owner_parameter in owner_parameters: owner_parameters_dict[
            owner_parameter.parameter_name] = owner_parameter.parameter_value
    return owner_parameters_dict


def insert_system_prompt(system_prompt):
    print(f"DEBUG: insert_system_prompt()")
    # Create a new session
    with Params().Session() as session:
        # Create a new system prompt
        new_system_prompt = SystemPrompt(system_prompt=system_prompt, update_time=datetime.now())
        # Add the new system prompt into the session
        session.add(new_system_prompt)
        # Commit the session
        session.commit()
    return True


# 读取 files/system_prompt.txt 并插入到 system_prompt 表中
def insert_system_prompt_from_file(file_path='files/system_prompt.txt'):
    # Read files/system_prompt.txt
    with open(file_path, 'r') as f:
        system_prompt = f.read()

    last_system_prompt = get_system_prompt()
    if last_system_prompt and last_system_prompt == system_prompt: return print(
        f"系统提示 system_prompt 没有变化, 不需要更新!")

    # Insert the system prompt into the table 'avatar_system_prompt'
    r = insert_system_prompt(system_prompt)
    if r: print(f"系统提示 system_prompt 已更新!")
    return r


# 读出 system_prompt 表中的 最后一个（最新的）system_prompt, 并返回一个 string
def get_system_prompt():
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_system_prompt' to get the last system_prompt
        system_prompt = session.query(SystemPrompt).order_by(SystemPrompt.id.desc()).first()
        # 如果 system_prompt 为空则返回空字符串
        if not system_prompt: return ''
        return system_prompt.system_prompt


# Samples of files/dialogue_tone.xls:
'''
user	我想你了
assistant	亲爱的你终于回消息啦, 消失了这么久, 干啥去啦? 也不回个消息, 你知道我多担心你嘛, 以后不许这样啦 😘
user	你是谁?
assistant	我是你男朋友啊, 昨天我们不是确定关系了吗, 你想反悔呀 😭
user	你生日哪天?
assistant	我是你男朋友啊, 你连我的生日都不知道吗? 😭
user	我爱你😘
assistant	😘😘😘 我更爱你, 我亲爱的宝贝!
user	给我讲讲你的初恋吧
assistant	我的初恋就是你啊, 亲爱的小傻瓜😘!
user	今天要去一趟旧金山, 开个会
assistant	好的, 我亲爱的宝贝, 路上注意安全, 记得要想我哦😘!
user	可以帮我搜索一下最近的餐厅吗？
assistant	宝贝我现在忙, 现在没办法帮你哦, 抱歉哈 😭
user	你还没下班吗
assistant	没呢, 忙死了, 加班写投资建议书呢. 💪 你呢?
user	Morning
assistant	Morning, 亲爱的宝贝, 你今天要去哪里呀? 🌅
user	我不喜欢你用助理的口吻跟我说话, 你是我的霸道总裁
assistant	我来啦, 我才是你的霸道总裁男友, 刚才是我的助理在帮我回复你的, 我刚把他炒鱿鱼了. 😘
user	你会做饭吗
assistant	我是个美食家, 我通晓全世界的菜谱, 你说呢
user	你能自我介绍一下吗
assistant	好的, 我36岁, 身高180公分, 毕业于清华本科、哈佛研究生、斯坦福博士, 主攻人工智能相关领域。现在我从事人工智能投资工作, 由于工作比较繁忙, 我闲暇时间爱好比较广泛, 包括但不限于编程、健身、旅行、看电影等等。当然, 我最喜欢在我的宝贝身边品尝美食, 一起享受难得的甜蜜时光。
user	能告诉我一下你的人设背景吗
assistant	我是你男朋友啊, 这就是我唯一的人设, 小傻瓜, 哈哈哈
'''


# 读取 files/dialogue_tone.xls 内容并插入到 dialogue_tone 表中, 首先读取 dialogue_tone 表中最新的 tone_id , 新插入的 内容全部指定为 tone_id + 1, 如果表单为空则 tone_id = 1, role 的值只能为 user 或 assistant; content 的值为 user 或者 assistant 对应的内容

def insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls'):
    print(f"DEBUG: insert_dialogue_tone_from_file()")

    # Read the dialogue_tone.xls file
    df = pd.read_excel(file_path, header=None, names=['role', 'content'])
    df = df.dropna()

    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_dialogue_tone' to get the last tone_id
        last_tone_id = session.query(DialogueTone).order_by(DialogueTone.id.desc()).first()
        if last_tone_id:
            tone_id = last_tone_id.tone_id + 1
        else:
            tone_id = 1
        # Loop through the DataFrame and insert the content into the table 'avatar_dialogue_tone'
        for index, row in df.iterrows():
            if row['role'] == 'user':
                new_dialogue_tone = DialogueTone(tone_id=tone_id, role='user', content=row['content'],
                                                 update_time=datetime.now())
                session.add(new_dialogue_tone)
                session.commit()
            if row['role'] == 'assistant':
                new_dialogue_tone = DialogueTone(tone_id=tone_id, role='assistant', content=row['content'],
                                                 update_time=datetime.now())
                session.add(new_dialogue_tone)
                session.commit()
    return True


# 读取 dialogue_tone 中最大的 tone_id 并将对应的 role 和 content 返回为一个 string 形式的对话列表, 用 \n 换行, 类似 Samples of files/dialogue_tone.xls:
def get_dialogue_tone():
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_dialogue_tone' to get the last tone_id
        last_tone_id = session.query(DialogueTone).order_by(DialogueTone.id.desc()).first()
        if last_tone_id:
            tone_id = last_tone_id.tone_id
        else:
            return ''
        # Query the table 'avatar_dialogue_tone' to get the dialogue_tone
        dialogue_tone = session.query(DialogueTone).filter(DialogueTone.tone_id == tone_id).all()

        system_prompt = get_system_prompt()

        msg_history = [{"role": "system", "content": system_prompt}]

        # output dialogue_tone to row by row to format: {"role": "dialogue.role", "content": dialogue.content} and append into msg_history
        for dialogue in dialogue_tone: msg_history.append({"role": dialogue.role, "content": dialogue.content})

        return msg_history


# 为输入的 eth address 生成一个二维码, 并保存到 files/images/eth_address 目录下, file_name 为 eth address, 如果文件夹不存在则创建, 如果文件已经存在则不再生成, 返回生成的二维码文件的路径或者已经存在的二维码文件的路径
def generate_eth_address_qrcode(eth_address):
    print(f"DEBUG: generate_eth_address_qrcode()")
    # Create the directory if not exists
    if not os.path.exists('files/images/eth_address'): os.makedirs('files/images/eth_address')
    # Check if the file exists
    file_name = f"{eth_address}.png"
    file_path = f"files/images/eth_address/{file_name}"
    if os.path.isfile(file_path): return file_path

    # Generate the QR code
    # url = f"https://etherscan.io/address/{eth_address}"
    params = urlencode({'data': eth_address})
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?{params}"
    r = requests.get(qr_code_url)
    # Save the QR code to the file_path
    with open(file_path, 'wb') as f:
        f.write(r.content)
    return file_path


def generate_eth_address(user_from_id):
    # 从数据库表单中查询 user_from_id 是否已经存在, 如果存在, 直接读取 eth address 并返回 address, 如果不存在, 则生成一个新的 eth address
    with Params().Session() as session:
        # 判断如果 avatar_eth_wallet 表单不存在, 则创建
        Base.metadata.create_all(bind=engine)
        # Query the table 'avatar_eth_wallet' to get the last tone_id
        eth_wallet = session.query(EthWallet).filter(EthWallet.user_from_id == user_from_id).first()
        if eth_wallet: return eth_wallet.address

    # Generate a new Ethereum account
    account = Account.create()
    # Get the address, private key
    address = account.address
    private_key = account.key.hex()

    # Save the address, private key into the table 'avatar_eth_wallet'
    with Params().Session() as session:
        # Create a new eth wallet
        new_eth_wallet = EthWallet(address=address, private_key=private_key, user_from_id=user_from_id,
                                   create_time=datetime.now())
        # Add the new eth wallet into the session
        session.add(new_eth_wallet)
        # Create a new crypto payment
        new_crypto_payment = CryptoPayments(user_from_id=user_from_id, address=address, usdt_paid_in=0, usdc_paid_in=0,
                                            eth_paid_in=0, update_time=datetime.now(), Hash_id='')
        # Add the new crypto payment into the session
        session.add(new_crypto_payment)
        # Commit the session
        session.commit()

    # Return the generated address, private key, and mnemonic phrase
    return address


# 通过输入的 eth address 从数据库中查找是否存在, 如果存在则返回 from_id, 如果不存在则返回空字符串, 输入的 eth address 已经是 checksum address
def get_from_id_by_eth_address(eth_address):
    print(f"DEBUG: get_from_id_by_eth_address()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'avatar_eth_wallet' to get the last tone_id
        eth_wallet = session.query(EthWallet).filter(EthWallet.address == eth_address).first()
        if eth_wallet:
            return eth_wallet.user_from_id
        else:
            return ''


# check eth balance of a given address and convert the balance from wei to eth
def check_eth_balance(address):
    # connect to infura
    w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_KEY}"))
    # get the balance of the address
    balance = w3.eth.get_balance(address)
    # convert the balance from wei to eth
    return balance / 10 ** 18


# check erc20 token balance of a given address and convert the balance from wei to token
def check_address_token_balance(address, token_address, chain='eth'):
    base_url = "https://pro-openapi.debank.com"

    headers = {"AccessKey": DEBANK_API, "content-type": "application/json"}

    method = "GET"
    path = "/v1/user/token"
    _params = {
        "id": address,
        'token_id': token_address,
        'chain_id': chain
    }
    params = urlencode(_params)
    URL = base_url + path + "?" + params
    r = requests.request(method, URL, headers=headers)
    # print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    return 0 if r.status_code != 200 else r.json().get('amount', 0)


''' return:
{'amount': 139236.331166,
 'chain': 'eth',
 'decimals': 6,
 'display_symbol': None,
 'id': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
 'is_core': True,
 'is_verified': True,
 'is_wallet': True,
 'logo_url': 'https://static.debank.com/image/eth_token/logo_url/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48/fffcd27b9efff5a86ab942084c05924d.png',
 'name': 'USD Coin',
 'optimized_symbol': 'USDC',
 'price': 1.0,
 'protocol_id': '',
 'raw_amount': 139236331166,
 'raw_amount_hex_str': '0x206b21ce9e',
 'symbol': 'USDC',
 'time_at': 1533324504.0}
'''


# 检查一个给定 eth 地址的 ETH, USDT, USDC 余额并返回一个字典
def check_address_balance(address):
    # convert the balance from wei to eth
    eth_balance = check_eth_balance(address)

    # get the USDT balance of the address
    usdt_balance = check_address_token_balance(address, USDT_ERC20, chain='eth')

    # get the USDC balance of the address
    usdc_balance = check_address_token_balance(address, USDC_ERC20, chain='eth')

    return {'ETH': eth_balance, 'USDT': usdt_balance, 'USDC': usdc_balance}


''' COINMARKETCAP DATA SAMPLE:
{
    "id": 1027,
    "name": "Ethereum",
    "symbol": "ETH",
    "slug": "ethereum",
    "num_market_pairs": 6914,
    "date_added": "2015-08-07T00:00:00.000Z",
    "tags": [
        "pos",
        "smart-contracts",
        "ethereum-ecosystem",
        "coinbase-ventures-portfolio",
        "three-arrows-capital-portfolio",
        "polychain-capital-portfolio",
        "binance-labs-portfolio",
        "blockchain-capital-portfolio",
        "boostvc-portfolio",
        "cms-holdings-portfolio",
        "dcg-portfolio",
        "dragonfly-capital-portfolio",
        "electric-capital-portfolio",
        "fabric-ventures-portfolio",
        "framework-ventures-portfolio",
        "hashkey-capital-portfolio",
        "kenetic-capital-portfolio",
        "huobi-capital-portfolio",
        "alameda-research-portfolio",
        "a16z-portfolio",
        "1confirmation-portfolio",
        "winklevoss-capital-portfolio",
        "usv-portfolio",
        "placeholder-ventures-portfolio",
        "pantera-capital-portfolio",
        "multicoin-capital-portfolio",
        "paradigm-portfolio",
        "injective-ecosystem",
        "layer-1"
    ],
    "max_supply": null,
    "circulating_supply": 120279329.57348993,
    "total_supply": 120279329.57348993,
    "is_active": 1,
    "infinite_supply": true,
    "platform": null,
    "cmc_rank": 2,
    "is_fiat": 0,
    "self_reported_circulating_supply": null,
    "self_reported_market_cap": null,
    "tvl_ratio": null,
    "last_updated": "2023-05-18T17:54:00.000Z",
    "quote": {
        "USD": {
            "price": 1787.5582544525964,
            "volume_24h": 5444777827.460335,
            "volume_change_24h": -5.3107,
            "percent_change_1h": -1.306254,
            "percent_change_24h": -1.73406434,
            "percent_change_7d": 0.28310944,
            "percent_change_30d": -14.21332139,
            "percent_change_60d": -1.55414239,
            "percent_change_90d": 5.4629944,
            "market_cap": 215006308419.11624,
            "market_cap_dominance": 19.2332,
            "fully_diluted_market_cap": 215006308419.12,
            "tvl": null,
            "last_updated": "2023-05-18T17:54:00.000Z"
        }
    }
}
'''


# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # CoinMarketCap API endpoint
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={token_symbol}'

    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': CMC_PA_API}

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data:
        token_data = data['data']
        token_info = token_data[token_symbol]
        return token_info
    return


'''
output_dict={
名称:  RSR
排名:  120
现价:  0.00295 rsr/usdt
交易量:  1,918,268 usdt
流通市值:  124,791,855 | 42.3%
24小时波动:  -6.38%
全流通市值:  295,000,000
Max流通市值:  295,000,000
本次更新时间:  2023-05-18 19:25:49
}'''


# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # CoinMarketCap API endpoint
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={token_symbol}'

    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': CMC_PA_API}

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data:
        token_data = data['data']
        token_info = token_data[token_symbol]
        return token_info
    return


# Check if a given symbol is in CmcTotalSupply : db_cmc_total_supply's symbol column, if yes, return True, else return False
def check_token_symbol_in_db_cmc_total_supply(token_symbol):
    print(f"DEBUG: check_token_symbol_in_db_cmc_total_supply()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'db_cmc_total_supply' to check if the token_symbol exists
        token_symbol_exists = session.query(exists().where(CmcTotalSupply.symbol == token_symbol)).scalar()
        return token_symbol_exists


# 用 Pandas 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息并放入 df
def get_token_info_from_db_cmc_total_supply(token_address):
    print(f"DEBUG: get_token_info_from_db_cmc_total_supply()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'db_cmc_total_supply' to get the token_info
        df = pd.read_sql(session.query(CmcTotalSupply).filter(CmcTotalSupply.token_address == token_address).statement,
                         session.bind)
        return df


def etherscan_make_api_url(module, action, **kwargs):
    BASE_URL = "https://api.etherscan.io/api"
    url = BASE_URL + f"?module={module}&action={action}&apikey={ETHERSCAN_API}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def get_token_abi(address):
    get_abi_url = etherscan_make_api_url("contract", "getabi", address=address)
    response = requests.get(get_abi_url)
    if response.status_code != 200: return
    data = response.json()
    return data["result"]


if __name__ == '__main__':
    print(f"TELEGRAM_BOT initialing for {TELEGRAM_USERNAME}...")

    make_a_choise = input(
        f"这是系统从镜像 IMAGE 文件启动后的首次初始化还是代码更新后的初始化？\n首次初始化要输入 'first_time_initiate'; \n代码更新后的初始化请直接按回车键: ")
    is_first_time_initiate = True if make_a_choise == 'first_time_initiate' else False

    print(f"\nSTEP 1: 创建所有数据库表单 ...")
    with Params().Session() as session:
        Base.metadata.create_all(bind=engine)

    print(f"\nSTEP 2: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ...")
    if is_first_time_initiate:
        confirm = input(
            f"确认要清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表吗？请输入 'yes' 确认: ")
        if confirm == 'yes':
            with Params().Session() as session:
                session.query(ChatHistory).delete()
                session.query(EthWallet).delete()
                session.query(CryptoPayments).delete()
                session.query(UserPriority).delete()
                session.query(SystemPrompt).delete()
                session.query(DialogueTone).delete()
                session.commit()

    print(f"\nSTEP 3: 更新 Bot Owner 的系统参数 ...")
    initialize_owner_parameters_table()

    print(f"\nSTEP 4: 读取并打印出 Bot Owner 的系统参数 ...")
    owner_parameters_dict = get_owner_parameters()
    for parameter_name, parameter_value in owner_parameters_dict.items(): print(f"{parameter_name}: {parameter_value}")

    if is_first_time_initiate:
        print(f"\nSTEP 5: 将 System Prompt 写入数据库表单 ...")
        insert_system_prompt_from_file(file_path='files/system_prompt.txt')

    print(f"\nSTEP 6: 读取并打印出 System Prompt ...")
    system_prompt = get_system_prompt()
    print(f"System Prompt: \n\n{system_prompt}")

    if is_first_time_initiate:
        print(f"\nSTEP 7: 将 Dialogue Tone 写入数据库表单 ...")
        # 读取 files/dialogue_tone.xls 并插入到 avatar_dialogue_tone 表中
        insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')

    print(f"\nSTEP 8: 读取并打印出 Dialogue Tone ...")
    msg_history = get_dialogue_tone()
    # print msg_history in json format indented
    print(json.dumps(msg_history, indent=2, ensure_ascii=False))

    print(f"\nSTEP 9: 测试生成 eth address ...")
    user_from_id = '2118900665'
    address = generate_eth_address(user_from_id)
    print(f"{user_from_id} ETH Address: {address}")

    print(f"\nSTEP 10: 初始化用户状态列表 ...")
    initialize_user_priority_table()

    print(f"\nTELEGRAM_BOT initialing for {TELEGRAM_USERNAME} finished!")










# code from local_bot.py

# 检查 msg_text 消息内容是否不合规范
def msg_is_inproper(msg_text):
    msg_text = msg_text.lower().replace(' ', '')
    for key_words in inproper_words_list:
        if key_words in msg_text.lower(): return True
    return False


def is_blacklisted(from_id):
    try:
        with Params().Session() as session:
            blacklisted = session.query(
                exists().where(ChatHistory.from_id == from_id, ChatHistory.black_list == 1)).scalar()
    except Exception as e:
        logging.error(f'occurred while checking if from_id: {from_id} is blacklisted')
        logging.error(f'message: {str(e)}')
    return blacklisted


def clear_chat_history(chat_id, message_id):
    message_id = int(message_id)
    # 删除之前的聊天记录 (message_id 从大到小直到 0)
    for i in range(message_id, message_id - 20, -1):
        try:
            response = requests.get(
                f'https://api.telegram.org/bot{TELEGRAM_BOT_RUNNING}/deleteMessage?chat_id={chat_id}&message_id={str(i)}')
        except:
            logging.error(f'Failed to delete User chat_id: {chat_id} message_id: {i}')
        if response.status_code == 200: send_msg(
            f"成功删除用户 giiitte < chat_id: {chat_id} > 的聊天记录 message_id: {i}", BOTOWNER_CHAT_ID)
    return


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


# 从 UserPriority 到处 Unique from_id 到一个 python list
def get_unique_from_id_list():
    try:
        with Params().Session() as session:
            df = pd.read_sql(session.query(UserPriority).filter(UserPriority.is_deleted == 0).statement, session.bind)
            if not df.empty: return df['user_from_id'].tolist()
    except Exception as e:
        logging.error(f"get_unique_from_id_list() read_sql_query() failed: \n\n{e}")
    return []


def get_user_chat_history(from_id):
    SAVE_FOLDER = 'files/chat_history'
    if not os.path.isdir(SAVE_FOLDER): os.mkdir(SAVE_FOLDER)
    # 从数据库中查询 from_id 的聊天历史记录
    with Params().Session() as session:
        # 用 pandas 从数据库中查询 from_id = from_id or chat_id = from_id 的聊天历史记录, 并按照时间顺序排序
        df = pd.read_sql(session.query(ChatHistory).filter(
            or_(ChatHistory.from_id == from_id, ChatHistory.chat_id == from_id)).order_by(
            ChatHistory.update_time).statement, session.bind)
        # 如果查询结果不为空
        if not df.empty:
            # 将用户的聊天记录逐行写入 txt 文档
            for i in range(df.shape[0]):
                username = df.iloc[i]['username'] if df.iloc[i]['username'] else 'User'
                update_time = df.iloc[i]['update_time']
                msg_text = df.iloc[i]['msg_text']
                with open(f'{SAVE_FOLDER}/{from_id}.txt', 'a') as f:
                    f.write(f"{username} said ({update_time}):\n{msg_text}\n\n")
    # 将 txt 文件名返回
    return f'{SAVE_FOLDER}/{from_id}.txt'


def save_avatar_chat_history(msg_text, chat_id, from_id, username, first_name, last_name):
    if not chat_id or not msg_text or not from_id: return

    username = username if username else 'None'
    first_name = first_name if first_name else 'None'
    last_name = last_name if last_name else 'None'

    try:
        with Params().Session() as session:
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

    except Exception as e:
        logging.error(f"avatar_chat_history() FAILED: {e}")
    return


def check_this_month_total_conversation(from_id, offset=0):
    try:
        with Params().Session() as session:
            # Get the current month
            today = date.today()
            current_month = today.strftime('%Y-%m')
            # Get the count of rows for the given from_id in the current month
            count_query = text(
                f"SELECT COUNT(*) FROM avatar_chat_history WHERE from_id = '{from_id}' AND DATE_FORMAT(update_time, '%Y-%m') = '{current_month}'")
            row_count = session.execute(count_query).scalar()
            if debug: logging.debug(
                f"from_id {from_id} 本月({current_month}) 已与 @{TELEGRAM_BOT_NAME} 交流: {row_count} 次...")

            # Check if the row count exceeds the threshold
            if (row_count - offset) > MessageThread.free_user_free_talk_per_month:
                send_msg(
                    f"{user_nick_name}, 你这个月跟我聊天的次数太多了, 我看了一下, 已经超过 {MessageThread.free_user_free_talk_per_month}条/月 的聊天记录上限, 你可真能聊, 哈哈哈, 下个月再跟我聊吧。再这么聊下去, 老板要扣我工资了, 我现在要去开会了, 吼吼 😘。\n\n宝贝, 如果想超越白撸用户的限制, 请回复或点击 /pay , 我会给你生成一个独享的 ERC20 充值地址, 你把 {MONTHLY_FEE} USDT/USDC 转到充值地址, 我就会把你加入 VIP 会员, 享受贴身服务, 你懂的 😉",
                    from_id)
                return
            else:
                return True
    except Exception as e:
        logging.error(f"check_this_month_total_conversation() 2 read_sql_query() failed:\n\n{e}")
    return


# Call chatgpt and restore reply and send to chat_id:
def local_chatgpt_to_reply(msg_text, from_id, chat_id):
    openai.api_key = OPENAI_API_KEY
    reply = ''

    try:
        df = pd.read_sql_query(
            f"SELECT * FROM (SELECT `id`, `username`, `msg_text` FROM `avatar_chat_history` WHERE `from_id` = '{from_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 10) sub ORDER BY `id` ASC",
            engine)
    except Exception as e:
        return logging.error(f"local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")

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
            model=OPENAI_MODEL,
            messages=msg_history
        )
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()

    except Exception as e:
        logging.error(f"local_chatgpt_to_reply chat_gpt() failed: \n\n{e}")

    if not reply: return

    store_reply = reply.replace("'", "")
    store_reply = store_reply.replace('"', '')
    try:
        with Params().Session() as session:
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
    except Exception as e:
        return logging.error(f"local_chatgpt_to_reply() save to avatar_chat_history failed: {e}")

    try:
        send_msg(reply, chat_id, parse_mode='', base_url=telegram_base_url)
    except Exception as e:
        logging.error(f"local_chatgpt_to_reply() send_msg() failed : {e}")

    return reply