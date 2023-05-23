import azure.cognitiveservices.speech as speechsdk
import os, json, requests, time, re, subprocess, string, hashlib, chardet, shutil
from dotenv import load_dotenv
from pydub import AudioSegment
from glob import glob
from datetime import datetime
import openai
import imaplib, email, smtplib
from email.mime.text import MIMEText
import replicate
from urllib.request import urlretrieve
import random
import chardet
from langdetect import detect
from unidecode import unidecode
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips


load_dotenv()
debug = True

if 'LOAD VARIABLES':
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

    GMAIL_PREANGELLEO = 'preangelleo@gmail.com'
    GMAIL_CHATGPT_ADDRESS = 'emailchatgptbot@gmail.com'
    GMAIL_CHATGPT_PASSWD = os.getenv("GMAIL_CHATGPT")

    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/"

    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
    YOUTUBE_API = os.getenv('YOUTUBE_API')

    BOTOWNER_CHAT_ID = os.getenv("BOTOWNER_CHAT_ID")

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
    # Load your API key from an environment variable or secret management service
    openai.api_key = OPENAI_API_KEY

if 'GMAIL SETUP':
    # 登录邮箱
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(GMAIL_CHATGPT_ADDRESS, GMAIL_CHATGPT_PASSWD)

    # 设置邮箱服务器信息
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = GMAIL_CHATGPT_ADDRESS
    smtp_password = GMAIL_CHATGPT_PASSWD

def is_english(text):
    result = chardet.detect(text.encode())
    encoding = result['encoding']
    if encoding == 'ascii': return True
    lang = detect(text)
    if lang == 'en': return True

def detect_language(text):
    if not text: return
    lang = detect(text)
    if lang in ['zh-cn', 'zh-tw']: return 'Chinese'
    else: return 'English'

def send_message(text='', chat_id=BOTOWNER_CHAT_ID):
    if not text: return
    if not chat_id: 
        print(f"DEBUG: send_message() NO_CHAT_ID print: {text}")
        return
    else:
        url = TELEGRAM_API_URL + "sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        return response

def retrieve_email():
    if debug: print("DEBUG: retrieve_email()")
    
    # 选择邮箱
    imap_server.select("INBOX")

    # 搜索未读邮件
    typ, data = imap_server.search(None, "UNSEEN")
    
    new_inbox = []
    if data:
        # 获取最新的未读邮件
        try:
            latest_email_id = data[0].split()[-1]
            typ, data = imap_server.fetch(latest_email_id, "(RFC822)")
            # 解析邮件
            msg = email.message_from_bytes(data[0][1])
            for part in msg.walk():
                # 如果该部分是文本内容
                if part.get_content_type() == "text/plain": new_inbox.append([msg["From"], msg["Subject"], part.get_payload(decode=True).decode('utf-8')])
        except: pass

    return new_inbox

def send_email(email_content, to_address, subject="Chatbot Reply"):
    # 创建邮件内容
    message = MIMEText(email_content)
    message["Subject"] = subject
    message["From"] = smtp_username
    message["To"] = to_address

    # 发送邮件
    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.starttls()
    smtp_client.login(smtp_username, smtp_password)
    smtp_client.sendmail(smtp_username, to_address, message.as_string())
    smtp_client.quit()
    return True

# Using openai whisper api to convert voice to text
def from_voice_to_text(audio_path):
    if not os.path.isfile(audio_path): 
        print(f"DEBUG: from_voice_to_text() NOT_AN_AUDIO_FILE: {audio_path}")
        return
    
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text


def recognize_from_audio_file(audio_file):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print(f"Recognizing speech from {audio_file}...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return 

def chat_gpt(prompt, use_model = "gpt-3.5-turbo", api_key = OPENAI_API_KEY):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    data = {
        "model": use_model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    reply = response.json()['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply

def chat_gpt_for_email(prompt, system_prompt = ''):
    if not prompt: return

    prompt_head = prompt.split('\n')[0]
    if 'THE END' in prompt:  prompt = prompt.split('THE END')[0]

    if debug: print(f"DEBUG: chat_gpt_for_email() prompt length: {len(prompt.split())}")

    dynamic_model = "gpt-4" if '4' in prompt_head else "gpt-3.5-turbo"
    if not system_prompt: system_prompt = "You are a helpful assistant. You help me to read and reply emails."

    response = openai.ChatCompletion.create(
    model = dynamic_model,
    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply

def chatgpt_retrieve_gmail(new_inbox):
    if not new_inbox: return
    if debug: print(f"DEBUG: chatgpt_retrieve_gmail() new_inbox length: {len(new_inbox)}")
    
    for email_content in new_inbox:
        # 获取邮件内容
        email_from, email_subject, email_body = email_content

        # 回复邮件
        reply = chat_gpt_for_email(email_body)
        send_email(reply, email_from, email_subject)

    return

def remove_punctuation(working_folder='/Users/lgg/Downloads'):
    if debug: print(f"DEBUG: remove_punctuation() 正在处理 {working_folder} 文件夹中的文件...")
    # Get a list of all files in the working folder
    file_list = os.listdir(working_folder)

    # Define the set of punctuation characters to remove
    punctuation_set = set(string.punctuation) - set(".")

    # Loop through all files in the working folder and remove punctuation
    for file_name in file_list:
        # Ignore subdirectories
        if not os.path.isfile(os.path.join(working_folder, file_name)):
            continue
        
        # Split the file name into base name and extension
        file_base, file_ext = os.path.splitext(file_name)
        
        # Remove punctuation from the file base name
        # file_base_new = "".join(char for char in file_base if char not in ['punctuation_set'])
        file_base_new = file_base.replace('？', '')
        
        # Rename the file if the file base name has changed
        if file_base != file_base_new:
            file_name_new = file_base_new + file_ext
            os.rename(os.path.join(working_folder, file_name), os.path.join(working_folder, file_name_new))
            
    if debug: print(f"DEBUG: remove_punctuation() 处理完成!")
    return True

def rename_target_file(filepath, target_filename='today_video'):
    if not os.path.isfile(filepath): return

    dirname, filename = os.path.split(filepath)

    new_filepath_list = []
    for extention in ['.mp4', '.srt', '.txt', '.wav', '.mp3', 'json']:
        old_filename = filename[:-4] + extention
        new_filename = target_filename + extention

        old_filepath = os.path.join(dirname, old_filename)
        if os.path.isfile(old_filepath): 
            new_filepath = os.path.join(dirname, new_filename)
            os.rename(old_filepath, new_filepath)
            new_filepath_list.append(new_filepath)
    
    return new_filepath_list

def get_latest_folder(folder_path):
    folders = glob(os.path.join(folder_path, "*/"))  # list all folders in the given directory
    latest_folder = max(folders, key=os.path.getmtime)  # get the folder with the latest modification time
    return latest_folder
    
def get_latest_file_in_folder(folder, extension):
    # Get a list of all files with the given extension in the folder
    files = glob(os.path.join(folder, f"*{extension}"))
    if not files: return False

    # Find the latest file by comparing modification times
    latest_file = max(files, key=os.path.getmtime)

    return latest_file

def read_lines(filepath):
    with open(filepath, 'r') as f:
        for line in f: yield line.strip()

def chat_gpt_full(prompt, system_prompt = '', user_prompt = '', assistant_prompt = '', dynamic_model = '', chatgpt_key = ''):
    if not prompt: return 
    
    if not dynamic_model: dynamic_model = "gpt-4" if '4' in prompt else "gpt-3.5-turbo"
    if not system_prompt: system_prompt = "read below top news snippets and generate a new report titled as What you need to know today or something better to catch attention, the repot content need sounds like CNN but cover all of the information in the text in a concise way:"
    if not user_prompt: user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt: assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."
    if not chatgpt_key: chatgpt_key = OPENAI_API_KEY

    if debug: print(f"DEBUG: chat_gpt_full() prompt length: {len(prompt.split())}")

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key
    
    response = openai.ChatCompletion.create(
    model = dynamic_model,
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

def chat_gpt_regular(prompt, use_model = 'gpt-3.5-turbo', chatgpt_key = OPENAI_API_KEY):
    if not prompt: return
    if debug: print(f"DEBUG: chat_gpt_regular() prompt: {prompt}")

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key
    
    response = openai.ChatCompletion.create(
    model = use_model,
    messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply

if __name__ == "__main__":
    if debug: print("DEBUG: my_config.py is running...")
    send_message(text='测试一下', chat_id=BOTOWNER_CHAT_ID)