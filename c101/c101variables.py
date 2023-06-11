# -*- coding: utf-8 -*-
# from my_config.my_variables import *
from prompt_template import *

place_holder = True

# 导入库
if place_holder:
    import base64
    import email
    import hashlib
    import hmac
    import imaplib
    import io
    import json
    import math
    import os
    import pyotp
    import pickle
    import random
    import re
    import ccxt
    import socket
    import string
    import struct
    import sys
    import time
    import urllib
    import uuid
    import threading
    import requests
    from collections import Counter
    from datetime import datetime
    from io import BytesIO
    from pathlib import Path
    from urllib.parse import urlencode
    from urllib.request import urlretrieve
    import boto3
    import chardet
    import openai
    import pandas as pd
    import pytz
    import streamlit as st
    import streamlit_authenticator as stauth
    import whisper
    import replicate
    import yaml
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    from gtts import gTTS
    from langdetect import detect
    from matplotlib import pyplot as plt
    from PIL import Image, ExifTags
    from requests import Session, get
    from sqlalchemy import DateTime, MetaData, Table, create_engine, insert, update, Column, Integer, String, Text, Float, text
    from sqlalchemy.orm import sessionmaker
    from yaml import SafeLoader
    import tempfile
    from web3 import Web3
    from ens import ENS
    from urllib.parse import urljoin
    import shutil
    from io import StringIO
    import pyheif
    from math import sqrt
    import subprocess
    import imghdr
    import imageio.v2 as iio
    import numpy as np
    import piexif
    import PyPDF2
    import azure.cognitiveservices.speech as speechsdk
    import imaplib
    import email
    import smtplib
    from email.mime.text import MIMEText
    from bs4 import BeautifulSoup
    import discord
    from discord.ext import commands
    from pydub import AudioSegment
    from twilio.rest import Client

    from langchain.memory import ConversationBufferWindowMemory
    from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
    from langchain.agents import Tool, load_tools
    from langchain.agents import AgentType
    from langchain.memory import ConversationBufferMemory
    from langchain.utilities import SerpAPIWrapper
    from langchain.agents import initialize_agent
    from langchain.schema import Document
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader, UnstructuredURLLoader
    from langchain.indexes import VectorstoreIndexCreator
    from langchain.document_loaders.csv_loader import CSVLoader
    from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
    from langchain.vectorstores import Chroma, Pinecone
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.chains.question_answering import load_qa_chain
    from langchain.chat_models import ChatOpenAI
    from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
    from langchain.utilities import WikipediaAPIWrapper

    import pinecone
    from abc import ABC, abstractmethod
    from typing import List

    load_dotenv()

# 获取变量参数
if place_holder:
    debug = True
    # Access environment variables
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    remote_db_password = os.getenv('REMOTE_DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    bot_token = os.getenv('BOT_TOKEN')
    bot_owner_chat_id = str(os.getenv('BOTOWNER_CHAT_ID'))
    bot_id = os.getenv('BOT_ID')
    woshi_laogege = str(os.getenv('WOSHI_LAOGEGE'))
    danli_yu = str(os.getenv('DANLI_YU'))
    bit_ly = os.getenv('BIT_LY')
    replicate_key = os.getenv('REPLICATE')
    eleven_api_key = os.getenv("ELEVEN_API_KEY")
    OPENAI_API_KEY_FREE = os.getenv("OPENAI_API_KEY_FREE")
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
    TWILIO_API = os.getenv("TWILIO_API")
    TWILIO_AUTH = os.getenv("TWILIO_AUTH")
    TELEGRAM_HOME_BOT = os.getenv("TELEGRAM_HOME_BOT")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

    FANBOOK_CLIENT_ID=os.getenv("FANBOOK_CLIENT_ID")
    FANBOOK_SECRET=os.getenv("FANBOOK_SECRET")
    FANBOOK_DICTIONARY_BOT=os.getenv("FANBOOK_DICTIONARY_BOT")

    openai_key = os.getenv('OPENAI_KEY')
    openai.api_key = openai_key

    notion_api = os.getenv('NOTION_INTEGRATION_API')
    My_daily_talks_with_ChatGPT = '9b0796a9-97a5-4b5b-8d20-e081530c962a'

    youdao_url = 'https://openapi.youdao.com/api'
    youdao_id = os.getenv('YOUDAO_ID')
    youdao_secret = os.getenv('YOUDAO_SECRET')

    infura_api = os.getenv('INFURA_API')
    infura_url = "https://mainnet.infura.io/v3/" + infura_api

    web3 = Web3(Web3.HTTPProvider(infura_url))
    ns = ENS.fromWeb3(web3)

    binance_api = os.getenv('BINANCE_LTD_API_KEY')
    binance_secret = os.getenv('BINANCE_LTD_API_SECRET')
    BINANCE_TICKER_URL = 'https://api.binance.com/api/v3/ticker/24hr'

    CMC_PA_API = 'bbac788f-ab81-41c8-88f5-bd930b14f886'

    BOTOWNER_CHAT_ID = bot_owner_chat_id

    ETH_REGEX = r'0x[a-fA-F0-9]{40}'
    TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
    EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    VERY_BIG_NUMBER = 1000000000000000000000000000000
    VERY_BIG_NUMBER_STR = str(VERY_BIG_NUMBER)

    BINANCE_DEPOSIT_ADDRESS_FOR_ERC20 = '0x34B940120AEB9cadbCc4131fB034aD3B83B0367d'

    ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
    ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
    ETH_ADDRESS_STD = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    MY_MAIN_ADDRESS = '0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'
    MY_DEX_TRADING_ADDRESS = '0x4Dfb418B2dd552cA085FAc5a64b1C4508dc2877F'

    ONE_INCH_ERC20_ADDRESS = '0x111111111117dC0aa78b770fA6A738034120C302'
    ONE_INCH_CONTRACT_ADDRESS = '0x1111111254fb6c44bAC0beD2854e76F90643097d'

    USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    USDT_ERC20_DECIMALS = 6

    DID_API_KEY = 'cHJlYW5nZWxsZW9AZ21haWwuY29t:bCUrfsif0HFikxmTUSZrz'
    IGNORE_POSITIONS = ['USDT', 'BNB', 'NFT']
    SPECIAL_CHARS = " .~!@#${%^&*()_+-*/<>},[]\/;?:'"
    ONE_DAY_SECONDS = 60 * 60 * 24
    SPLIT_LINE = '='*33
    

    # Telegram base URL
    base_url = "https://api.telegram.org/bot" + bot_token + "/"

    # Link to database
    db_engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', pool_pre_ping=True)
    conn = db_engine.connect()

    try:
        remote_db_engine = create_engine(
            f'mysql+pymysql://master:{remote_db_password}@8.209.210.222:3306/binance_ltd_main', pool_pre_ping=True)
        remote_conn = remote_db_engine.connect()
    except Exception as e:
        print(
            f"ERROR : connecting to remote mysql server failed because of: {e}")

    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')
    # os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY

    class BaseRetriever(ABC):
        @abstractmethod
        def get_relevant_documents(self, query: str) -> List[Document]:
            """Get texts relevant for a query.

            Args:
                query: string to find relevant texts for

            Returns:
                List of relevant documents
            """

    # initialize pinecone
    pinecone.init(
        api_key=os.getenv('PINECONE_FREE'),  # find at app.pinecone.io
        environment='us-west1-gcp-free'  # next to api key in console
    )

    os.environ["WOLFRAM_ALPHA_APPID"] = 'WA4937-6U5K7UXR74'
    wolfram = WolframAlphaAPIWrapper()
    wikipedia = WikipediaAPIWrapper()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=openai_key)

    # 创建一个新的表单 avatar_user_info, 包括 user_id (primary key, autoincrease; int), user_chinese_name (varchar 20), phone (varchar 20), openai_key (text), telegram_bot_key (text), telegram_bot_name (text), telegram_user_name (text),domain_name (text), email_address (text), server_ip_address (varchar 20), server_root_passwd (varchar 30), user_nick_name (varchar 20), user_website_passwd (varchar 30), system_prompt (text), user_full_name (varchar 30), user_chat_id (text), usdt_address_erc20 (text), first_payment_date (datetime), next_payment_date (datetime), notes (text)
    query = 'CREATE TABLE IF NOT EXISTS avatar_user_info (user_id INT AUTO_INCREMENT PRIMARY KEY, user_chinese_name VARCHAR(20), phone VARCHAR(20), openai_key TEXT, telegram_bot_key TEXT, telegram_bot_name TEXT, telegram_user_name TEXT, domain_name TEXT, email_address TEXT, server_ip_address VARCHAR(20), server_root_passwd VARCHAR(30), user_nick_name VARCHAR(20), user_website_passwd VARCHAR(30), system_prompt TEXT, user_full_name VARCHAR(30), user_chat_id TEXT, usdt_address_erc20 TEXT, first_payment_date DATETIME, next_payment_date DATETIME, notes TEXT)'
    conn.execute(query)


if 'GMAIL_SETUP':

    GMAIL_LAOGEGECODING_ADDRESS = 'laogegecoding@gmail.com'
    GMAIL_LAOGEGECODING_PASSWD = os.getenv("GMAIL_LAOGEGECODING")
    GMAIL_CHATGPT_ADDRESS = 'emailchatgptbot@gmail.com'
    GMAIL_CHATGPT_PASSWD = os.getenv("GMAIL_CHATGPT")

# insert new user_chinese_name to avatar_user_info


def send_sms(msg, to_number, from_number='+18555832670'):
    sms_client = Client(TWILIO_API, TWILIO_AUTH)
    respond = sms_client.messages.create(
        from_=from_number,
        body=msg,
        to=to_number
    )
    return respond.sid
    '''
    Response Headers: {'Date': 'Thu, 13 Apr 2023 19:21:46 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': '840', 'Connection': 'keep-alive', 'Twilio-Request-Id': 'RQee4e21a024ed477bf81e467375f1024d', 'Twilio-Request-Duration': '0.129', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Accept, Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Idempotency-Key', 'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS', 'Access-Control-Expose-Headers': 'ETag', 'Access-Control-Allow-Credentials': 'true', 'X-Powered-By': 'AT-5000', 'Twilio-Concurrent-Requests': '1', 'X-Shenanigans': 'none', 'X-Home-Region': 'us1', 'X-API-Domain': 'api.twilio.com', 'Strict-Transport-Security': 'max-age=31536000'}
    '''
    'SMee4e21a024ed477bf81e467375f1024d'


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

        folder = 'json_datas/bing_search'
        if not os.path.exists(folder):
            os.makedirs(folder)
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
        if os.path.isfile(file_path):
            os.remove(file_path)

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

# Function to decode Base64-encoded string to UTF-8


def decode_base64(text):
    decoded = base64.b64decode(text)
    try:
        result = decoded.decode('utf-8')
    except UnicodeDecodeError:
        result = decoded.decode('iso-8859-1')
    return result


def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8').strip()


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


def detect_language(text):
    if not text:
        return
    lang = detect(text)
    if lang in ['zh-cn', 'zh-tw']:
        return 'Chinese'
    else:
        return 'English'


def st_extract_words(text):
    if debug:
        print(f"DEBUG: st_extract_words()")
    words = re.split('[\.:\-\)]', text)
    extracted_words_list = []
    for word in words:
        if len(word.split()) == 1 and str(word).strip() not in ['1', '2', '3', '4', '5']:
            extracted_words_list.append(word.strip().lower())
        if len(word.split()) == 2 and word.split()[1].strip() in ['2', '3', '4', '5']:
            extracted_words_list.append(word.split()[0].strip().lower())
    return extracted_words_list


def st_remove_puctuations_and_duplicated_contents(original_string):
    # original_string = ' erratically erratically, fitfully. intermittently,, erratically unpredictably '
    punctuation = string.punctuation
    word_list = original_string.split()
    unique_word_list = []
    for word in word_list:
        stripped_word = word.strip(punctuation)
        if stripped_word and stripped_word.lower() != 'none':
            unique_word_list.append(stripped_word.lower())
    unique_word_list = list(set(unique_word_list))
    return unique_word_list


def show_all_tables(engine=remote_db_engine):
    conn = engine.connect()
    alist = conn.execute("SHOW TABLES")
    conn.close()
    df = pd.DataFrame(alist)
    return df['Tables_in_binance_ltd_main'].tolist()

# Database update or insert function


def update_or_insert_data(engine, table_name, filter_column, filter_value, update_column, update_value):
    if debug:
        print(f"DEBUG: update_or_insert_data()")
    connection = engine.connect()
    metadata = MetaData(bind=engine)
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)
    filter_column = table.columns[filter_column]
    update_column = table.columns[update_column]
    result = connection.execute(table.select().where(
        filter_column == filter_value)).first()
    if result:
        if str(update_column.type).startswith('INTEGER') or str(update_column.type).startswith('TINYINT'):
            connection.execute(table.update().where(
                filter_column == filter_value).values({update_column: int(update_value)}))
        elif str(update_column.type).startswith('VARCHAR') or str(update_column.type).startswith('TEXT'):
            connection.execute(table.update().where(
                filter_column == filter_value).values({update_column: str(update_value)}))
        elif str(update_column.type) == 'DATETIME':
            if isinstance(update_value, int):
                update_value = int(update_value)
            elif isinstance(update_value, float):
                update_value = float(update_value)
            elif isinstance(update_value, str):
                update_value = update_value
            elif isinstance(update_value, datetime):
                update_value = update_value.strftime('%Y-%m-%d %H:%M:%S')
            connection.execute(table.update().where(
                filter_column == filter_value).values({update_column: str(update_value)}))
        else:
            connection.close()
            return
        connection.close()
        return True
    else:
        insert_stmt = insert(table).values(
            {filter_column: filter_value, update_column: update_value})
        connection.execute(insert_stmt)
        connection.close()
        return True

# Sending message from telegram bot


def send_msg(message, chat_id, parse_mode='', base_url=base_url):
    if not message: return
    if not chat_id: return print(message)
    if debug: print(f"DEBUG: send_msg() length: {len(message.split())}")
    
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


def send_audio(audio_path, chat_id, base_url=base_url):
    if not audio_path: return
    if debug: print(f"DEBUG: send_audio()")
    url = base_url + 'sendAudio'
    # send the audio message to the user
    try:
        with open(audio_path, 'rb') as audio_file:
            requests.post(url, data={'chat_id': chat_id}, files={'audio': audio_file})
    except Exception as e: print(f"ERROR : send_audio() failed : {e}")
    return


def send_img(chat_id, file_path, description='', base_url=base_url):
    if not file_path or not chat_id: return
    method = "sendPhoto?"
    try: files = {'photo': open(file_path, 'rb')}
    except Exception as e: return print(f"ERROR: send_img() failed for:\n{e}\n\nOriginal message:\n{file_path}\n\nCan't open file.")
    URL = base_url + method + "chat_id=" + str(chat_id) + "&caption=" + description
    r = ''
    try: r = requests.post(URL, files=files)
    except Exception as e: print(f"ERROR : send_img() failed : \n{e}")
    return r

# Telegram bot send file to chat_id
def send_file(chat_id, file_path, description='', base_url=base_url):
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
    url = base_url + "getFile"
    payload = { "file_id": file_id}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200: return
    return response.json()['result']


def convert_m4a_to_wav(m4a_file):
    if debug:
        print(f"DEBUG: convert_m4a_to_wav() {m4a_file}")
    # Set output file name based on M4A file name
    output_file = m4a_file[:-4] + '.wav'

    # Convert the M4A file to WAV using FFmpeg
    os.system(
        f'ffmpeg -y -i {m4a_file} -acodec pcm_s16le -ar 44100 {output_file}')

    # Print success message
    if debug:
        print(f'DEBUG: convert_m4a_to_wav() output : {output_file}')
    return output_file


def get_elevenlabs_userinfo():
    url = "https://api.elevenlabs.io/v1/user"
    headers = {
        "accept": "application/json",
        "xi-api-key": eleven_api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()


def elevenlabs_add_voice(audio_file_path):
    name = str(audio_file_path).split('.')[0].split('/')[-1]
    curl_command = (f"curl -X 'POST' "
                    f"'https://api.elevenlabs.io/v1/voices/add' "
                    f"-H 'accept: application/json' "
                    f"-H 'xi-api-key: {eleven_api_key}' "
                    f"-H 'Content-Type: multipart/form-data' "
                    f"-F 'name={name}' "
                    f"-F 'files=@{audio_file_path};type=audio/wav' "
                    f"-F 'labels='")
    # Execute the curl command
    process = subprocess.Popen(
        curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode != 0:
        raise Exception(f"Curl command failed: {stderr.decode('utf-8')}")

    # Parse the JSON response
    response = json.loads(stdout.decode('utf-8'))
    return response


def elevenlabs_update_voice(voice_id, voice_name, audio_file_path):
    curl_command = (f"curl -X 'POST' "
                    f"'https://api.elevenlabs.io/v1/voices/{voice_id}/edit' "
                    f"-H 'accept: application/json' "
                    f"-H 'xi-api-key: {eleven_api_key}' "
                    f"-H 'Content-Type: multipart/form-data' "
                    f"-F 'name={voice_name}' "
                    f"-F 'files=@{audio_file_path};type=audio/wav' "
                    f"-F 'labels='")

    # Execute the curl command
    process = subprocess.Popen(
        curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode != 0:
        raise Exception(f"Curl command failed: {stderr.decode('utf-8')}")

    # Parse the JSON response
    response = json.loads(stdout.decode('utf-8'))
    return response


def get_elevenlabs_voices():
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {
        'accept': 'application/json',
        'xi-api-key': eleven_api_key
    }
    response = requests.get(url, headers=headers).json()
    # if debug: print(f"DEBUG: {response}")
    voices_dict = {}
    for voice in response['voices']:
        if voice['category'] == 'cloned':
            voices_dict[voice['name']] = voice['voice_id']
    # if debug: print(f"DEBUG: {voices_dict}")
    return voices_dict


def eleven_labs_tts(content, tts_file_name, voice_id='YEhWVRrlzrtA9MzdS8vE'):
    if debug:
        print(f"DEBUG: eleven_labs_tts() voice_id: {voice_id}")
    API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    if debug:
        print(f"DEBUG: eleven_labs_tts() API_URL : {API_URL}")

    headers = {"xi-api-key": eleven_api_key}
    data = {
        "text": content,
        "voice_settings": {
            "stability": 0.95,
            "similarity_boost": 0.95
        }
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            with open(tts_file_name, "wb") as f:
                f.write(response.content)
            return tts_file_name
        except Exception as e:
            print(
                f"ERROR : wring response.content to tts_file_name FAILED.\response.reason:{response.reason}\ntts_file_name:{tts_file_name}\nerror: {e}")
    return False


def did_upload_img(img_file_name):
    if debug:
        print(f"DEBUG: did_upload_img()")
    url = "https://api.d-id.com/images"

    files = {"image": ("leo_img.png", open(img_file_name, "rb"), "image/png")}
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {DID_API_KEY}"
    }
    img_url = ''
    try:
        response = requests.post(url, files=files, headers=headers)
        if debug:
            print(f"DEBUG: did_upload_img() response.text : {response.text}")
        response_dict = response.json()
        img_url = response_dict.get('url')
        if debug:
            print(f"DEBUG: did_upload_img() response url : {img_url}")
    except Exception as e:
        print(f"ERROR : did_upload_img() failed for {e}")
    return img_url


def did_upload_audio(tts_file_name):
    if debug:
        print(f"DEBUG: did_upload_audio()")
    url = "https://api.d-id.com/audios"

    files = {"audio": ("leo_audio.mp3", open(
        tts_file_name, "rb"), "audio/mpeg")}
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {DID_API_KEY}"
    }
    audio_url = ''
    try:
        response = requests.post(url, files=files, headers=headers)
        response_dict = response.json()
        audio_url = response_dict.get('url')
        if debug:
            print(f"DEBUG: did_upload_audio() response url : {audio_url}")
    except Exception as e:
        print(f"ERROR : did_upload_audio() failed for {e}")
    return audio_url


def did_create_talkinghead(img_url, audio_url):
    if debug:
        print(f"DEBUG: did_create_talkinghead()")
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "audio",
            "provider": {
                "type": "microsoft",
                "voice_id": "Jenny"
            },
            "ssml": "false",
            "audio_url": audio_url
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": img_url
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {DID_API_KEY}"
    }
    video_id = ''
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_dict = response.json()
        video_id = response_dict.get('id')
        if debug:
            print(f"DEBUG: did_create_talkinghead() video_id : {video_id}")
    except Exception as e:
        print(f"ERROR : did_create_talkinghead() failed for {e}")
    return video_id


def did_get_talkinghead(video_id):
    if debug:
        print(f"DEBUG: did_get_talkinghead()")
    url = "https://api.d-id.com/talks?limit=1"

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {DID_API_KEY}"
    }

    result_url = ''
    try:
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        result_video_id = response_dict.get('talks')[0].get('id')
        if result_video_id == video_id:
            result_url = response_dict.get('talks')[0].get('result_url')
        else:
            print(
                f"ERROR : did_get_talkinghead() get no video clip has the same video id, only get id: {result_video_id}")
    except Exception as e:
        print(f"ERROR : did_get_talkinghead() failed for {e}")
    return result_url


def did_get_credits():
    url = "https://api.d-id.com/credits"

    headers = {
        "accept": "application/json",
        "authorization": "Basic Y0hKbFlXNW5aV3hzWlc5QVoyMWhhV3d1WTI5dDpCR3JsbEFRbFhpcGJjaHhDY0ZRUDQ="
    }
    try:
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        r = f"CREDITS: remain credits: {str(response_dict.get('remaining'))} / total credits: {str(response_dict.get('total'))}"
        return r
    except Exception as e:
        return e


def get_latest_file(path='json_datas/img/did_img/'):
    files = [os.path.join(path, f) for f in os.listdir(path)]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files


def get_files_list(path='json_datas/img/did_img/'):
    allowed_extensions = ('.png', '.jpg', '.jpeg')
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(
        os.path.join(path, f)) and f.lower().endswith(allowed_extensions)]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    files = [file.split('/')[-1] for file in files]
    return files

# Generate tts from google gTTS api or find audio file if exist from eleven labs with my voice


def generate_or_read_tts_11_labs(folder='leo_voice', content='you forgot to put a content', voice_id='YEhWVRrlzrtA9MzdS8vE'):
    # if debug: print(f"DEBUG: generate_or_read_tts_11_labs()")
    if folder not in ['sentences_tts', 'word_tts', 'ai_chat', 'leo_voice']: return
    content = str(content)
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    tts_file_name = f"json_datas/{folder}/{hashed_content}.mp3"
    if os.path.isfile(tts_file_name): return tts_file_name
    try:
        new_tts_file_name = ''
        new_tts_file_name = eleven_labs_tts(content, tts_file_name, voice_id)
        if new_tts_file_name: return new_tts_file_name
    except: return

def microsoft_azure_tts(text, voice='zh-CN-YunxiNeural', output_filename='output.wav'):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv(
        'SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=True, filename=output_filename)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return output_filename
    return False

# Generate tts from AZURE api or find audio file if exist


def generate_or_read_tts_male(folder='sentences_tts', content='you forgot to put a content', is_chinese=False):

    if folder not in ['sentences_tts', 'word_tts', 'ai_chat']:
        return
    content = str(content)
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    tts_file_name = f"json_datas/{folder}/{hashed_content}.mp3"

    if os.path.isfile(tts_file_name):
        return tts_file_name

    if is_chinese:
        voice = 'zh-CN-YunxiNeural'  # 中文男声
    else:
        voice = 'en-US-GuyNeural'

    return microsoft_azure_tts(content, voice, tts_file_name)

# Generate tts from AZURE api or find audio file if exist


def generate_or_read_tts_female(folder='sentences_tts', content='you forgot to put a content', is_chinese=False):

    if folder not in ['sentences_tts', 'word_tts', 'ai_chat']:
        return
    content = str(content)
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    tts_file_name = f"json_datas/{folder}/{hashed_content}.mp3"

    if os.path.isfile(tts_file_name):
        return tts_file_name

    if is_chinese:
        voice = 'zh-CN-shaanxi-XiaoniNeural'  # 中文陕西话女声
    else:
        voice = 'en-US-JennyNeural'

    return microsoft_azure_tts(content, voice, tts_file_name)

# Generate tts from AZURE api or find audio file if exist


def generate_or_read_tts(folder='sentences_tts', content='you forgot to put a content', is_chinese=False):

    if folder not in ['sentences_tts', 'word_tts', 'ai_chat']:
        return
    content = str(content)
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    tts_file_name = f"json_datas/{folder}/{hashed_content}.mp3"

    if os.path.isfile(tts_file_name):
        return tts_file_name

    if is_chinese:
        voice = 'zh-CN-YunxiNeural'
    else:
        voice = 'en-US-TonyNeural'

    return microsoft_azure_tts(content, voice, tts_file_name)


def escape_quotes(sentence):
    if debug:
        print(f"DEBUG: escape_quotes()")
    # Escape single quotes
    sentence = re.sub(r"(')", r"\\\1", sentence)
    # Escape double quotes
    sentence = re.sub(r'(")', r"\\\1", sentence)
    return sentence


def st_update_sentences(sentence):
    if debug:
        print(f"DEBUG: st_update_sentences()")
    escaped_sentence = escape_quotes(sentence)
    hashed_content = hashlib.md5(
        escaped_sentence.lower().encode('utf-8')).hexdigest()
    df = pd.read_sql_query(
        f"SELECT * FROM `db_lemmas_sentences` WHERE `hash`='{hashed_content}'", db_engine)
    if df.empty:
        words_dict = {'sentence': escaped_sentence,
                      'hash': hashed_content, 'update_time': datetime.now()}
        for update_column in ['hash', 'sentence', 'update_time']:
            update_value = words_dict[update_column]
            r = update_or_insert_data(
                db_engine, 'db_lemmas_sentences', 'hash', hashed_content, update_column, update_value)
        tts_file_name = generate_or_read_tts(
            folder='sentences_tts', content=escaped_sentence)
        # if r and debug: print(f"DEBUG: tts_file_name: {tts_file_name}")
        return tts_file_name
    else:
        return f"json_datas/sentences_tts/{hashed_content}.mp3"


def get_openai_models(api_key=OPENAI_API_KEY_FREE):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.openai.com/v1/models"
    response = requests.get(url, headers=headers)
    return response.json()


def chat_gpt_full(prompt, system_prompt='', user_prompt='', assistant_prompt='', dynamic_model='', chatgpt_key=''):
    if not prompt:
        return

    if not dynamic_model:
        dynamic_model = "gpt-4" if '4' in prompt else "gpt-3.5-turbo"
    if not system_prompt:
        system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work."
    if not user_prompt:
        user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt:
        assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."
    if not chatgpt_key:
        chatgpt_key = OPENAI_API_KEY_FREE

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


def chat_gpt_regular(prompt, chatgpt_key=openai_key, use_model='gpt-3.5-turbo'):
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


def chat_gpt_word_synonyms(prompt, chatgpt_key):
    if not prompt or not chatgpt_key:
        return
    if debug:
        print(f"DEBUG: chat_gpt_word_synonyms() prompt: {prompt}")

    system_prompt = f"You are a highly respected English teacher who is not only a language master but also knows synonyms of every word, when I send a curten word to you, you will reply maximum 5 synonyms words to me, each synonym should be one single word, not a phrase, and not using word that contains - as a connector."

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "ostentatious"},
            {"role": "assistant",
                "content": "showy pretentious pompous bombastic grandiloquent"},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply


def chat_gpt_word_correction(prompt, chatgpt_key=''):
    if not prompt or not chatgpt_key:
        return
    if debug:
        print(f"DEBUG: chat_gpt_word_correction() prompt: {prompt}")

    system_prompt = f"You are a highly respected English teacher who is not only a language master but can also spot minor errors in English spelling, even if it's just a subtitle. I am your student now, and I am sending you a word. Can you check if it's spelled wrong? If it's misspelled, please provide the correct English word. If it's not misspelled but the word is in plural form, please provide the singular form of the word. If the word is a progressive or past tense form of a verb or another form, please provide the word accordingly. Reply only the correct answer, no other words or punctuation. If you are not sure, please reply not sure."

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "acurate"},
            {"role": "assistant", "content": "accurate"},
            {"role": "user", "content": "ostentetious"},
            {"role": "assistant", "content": "ostentatious"},
            {"role": "user", "content": "working"},
            {"role": "assistant", "content": "work"},
            {"role": "user", "content": "sought"},
            {"role": "assistant", "content": "seek"},
            {"role": "user", "content": "written"},
            {"role": "assistant", "content": "write"},
            {"role": "user", "content": "mythetery"},
            {"role": "assistant", "content": "not sure"},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    if debug:
        print(f"DEBUG: chat_gpt_word_correction() reply: {reply}")
    return reply


def chat_gpt(prompt, system_prompt=''):
    if not prompt:
        return
    if debug:
        print(f"DEBUG: chat_gpt() prompt length: {len(prompt.split())}")

    dynamic_model = "gpt-4" if '4' in prompt else "gpt-3.5-turbo"

    if debug:
        print(f"DEBUG: chat_gpt() dynamic_model: {dynamic_model}")

    if not system_prompt:
        system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work. Answer with the same language as the question, and try to answer the question as much as possible."

    # Load your API key from an environment variable or secret management service
    openai.api_key = openai_key

    response = openai.ChatCompletion.create(
        model=dynamic_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    if debug:
        print(f"DEBUG: chat_gpt() repled: \n\n{reply}")

    return reply

# Dalle2 downloading and send img


def dalle2_download_and_sent_img(image_url, chat_id, prompt=''):
    if debug:
        print(f"DEBUG: dalle2_download_and_sent_img()")
    # Download the image and save it to a file
    image_data = requests.get(image_url).content
    if not image_data:
        return

    if not prompt:
        prompt = str(datetime.now().timestamp())

    filename = hashlib.md5(prompt.encode()).hexdigest() + ".png"
    file_path = f"json_datas/img/dalle2/{filename}"
    with open(file_path, "wb") as f:
        f.write(image_data)

    try:
        send_img(chat_id, file_path, description='')
    except:
        print(f"FAILED SENDING IMG to chat_id: {chat_id}")
    return

# Generating img based on replicate api


def generative_ai_replicate(prompt, chat_id=''):
    if debug:
        print(f"DEBUG: generative_ai_replicate()")
    prompt = str(prompt).lower()

    model_name = 'midjourney'
    seed = ''
    steps = ''
    scale = ''
    num = 1
    negative = ''

    if 'midjourney' in prompt:
        model_name = 'midjourney'
        prompt = prompt.replace('midjourney', '')

    if 'openjourney' in prompt:
        model_name = 'openjourney'
        prompt = prompt.replace('openjourney', '')

    if 'seed' in prompt:
        prompt_list = prompt.split()
        seed = prompt_list[prompt_list.index('seed')+1]
        try:
            seed = int(seed)
        except:
            seed = False
        prompt = prompt.replace('seed', '').replace(str(seed), '')

    if 'steps' in prompt:
        prompt_list = prompt.split()
        steps = prompt_list[prompt_list.index('steps')+1]
        try:
            steps = int(steps)
        except:
            steps = False
        prompt = prompt.replace('steps', '').replace(str(steps), '')

    if 'scale' in prompt:
        prompt_list = prompt.split()
        scale = prompt_list[prompt_list.index('scale')+1]
        try:
            scale = int(scale)
        except:
            scale = False
        prompt = prompt.replace('scale', '').replace(str(scale), '')

    if 'num' in prompt:
        prompt_list = prompt.split()
        try:
            num = prompt_list[prompt_list.index('num')+1]
            num = int(num)
        except:
            num = 1
        prompt = prompt.replace('num', '').replace(str(num), '')

    if 'negative' in prompt:
        prompt, negative = prompt.rsplit('negative', 1)

    os.environ["REPLICATE_API_TOKEN"] = replicate_key
    model_address = {
        'openjourney': 'prompthero/openjourney',
        'midjourney': 'tstramer/midjourney-diffusion'
    }
    modle_id = {
        'openjourney': '9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb',
        'midjourney': '436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b'
    }
    model = replicate.models.get(model_address.get(model_name))
    version = model.versions.get(modle_id.get(model_name))

    inputs = {
        # Input prompt
        'prompt': prompt,

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Width of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'width': 512,

        # Height of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'height': 512,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    if seed:
        inputs['seed'] = seed
    if steps:
        inputs['num_inference_steps'] = steps
    if scale:
        inputs['guidance_scale'] = scale
    if num:
        inputs['num_outputs'] = num
    if negative:
        inputs['negative_prompt'] = negative

    if model_name == 'midjourney':
        inputs['prompt_strength'] = 0.8
        inputs['scheduler'] = 'DPMSolverMultistep'

    if debug:
        print_out = [f"{k}: {v}" for k, v in inputs.items(
        ) if k not in ['prompt', 'width', 'height', 'negative_prompt']]
        print(f"DEBUG: {' '.join(print_out)}")

    try:
        out = version.predict(**inputs)
    except Exception as e:
        print(f"ERROR : generative_ai_replicate() {e}")
        return
    # if debug: print(f"output: {out}")

    if not chat_id:
        streamlit_filepath_list = []

    for i in range(num):
        filename = hashlib.md5((prompt+str(i)).encode()).hexdigest() + ".png"
        file_path = f"json_datas/img/replicate/{filename}"
        urlretrieve(out[i], file_path)
        if not chat_id:
            streamlit_filepath_list.append(file_path)
        else:
            try:
                send_img(chat_id, file_path, description=prompt)
            except:
                print(
                    f"ERROR : FAILED SENDING the {i} IMG to chat_id: {chat_id}")
    if not chat_id:
        return streamlit_filepath_list
    else:
        return prompt

# Get caption from img


def replicate_img_to_caption(file_path, chat_id=bot_owner_chat_id):
    if debug:
        print(f"DEBUG: replicate_img_to_caption()")

    os.environ["REPLICATE_API_TOKEN"] = replicate_key

    model = replicate.models.get("salesforce/blip")
    version = model.versions.get(
        "2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
    inputs = {
        # Input image
        'image': open(file_path, "rb"),
        # Choose a task.
        'task': "image_captioning",
    }

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    output = ''
    try:
        output = version.predict(**inputs)
    except:
        pass

    return output

# Generating img based on prompt


def generate_dalle2_image(prompt, chat_id=bot_owner_chat_id):
    if debug:
        print(f"DEBUG: generate_dalle2_image()")

    # Make the API request
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
    except openai.error.OpenAIError as e:
        print('FAILURE :', e.error)
        return

    image_url = response['data'][0]['url']

    try:
        dalle2_download_and_sent_img(image_url, chat_id, prompt)
    except:
        print(f"FAILED executing dalle2_download_and_sent_img()")
    return


def generate_dalle2_image_variations(file_path, chat_id=bot_owner_chat_id):
    if debug:
        print(f"DEBUG: generate_dalle2_image_variations()")

    # Read the image file from disk and resize it
    image = Image.open(file_path)
    width, height = 512, 512
    image = image.resize((width, height))

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    try:
        response = openai.Image.create_variation(
            image=byte_array,
            n=1,
            size="1024x1024"
        )
    except openai.error.OpenAIError as e:
        print(e.error)
        return

    image_url = response['data'][0]['url']

    try:
        dalle2_download_and_sent_img(image_url, chat_id)
    except:
        print(f"FAILED executing dalle2_download_and_sent_img()")
    return


def seal_db_daily_words():
    df = pd.read_sql_query(
        f"SELECT `word`, `synonyms` FROM `db_daily_words` WHERE `chat_gpt_explanation` IS NOT NULL AND `origin` IS NOT NULL AND `synonyms` IS NOT NULL AND `sealed`=0", db_engine)
    word_conn = db_engine.connect()
    for word in df['word']:
        try:
            word_conn.execute(
                f'UPDATE db_daily_words SET sealed=1 WHERE word="{word}"')
        except:
            print(f"ERROR : seal_db_daily_words(): {word} FAILED!")
        print(f"SUCCESS : seal_db_daily_words(): {word} just SEALED!")
    word_conn.close()
    return


def find_out_synonyms_2(text):
    synonyms = re.findall(r'Synonyms:\s*(.*)\.', text)
    if synonyms:
        return [w.strip() for w in synonyms[0].split(',')[:5]]
    else:
        return


def append_synonyms_to_database(key_word, synonyms_new):
    if debug:
        print(f"DEBUG: append_synonyms_to_database()")
    key_word = str(key_word).lower()
    df_word = pd.read_sql_query(
        f'SELECT * FROM `db_daily_words` WHERE word="{key_word}"', db_engine)
    if df_word.empty:
        return
    synonyms_word_list = st_remove_puctuations_and_duplicated_contents(
        synonyms_new)
    new_synonyms_word_list = [word for word in synonyms_word_list if word not in [
        key_word, 'synonym', 'synonyms', 'of', 'to', 'the', 'a', 'b', 'as', 'if', 'with', 'to', 'for', 'None', 'none', 'no']]
    if not new_synonyms_word_list:
        return
    df_all = pd.read_sql_query(
        f'SELECT `word`, `rank` FROM `db_daily_words`', db_engine)
    df = df_all.query('word in @new_synonyms_word_list')
    if df.empty or df.shape[0] < len(new_synonyms_word_list):
        if debug:
            print(f"DEBUG: df.shape[0] < len(new_synonyms_word_list")
        for word in new_synonyms_word_list:
            if word not in df['word'].to_list():
                single_word = word[:-2] if str(word).endswith(
                    'es') else word[:-1] if str(word).endswith('s') else ''
                if not single_word:
                    continue
                new_synonyms_word_list.append(single_word)
                if debug:
                    print(
                        f"DEBUG: append_synonyms_to_database just replaced {word} with {single_word}")
        df = df_all.query('word in @new_synonyms_word_list')
        if df.empty:
            return
    df = df.sort_values(by=['rank'], ascending=True)
    db_dict = df[['word', 'rank']].set_index('word').to_dict()['rank']
    if not db_dict:
        return
    synonyms_list = [f"{k}({int(v)})" for k,
                     v in db_dict.items() if not math.isnan(v)]
    updated_synonyms = ' | '.join(synonyms_list)
    try:
        word_conn = db_engine.connect()
        word_conn.execute(
            f'UPDATE `db_daily_words` SET `synonyms`="{updated_synonyms}", `sealed`=1 WHERE `word`="{key_word}"')
        if debug:
            print(
                f"DEBUG: Synonyms updated and sealed: {key_word} : synonyms len : {len(synonyms_list)}")
    except:
        pass
    word_conn.close()
    return updated_synonyms


def update_db_daily_words_origin():
    if debug:
        print(f"DEBUG: update_db_daily_words_origin()")
    df = pd.read_sql_query(
        f'SELECT `word`, `rank` FROM `db_daily_words` WHERE `origin` IS NULL ORDER BY `rank` ASC', db_engine)
    if df.empty:
        if debug:
            print(f"DEBUG: update_db_daily_words_origin() FINISHED time.sleep(60*60*12)")
        time.sleep(60*60*12)
        return
    for i in range(df.shape[0]):
        if debug:
            print(
                f"DEBUG: update_db_daily_words_origin(): {i} {df.iloc[i]['word']} ({df.iloc[i]['rank']})")
        try:
            origin = chat_gpt(
                f"What's the root or origin of word: {df.iloc[i]['word']}, And what's the Chinese meaning.")
        except:
            continue
        if not origin:
            continue
        origin = origin.replace('\n\n', '\n')
        try:
            update_or_insert_data(
                db_engine, 'db_daily_words', 'word', df.iloc[i]['word'], 'origin', origin)
        except:
            pass
    return


def update_db_daily_words_synonyms():
    if debug:
        print(f"DEBUG: update_db_daily_words_synonyms()")
    df = pd.read_sql_query(
        f'SELECT `word`, `rank` FROM `db_daily_words` WHERE `synonyms` IS NULL AND `note` IS NULL ORDER BY `rank` ASC', db_engine)
    if df.empty:
        try:
            update_db_daily_words_origin()
        except:
            print(f"ERROR : update_db_daily_words_origin() Falied: ({e})")
        return
    for i in range(df.shape[0]):
        if debug:
            print(f"DEBUG: {i} : {df.iloc[i]['word']} ({df.iloc[i]['rank']})")
        try:
            note = chat_gpt(
                f"give me five synonyms of word: {df.iloc[i]['word']}, each synonym shoule be one single word, not a phrase, and don't use word that contains '-'.")
        except:
            continue
        if not note:
            continue
        try:
            update_or_insert_data(
                db_engine, 'db_daily_words', 'word', df.iloc[i]['word'], 'note', note)
        except:
            pass
        new_synonyms_list = st_extract_words(note)
        new_synonyms_list = new_synonyms_list[:5] if new_synonyms_list else []
        if not new_synonyms_list:
            new_synonyms_list = find_out_synonyms_2(note.lower())
        if not new_synonyms_list:
            continue
        updated_synonyms = ' '.join(new_synonyms_list)
        if debug:
            print(
                f"DEBUG: {i} {df.iloc[i]['word']} ({df.iloc[i]['rank']}) updated_synonyms : {updated_synonyms}")
        if not updated_synonyms:
            continue
        try:
            updated_synonyms = append_synonyms_to_database(
                df.iloc[i]['word'], updated_synonyms)
        except:
            continue
    return


def update_db_daily_words_chat_gpt():
    if debug:
        print(f"DEBUG: update_db_daily_words_chat_gpt()")
    df = pd.read_sql_query(
        f'SELECT `word`, `rank` FROM `db_daily_words` WHERE `chat_gpt_explanation` IS NULL ORDER BY `rank` ASC LIMIT 1', db_engine)
    if df.empty:
        try:
            update_db_daily_words_synonyms()
        except Exception as e:
            print(f"ERROR : update_db_daily_words_synonyms() Failed: ({e})")
        return
    if debug:
        print(
            f"DEBUG: update_db_daily_words_chat_gpt(): {df.iloc[0]['word']} ({df.iloc[0]['rank']})")
    try:
        responsed_content = chat_gpt(
            f"What is the English explanation of {df.iloc[0]['word']}")
    except:
        responsed_content = 'Last time update from chatgpt failed, please UPDATE mannully.'
    try:
        r = update_or_insert_data(db_engine, 'db_daily_words', 'word',
                                  df.iloc[0]['word'], 'chat_gpt_explanation', responsed_content)
    except:
        print(
            f"ERROR : {df.iloc[0]['word']} ({df.iloc[0]['rank']}) chat_gpt_explanation update failed.")
    return


def st_english_study_report():
    df_daily = pd.read_sql_query(
        f"SELECT `word`, `rank`, `sealed`, `gre`, `sat`, `toefl`, `gmat`, `last_check_time` FROM `db_daily_words`", db_engine)
    total_words = df_daily.shape[0]

    df_sealed = df_daily.query('sealed==1')
    sealed_words_list = df_sealed.word.to_list()

    df_category = df_daily.query(
        '(gre==1 | sat==1 | gmat==1 | toefl==1) & sealed==0')
    df_category_list = df_category.word.to_list()

    today = datetime.now().date()
    df_today = df_daily[df_daily["last_check_time"].dt.date.eq(today)]

    initial_date = '2022-11-01 00:00:01'
    start_date = datetime.fromisoformat(initial_date)
    finish_date = df_today['last_check_time'].max()
    study_date = finish_date - start_date

    df_today = df_today.sort_values(by=['last_check_time'], ascending=False)
    today_words_count = df_today.shape[0]

    essential_words_df = df_today.query('gre==1 | sat==1 | toefl==1 | gmat==1')
    today_essential_words_list = essential_words_df['word'].to_list()

    report = f"{datetime.today().date()} 学习报告: \n\n您今天查询并学习英文单词 {today_words_count} 个, 其中属于 TOEFL/GRE/GMAT/SAT 精华的单词共 {len(today_essential_words_list)} 个. 您的个人学习词典数据库一共同步了 {total_words} 个英文单词, 其中有 {len(sealed_words_list)} 个单词已经完成与 CHAT GPT 的信息同步(数据库 Sealed)。从 {str(initial_date).split()[0]} 开始本次英语学习旅程以来, 您已经坚持了 {str(study_date).split()[0]} 天, 请继续坚持! 聪明人也要下笨功夫, 更何况你这样的笨蛋, 别松懈哦!"
    return report, today_words_count, today_essential_words_list, df_category_list, sealed_words_list


def read_pdf_and_save_as_txt(file_path):
    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        text = ''
        for i in range(len(pdf.pages)):
            text += pdf.pages[i].extract_text() + '\n'

        filename = os.path.splitext(file_path)[0] + f'.txt'
        with open(filename, 'w') as f:
            f.write(text)

    return filename


def retrieve_email(email_address=GMAIL_CHATGPT_ADDRESS, email_passwd=GMAIL_CHATGPT_PASSWD):
    if debug: print(f"DEBUG: retrieve_email() for {email_address}")
    # 登录邮箱
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(email_address, email_passwd)

    # 选择邮箱
    imap_server.select("INBOX")

    # 搜索未读邮件
    typ, search_data = imap_server.search(None, "UNSEEN")

    new_inbox = []
    if search_data:
        email_ids = search_data[0].split()
        for email_id in email_ids:
            try:
                typ, fetch_data = imap_server.fetch(email_id, "(RFC822)")
                # 解析邮件
                msg = email.message_from_bytes(fetch_data[0][1])
                processed_mime_part = False  # Add a flag to track MIME part processing
                for part in msg.walk():

                    if processed_mime_part: break

                    subject_decoded = 'NO SUBJECT'
                    try:
                        subject_parts = email.header.decode_header(msg["Subject"])
                        subject_decoded_parts = []
                        for head_part, charset in subject_parts:
                            if charset is not None: head_part = head_part.decode(charset)
                            subject_decoded_parts.append(head_part)
                        subject_decoded = ''.join(subject_decoded_parts)
                    except Exception as e: print(f"DEBUG: {msg['From']} subject_decoded failed: {str(e)}")

                    email_body = ''
                    encodings_to_try = ['utf-8', 'gb18030', 'iso-8859-1', 'cp1252']
                    for encoding in encodings_to_try:
                        try:
                            email_body = part.get_payload(decode=True).decode(encoding)
                            print(f"DEBUG: {msg['From']} email_body successfully with encoding: {encoding}")
                            break
                        except (UnicodeDecodeError, AttributeError): pass

                    if not email_body: continue

                    if part.get_content_type() == 'text/html':
                        # 从html中提取纯文本
                        soup = BeautifulSoup(email_body, 'html.parser')
                        email_body = soup.get_text()
                        if not email_body: continue
                        if debug: print(f"DEBUG: {msg['From']} email_body from HTML: \n\n{email_body}\n\n")

                    if [msg["From"], subject_decoded, email_body] not in new_inbox:
                        new_inbox.append([msg["From"], subject_decoded, email_body])
                        processed_mime_part = True  # Set the flag to True after processing a MIME part

            except: pass
    else: print(f"DEBUG: retrieve_email() NO DATA from {email_address}.")

    return new_inbox

def retrieve_email_with_attachments(email_address=GMAIL_CHATGPT_ADDRESS, email_passwd=GMAIL_CHATGPT_PASSWD):
    debug = False
    if debug: print(f"DEBUG: retrieve_email() for {email_address}")
    # 登录邮箱
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(email_address, email_passwd)

    # 选择邮箱
    imap_server.select("INBOX")

    # 搜索未读邮件
    typ, search_data = imap_server.search(None, "UNSEEN")

    new_inbox = []
    attachment_folder = 'json_datas/files/email_attachments'
    if search_data:
        email_ids = search_data[0].split()
        for email_id in email_ids:
            if debug: print(f"DEBUG: retrieve_email() email_id: {email_id}")
            try:
                typ, fetch_data = imap_server.fetch(email_id, "(RFC822)")
                # 解析邮件
                msg = email.message_from_bytes(fetch_data[0][1])
                attachment_filenames = []
                p = 0
                for part in msg.walk():
                    p += 1
                    if debug: print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p}")

                    subject_decoded = 'NO SUBJECT'
                    try:
                        subject_parts = email.header.decode_header(msg["Subject"])
                        subject_decoded_parts = []
                        for head_part, charset in subject_parts:
                            if charset is not None: head_part = head_part.decode(charset)
                            subject_decoded_parts.append(head_part)
                        subject_decoded = ''.join(subject_decoded_parts)
                    except Exception as e: print(f"ERROR: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} subject_decoded failed: {str(e)}")

                    email_body = ''
                    encodings_to_try = ['utf-8', 'gb18030', 'cp1252']
                    for encoding in encodings_to_try:
                        try:
                            email_body = part.get_payload(decode=True).decode(encoding)
                            print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} email_body with encoding: {encoding}, \n{subject_decoded}\n{email_body}")
                            break
                        except Exception as e: print(f"ERROR: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} email_body failed with encoding: {encoding}, {str(e)}")

                    if not email_body: 
                        if debug: print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} email_body is empty, continue")
                        continue

                    # if part.get_content_type() == 'text/html':
                    #     # 从html中提取纯文本
                    #     soup = BeautifulSoup(email_body, 'html.parser')
                    #     email_body = soup.get_text()
                    #     if not email_body: continue
                    #     if debug: print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} email_body text from beautifulsoup, \n{subject_decoded}\n{email_body}")
                    
                    try:
                        # Check if part is an attachment
                        if part.get_content_disposition(): 
                            filename = part.get_filename()
                            if filename and filename.lower()[-4:] in ['.txt', '.pdf', 'ppt', 'pptx', '.doc', '.docx', '.csv']:
                                # get file base name
                                basename = os.path.basename(filename)
                                # create new file name
                                filename = os.path.join(attachment_folder, basename)
                                with open(filename, 'wb') as f: f.write(part.get_payload(decode=True))
                                attachment_filenames.append(filename)
                                if debug: print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} {subject_decoded} just got attachment: {filename}")

                    except Exception as e: print(f"DEBUG: retrieve_email() email_id: {email_id} : part: {p} : {msg['From']} {subject_decoded} attachment retrieve failed: {e}")
                    
                    break
                    
                new_added_email = [msg["From"], subject_decoded, email_body, attachment_filenames]        
                
                if new_added_email not in new_inbox: new_inbox.append(new_added_email)

            except: pass
    else: print(f"DEBUG: retrieve_email() NO DATA from {email_address}.")

    return new_inbox


def send_email(email_content, to_address, subject="Talking with ChatGPT", smtp_username=GMAIL_CHATGPT_ADDRESS, smtp_password=GMAIL_CHATGPT_PASSWD):

    # 设置邮箱服务器信息
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

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


def send_email_with_attachments(email_content, to_address, subject="Talking with ChatGPT", attachments=[], smtp_username=GMAIL_CHATGPT_ADDRESS, smtp_password=GMAIL_CHATGPT_PASSWD):
    # import smtplib
    from email.mime.multipart import MIMEMultipart
    # from email.mime.text import MIMEText
    from email import encoders
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    # 设置邮箱服务器信息
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 创建邮件内容
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = smtp_username
    message["To"] = to_address

    # 邮件正文
    message.attach(MIMEText(email_content))

    # 构造附件
    for attachment in attachments:
        with open(attachment, 'rb') as f:
            file_type = attachment.split('.')[-1].lower()
            try:
                if file_type in ['png', 'jpeg', 'jpg', 'gif']:
                    mime = MIMEImage(f.read(), _subtype=file_type)
                elif file_type in ['mp3', 'mp4']:
                    mime = MIMEAudio(f.read(), _subtype=file_type)
                elif file_type in ['txt', 'srt']:
                    mime = MIMEText(f.read(), _subtype='plain')
                elif file_type in ['doc', 'docx']:
                    mime = MIMEApplication(f.read(), _subtype='vnd.openxmlformats-officedocument.wordprocessingml.document', name=attachment)
                elif file_type in ['ppt', 'pptx']:
                    mime = MIMEApplication(f.read(), _subtype='vnd.openxmlformats-officedocument.presentationml.presentation', name=attachment)
                elif file_type in ['xls', 'xlsx']:
                    mime = MIMEApplication(f.read(), _subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', name=attachment)

                else:
                    mime = MIMEBase('application', 'octet-stream')
                    mime.set_payload(f.read())
                    encoders.encode_base64(mime)
                    mime.add_header('Content-Disposition', 'attachment', filename=attachment)
                message.attach(mime)
            except: pass

    # 发送邮件
    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.starttls()
    smtp_client.login(smtp_username, smtp_password)
    smtp_client.sendmail(smtp_username, to_address, message.as_string())
    smtp_client.quit()
    return True


def chat_gpt_for_email(prompt, system_prompt=''):
    if not prompt:
        return

    prompt_head = prompt.split('\n')[0]
    if 'THE END' in prompt:
        prompt = prompt.split('THE END')[0]

    if debug:
        print(
            f"DEBUG: chat_gpt_for_email() prompt length: {len(prompt.split())}")

    dynamic_model = "gpt-3.5-turbo"
    if not system_prompt:
        system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work. Now you are working as my assistant, helping me to read and reply emails. If 'the end' or '-----' is in email body, pleas ignore the content after 'the end' or '-----', only read the conent ahead of 'the end' or '-----'. Please reply in the way you normally do, make them feel like you are a real person, an erudite and well-informed person. Reply in the same way you would reply to a friend and use the same lanquage and tone."

    # Load your API key from an environment variable or secret management service
    openai.api_key = OPENAI_API_KEY_FREE

    response = openai.ChatCompletion.create(
        model=dynamic_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()
    reply = f"{reply}\n\nAnswered by: {dynamic_model}\n\nSystem Prompt:\n{system_prompt}"

    return reply


def first_time_mail(email_from):
    if not email_from:
        return False
    if debug:
        print(f"DEBUG: first_time_mail() from: {email_from}")

    df = pd.read_sql(
        f"SELECT `email_address`, `in_blacklist` FROM `email_records` WHERE `email_address` = '{email_from}'", db_engine)
    if df.empty:
        send_email(email_welcome, email_from)
        with db_engine.connect() as conn:
            conn.execute(text(
                "INSERT INTO `email_records` (`email_address`) VALUES (:email_address)"), email_address=email_from)
        return True
    elif df['in_blacklist'].values[0]:
        return False
    else:
        return True


def group_send_email(email_content, email_subject):
    if not email_content or not email_subject:
        return

    if debug:
        print(f"DEBUG: group_send_email() is working...")

    df = pd.read_sql(
        "SELECT `email_address` FROM `email_records` WHERE `in_blacklist`=0 GROUP BY `email_address`", db_engine)
    if df.empty:
        return

    email_address_list = df['email_address'].tolist()
    email_address_list = [
        email_address for email_address in email_address_list if '<' not in email_address]
    email_address_list = list(set(email_address_list))

    email_address_sent_list = []
    for email_address in email_address_list:
        if email_address in email_address_sent_list:
            continue

        if debug:
            print(f"DEBUG: group_send_email() email_address: {email_address}")
        email_address_sent_list.append(email_address)
        try:
            send_email(email_content, email_address, email_subject)
        except:
            print(
                f"DEBUG: group_send_email() send_email() email_welcome failed for {email_address}")
        time.sleep(email_check_time_sleep)
    return

# email_from = 'preangelleo@gmail.com'
# conn.execute("UPDATE `email_records` SET `in_blacklist`=0 WHERE `email_address`=%s", (email_from,))


def chatgpt_reply_gmail():
    if debug:
        print(f"DEBUG: chatgpt_analysis_gmail() for {GMAIL_CHATGPT_ADDRESS}")

    new_inbox = retrieve_email(GMAIL_CHATGPT_ADDRESS, GMAIL_CHATGPT_PASSWD)
    if not new_inbox:
        if debug:
            print(
                f"DEBUG: chatgpt_analysis_gmail() No new email for {GMAIL_CHATGPT_ADDRESS}")
        return

    for email_content in new_inbox:
        # 获取邮件内容
        email_from, email_subject, email_body = email_content

        email_from = email_from.lower().strip()
        if '<' in email_from or '>' in email_from:
            match = re.search(r'<(.+)>', email_from)
            if match:
                email_from = match.group(1)

        if '退回' in email_body or 'return' in email_body or '退信' in email_body or '退订' in email_body or 'unsubscribe' in email_body:
            with db_engine.connect() as conn:
                conn.execute(
                    f"UPDATE `email_records` SET `in_blacklist`=1 WHERE `email_address`='{email_from}'")
            continue

        # 首次邮件保存邮箱地址
        r = first_time_mail(email_from)
        if not r:
            continue

        # 回复邮件
        try:
            reply = chat_gpt_for_email(email_body)
            if reply:
                send_email(reply, email_from, email_subject)
                if debug:
                    print(
                        f"DEBUG: chatgpt_analysis_gmail() reply to {email_from}: \n\n{reply}")
        except:
            print(
                f"DEBUG: chatgpt_analysis_gmail() chat_gpt_for_email() failed for {email_from}, email_body: {email_body}")
    return

# conn.execute('DROP TABLE IF EXISTS `email_asistant_whitelist`')
# conn.execute(f"CREATE TABLE IF NOT EXISTS `email_asistant_whitelist` (`id` INTEGER PRIMARY KEY AUTO_INCREMENT, `email_address` TEXT NOT NULL)")


def add_email_to_whitelist(email_address):
    email_address = email_address.lower().strip()
    with db_engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO `email_assistant_whitelist` (`email_address`) VALUES (:email_address)"), email_address=email_address)
    return True


def is_email_in_whitelist(email_address):
    email_address = email_address.lower().strip()
    with db_engine.connect() as conn:
        result = conn.execute(text(
            "SELECT `email_address` FROM `email_assistant_whitelist` WHERE `email_address` = :email_address"), email_address=email_address)
        return result.fetchone() is not None


def download_video_test(url):
    # Download the file from the URL
    r = requests.get(url)
    # Save the file to the directory with a timestamp-based name
    file_name = os.path.join(
        "json_datas/video/did_video/", str(datetime.now().timestamp()) + ".mp4")
    with open(file_name, "wb") as f:
        f.write(r.content)
    # Return the file name
    return file_name


def create_news_podcast(filepath = '', prompt = '', leo_voice = False):
    if not filepath and not prompt: return 

    if filepath and not prompt:
        try: 
            with open(filepath, 'r') as f: prompt = f.read()
        except Exception as e: print(f"ERROR: Can not open {filepath}: {e}")
    
    if not prompt: return

    system_prompt = '''
You are a very experiend news editor and report, you can easly create a news based on google search results. You don't need to click and read every article from google search results, you can simply read the snippets from google results and then you can create a news article based on the snippets. And it's allway eye catching, interesting and amazing. As a report, you know the truth is important, so you don't just make things up, you write based on the snippets, and you don't exaggerate the news, you just write the truth but in a very interesting way. The article will be read using an AI voice generator chosen by your boss, it's important to carefully choose words that are easy to pronounce. This is particularly important for technical terms, where using the full word is more helpful. For instance, instead of using V5 as an abbreviation for Version 5, it's better to write out the full term. Similarly, if you're unsure if readers are familiar with the term LLM, it's better to use the full term Large Language Model instead of the abbreviation. Even with the article title, you do the same. But remember, you don't need to put 'Title' for the beginning of the title. If you're unsure whether an AI voice generator can accurately read a special character, it's best to replace it with a word. For instance, the character / can be written as slash.
'''

    user_prompt = '''
Today's top news about  midjourney v5

1. Newest Model. The Midjourney V5 model is the newest and most advanced model, released on March 15th, 2023. To use this model, add the v 5 parameter to the end of a prompt, or use the slash settings command and select MJ Version 5. This model has very high Coherency, excels at interpreting natural language prompts, is higher resolution, and supports advanced features like repeating ...

2. Midjourney v4 vs Midjourney v5 The fifth edition is a significant improvement, especially when it comes to creating wellknown figures from popular culture. The distinction is most noticeable when the neural network attempts to depict a realistic scene, such as an image, landscape, or indoor space.

3. About. . Midjourney is an independent research lab exploring new mediums of thought and expanding the imaginative powers of the human species. We are a small selffunded team focused on design, human infrastructure, and AI. We have 11 fulltime staff and an incredible set of advisors.

4. MidJourney, the widely popular AIpowered image generator, has just launched its latest version, MidJourney V5. MidJourney decided to drop V5 just a day after OpenAI released GPT4. Crazy week for…

5. To set Midjourney v5 as default, use the /settings command to access your Midjourney settings and then select MJ version 5. To temporarily use Midjourney v5 without setting it as default, use the –v 5 parameter. March 31, 2023: With Midjourney closing for free users, you may want to give BlueWillow a try. Available on Discord, too, it’s ...

6. Midjourney v5 leaps out in front of v4 in the overall visual experience. In v5, we completely lose the "Midjourney look". The new v5 could easily be considered another universe, both in terms of photorealism and details. One of the key factors is a boost in dynamic range that's widely abundant in Midjourney v5 imagery.

7. Midjourney V5. V5 is the latest iteration of Midjourney. It is most definitely better than all its previous versions. For a bit of context, Midjourney released the 5th version a week ago, but it is only in its beta mode now. The V5 is considered more enhanced and powerful than its previous version. For example, it draws a line between artwork ...

8. Style and prompting for V5.  Today’s test is basically a ‘pro’ mode of the model.  It’s MUCH more ‘unopinionated’ than v3 and v4, and is tuned to provide a wide diversity of outputs and to be very responsive to your inputs.  The tradeoff here is that it may be harder to use.

9. Midjourney V5’s system default is the photographic style. It’s what shows up if the prompter does not specify any other styling. In v 5, to generate something other than a photographic image, you will need to reference art movements, artistic techniques, genres, media types, games titles, ...

10. Midjourney is an industry leader in AI generative art. With each new version, it manages to increasingly blur the lines between reality and fantasy. Thanks to ongoing development in algorithms that serve to boost photorealism and dynamic range,

11. На примерах в шапке: Скоро и айфон подруге не нужно будет покупать, можно будет промтом обойтись. Больше интересного у меня в телеге:

12. Make photorealistic images with Midjourney v5, the texttoimage AI that bamboozled the internet with the Pope photo.

13. Make photorealistic images with Midjourney v5, the texttoimage AI that bamboozled the internet with the Pope photo.

14. The problem is, Midjourney is too good. And, the lack of moderation policies makes its case even more concerning
'''

    assistant_prompt = '''
Midjourney Version 5 Revolutionizes AI-Powered Image Generation

In the world of AI-powered image generation, Midjourney has just released its most advanced model yet, the Midjourney Version 5. Launched on March 15, 2023, this new model has raised the bar in terms of coherency, natural language prompt interpretation, and resolution, supporting advanced features that users have come to expect from the industry leader.

The Midjourney Version 5 model significantly surpasses its predecessor, Midjourney Version 4, in creating lifelike depictions of popular culture figures and realistic scenes, including landscapes and indoor spaces. The visual experience offered by Version 5 has been completely transformed, with the "Midjourney look" being replaced by enhanced photorealism and intricate details, thanks in part to a substantial boost in dynamic range.

Midjourney, an independent research lab with 11 full-time staff members, has a mission to explore new mediums of thought and expand human imagination through design, human infrastructure, and AI. Their latest version, currently in beta mode, is a testament to their commitment to innovation and pushing the boundaries of what AI can do.

The Midjourney Version 5 also offers a more versatile and responsive experience for users. The model's 'pro' mode provides a wider diversity of outputs and adapts more readily to user inputs, though this may make it somewhat harder to use. The system default for Version 5 is the photographic style, with options for generating images in different styles by referencing art movements, techniques, genres, and media types.

As an industry leader in AI generative art, Midjourney continues to blur the lines between reality and fantasy with each new iteration. However, some have voiced concerns over the platform's lack of moderation policies, given its growing ability to create stunningly photorealistic images, such as the now-famous Pope photo.

Users can try Midjourney Version 5 by adding the "v 5" parameter to the end of a prompt or by selecting "MJ Version 5" in the settings. While the platform has closed for free users, the AI-powered image generator BlueWillow is available as an alternative for those seeking a similar experience on Discord.
'''

    dynamic_model = 'gpt-4'
    chatgpt_key = openai_key
    
    message = ''
    try: message = chat_gpt_full(prompt, system_prompt, user_prompt, assistant_prompt, dynamic_model, chatgpt_key)
    except Exception as e: print('ERROR: chat_gpt_full() failed:', e)
    if not message: return message

    filepath_news = ''
    try:
        filepath_news = filepath.replace('_snippet.txt', '_news.txt')
        with open(filepath_news, 'w') as f: f.write(message)
    except Exception as e: print('ERROR: writing to file failed:', e)

    filepath_news_mp3 = filepath_news.replace('.txt', '.mp3')
    if filepath_news:
        try:
            if not leo_voice: filepath_news_mp3 = microsoft_azure_tts(message, 'en-US-JaneNeural', filepath_news_mp3)
            else: filepath_news_mp3 = eleven_labs_tts(message, filepath_news_mp3, voice_id='YEhWVRrlzrtA9MzdS8vE')
        except: pass
    return filepath_news_mp3

# 通过 ffmpeg 合并英文语音文件和中文语音文件
def merge_audio_files(audio_files):
    if len(audio_files) == 1: return audio_files[0]
    if len(audio_files) == 0: return None
    merged_audio = audio_files[0].replace('.mp3', '_merged.mp3')
    cmd = f"ffmpeg -i {audio_files[0]} -i {audio_files[1]} -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[out]' -map '[out]' {merged_audio}"
    os.system(cmd)
    return merged_audio

def create_news_and_audio_from_bing_search(query, chat_id=bot_owner_chat_id, parse_mode='', base_url=base_url):
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
    try:
        filepath_news_mp3 = create_news_podcast(filepath = snippet_text_filepath, prompt = '', leo_voice = False)
        filepath_news_txt = filepath_news_mp3.replace('.mp3', '.txt')
        with open(filepath_news_txt, 'r') as f: text_contents = f.read()
        try: 
            send_msg(text_contents, chat_id, parse_mode=parse_mode, base_url=base_url)
            # send_audio(filepath_news_mp3, chat_id, base_url=base_url)
            # send_file(chat_id, snippet_text_filepath, description='', base_url=base_url)
        except Exception as e: print(f"ERROR : send_msg() failed: \n\n{e}")

        try:
            text_cn = 'Translated text'
            # filepath_news_txt_cn = filepath_news_txt.replace('.txt', '_cn.txt')
            try: text_cn = chat_gpt_regular(f"{translate_report_prompt}{text_contents}", openai_key, 'gpt-4')
            except Exception as e: return print(f"ERROR : chat_gpt_regular() translation failed: \n\n{e}")

            # 将中文文本添加至英文文本的末尾
            with open(filepath_news_txt, 'a') as file: file.write(text_cn)
            # with open(filepath_news_txt_cn, 'w') as file: file.write(text_cn)
            send_msg(text_cn, chat_id, parse_mode=parse_mode, base_url=base_url)
            send_file(chat_id, filepath_news_txt, description='中英文内容 Text 文件', base_url=base_url)

            filepath_news_mp3_cn = filepath_news_mp3.replace('.mp3', '_cn.mp3')
            filepath_news_mp3_cn = microsoft_azure_tts(text_cn, 'zh-CN-YunxiNeural', filepath_news_mp3_cn)
            try:
                merged_audio = merge_audio_files([filepath_news_mp3, filepath_news_mp3_cn])
                send_audio(merged_audio, chat_id, base_url=base_url)
            except Exception as e: print(f"ERROR : merge_audio_files() failed: \n\n{e}")

        except Exception as e: print(f"ERROR : chat_gpt_regular() translation failed: \n\n{e}")

        try:
            tweet_content = 'Tweet content'
            # 基于 text_contents 写一段 英文 Tweet 和一段中文 Tweet
            tweet_pre_prompt = "你是市场营销大师，你非常擅长撰写 Tweet 并引起广泛转发和点赞，请基于下面的英文报道写一段简短有力的中文 Tweet，控制好字数不要超过 Twitter 的限制。请注意，涉及到人名和产品名以及品牌名的情况，保留英文即可；涉及到技术专有术语，也请保留英文或者英文缩写。\n\n"
            for gpt_mode in ['gpt-4', 'gpt-3.5-turbo']:
                try:
                    tweet_content = chat_gpt_regular(f"{tweet_pre_prompt}{text_contents}", openai_key, gpt_mode)
                    break
                except Exception as e: print(f"ERROR : chat_gpt_regular() tweet generate failed with {gpt_mode}, will try next mode.")
            send_msg(tweet_content, chat_id, parse_mode=parse_mode, base_url=base_url)
        except Exception as e: print(f"ERROR : chat_gpt_regular() tweet generate failed: \n\n{e}")

        try: send_email_with_attachments(f"{text_contents}\n\n{text_cn}\n\n{tweet_content}", 'preangelleo@gmail.com', subject=query, attachments=[merged_audio], smtp_username=GMAIL_LAOGEGECODING_ADDRESS, smtp_password=GMAIL_LAOGEGECODING_PASSWD)
        except Exception as e: print(f"ERROR : send_email_with_attachments() failed: \n\n{e}")

    except Exception as e: print(f"ERROR : create_news_podcast() failed: \n\n{e}")

    return 

def chat_gpt_english(prompt):
    if not prompt: return

    for dynamic_model in ['gpt-3.5-turbo']:
        # Load your API key from an environment variable or secret management service
        openai.api_key = openai_key
        try:
            if debug: print(f"DEBUG: {dynamic_model} chat_gpt_english length: {len(prompt.split())} 正在创作...")
            response = openai.ChatCompletion.create(
                model=dynamic_model,
                messages=[
                    {"role": "system", "content": english_system_prompt},
                    {"role": "user", "content": english_user_prompt},
                    {"role": "assistant", "content": english_assistant_prompt},
                    {"role": "user", "content": 'Vector database technology has continued to improve, offering better performance and more personalized user experiences for customers.'},
                    {"role": "assistant", "content": '/英译中:\n矢量数据库技术一直在不断改进，为客户提供更佳的性能和更个性化的用户体验。'},
                    {"role": "user", "content": '''To address the challenges of digital intelligance in digital economy, artificial intelligence generate content (AIGC) has emerge. AIGC use artificial intalligence to assist or replace manual content generation by generating content based on userinputted keywords or requirements. '''},
                    {"role": "assistant", "content": '''
/英译中:
为了应对数字经济中的数字智能挑战，人工智能生成内容（AIGC）已经涌现。AIGC利用人工智能来辅助或取代人工内容生成，通过基于用户输入的关键词或需求来生成内容。

/英文中的修改建议：
"digital intelligance" 应改为 "digital intelligence"
"intalligence" 应改为 "intelligence"
"userinputted" 应改为 "user-inputted"
"has emerge." 应改为 "has emerged"

/修改后的英文句子：
To address the challenges of digital intelligence in the digital economy, artificial intelligence generated content (AIGC) has emerged. AIGC uses artificial intelligence to assist or replace manual content generation by generating content based on user-inputted keywords or requirements. '''},
                    {"role": "user", "content": '''vector database'''},
                    {"role": "assistant", "content": '''
Vector Database（矢量数据库）

/释义:
矢量数据库是一种地理信息系统（GIS）数据库，用于存储、管理和查询地理空间数据中的矢量数据。矢量数据是由点、线和多边形组成的地理要素，用以表示现实世界中的地理位置、形状和属性。

/相关信息:
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
        
        except Exception as e:
            print(f"DEBUG: {dynamic_model} prompt length: {len(prompt.split())} ERROR: {e}")
            continue
    return 

def chat_gpt_chinese(prompt):
    if not prompt: return

    for dynamic_model in ['gpt-3.5-turbo']:
        # Load your API key from an environment variable or secret management service
        openai.api_key = openai_key
        try:
            if debug: print(f"DEBUG: {dynamic_model} chat_gpt_chinese length: {len(prompt.split())} 正在创作...")
            response = openai.ChatCompletion.create(
                model=dynamic_model,
                messages=[
                    {"role": "system", "content": chinese_system_prompt},
                    {"role": "user", "content": chinese_user_prompt},
                    {"role": "assistant", "content": chinese_assistant_prompt},
                    {"role": "user", "content": '矢量数据库技术一直在不断改进，为客户提供更佳的性能和更个性化的用户体验。'},
                    {"role": "assistant", "content": '/中译英:\nVector database technology has continued to improve, offering better performance and more personalized user experiences for customers.'},
                    {"role": "user", "content": prompt}
                    ]
                )
            reply = response['choices'][0]['message']['content']
            reply = reply.strip('\n').strip()
            return reply
        
        except Exception as e:
            print(f"DEBUG: {dynamic_model} prompt length: {len(prompt.split())} ERROR: {e}")
            continue
    return 

def create_midjourney_prompt(prompt):

    system_prompt = midjourney_prompt_fomula if 'fomula' in prompt else midjourney_prompt_1
    prompt = prompt.replace('full', '').strip()

    try:
        message = chat_gpt_full(prompt, system_prompt, midjourney_user_prompt_fomula, midjourney_assistant_prompt_fomula,
                                dynamic_model='gpt-3.5-turbo', chatgpt_key=openai_key)
    except Exception as e:
        print(f"ERROR: create_midjourney_prompt() failed with error: \n{e}")
        return

    return message

if __name__ == '__main__':
    print(f"c101variables is running...")
