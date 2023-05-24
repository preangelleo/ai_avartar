# -*- coding: utf-8 -*-

debug = True
place_holder = True
if place_holder:
    import os, re, json, base64, hashlib, math, string, time, uuid, time, urllib, imaplib, email, random, requests, \
        chardet, subprocess, xlrd, pytz
    import azure.cognitiveservices.speech as speechsdk
    from pydub import AudioSegment
    from sqlalchemy import DateTime, Table, create_engine, insert, update, Column, Integer, String, Text, Float, text, \
        Boolean, exists, inspect
    from sqlalchemy.orm import declarative_base, Session
    from sqlalchemy.schema import MetaData
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func, exists, and_, or_, not_, select

    from datetime import datetime, timedelta, date
    from urllib.parse import urlencode
    from langdetect import detect
    import pandas as pd
    import openai, replicate

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
    from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredPowerPointLoader, \
        UnstructuredWordDocumentLoader, UnstructuredURLLoader
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

    from eth_account import Account
    from mnemonic import Mnemonic
    from web3 import Web3, EthereumTesterProvider
    from moralis import evm_api
    from logging_util import logging

    from dotenv import load_dotenv

    load_dotenv()

    # 获取环境变量
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    INFURA_KEY = os.getenv('INFURA_KEY')
    DEBANK_API = os.getenv('DEBANK_API')
    CMC_PA_API = os.getenv('CMC_PA_API')
    MORALIS_API = os.getenv('MORALIS_API')
    ETHERSCAN_API = os.getenv('ETHERSCAN_API')
    MONTHLY_FEE = float(os.getenv('MONTHLY_FEE'))
    BOTOWNER_CHAT_ID = os.getenv('BOTOWNER_CHAT_ID')
    BOTCREATER_CHAT_ID = os.getenv('BOTCREATER_CHAT_ID')
    ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
    USER_AVATAR_NAME = os.getenv('USER_AVATAR_NAME')
    BOT_USERNAME = os.getenv('BOT_USERNAME')

    BOT_OWNER_LIST = [BOTOWNER_CHAT_ID, BOTCREATER_CHAT_ID]

    INFURA = "https://mainnet.infura.io/v3/" + INFURA_KEY
    web3 = Web3(Web3.HTTPProvider(INFURA))

    USER_TELEGRAM_LINK = os.getenv("USER_TELEGRAM_LINK")
    TELEGRAM_USERNAME = USER_TELEGRAM_LINK.split('/')[-1]

    ETH_REGEX = r'0x[a-fA-F0-9]{40}'
    TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
    EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    USDT_ERC20_DECIMALS = 6

    USDC_ERC20 = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    USDC_ERC20_DECIMALS = 6

    REFILL_TEASER = "亲爱的, 该交公粮咯, 不过现在我们也还没分手, 所以你还可以继续用我, 就像其他免费用户一样; 如果想要我继续为你贴身服务, 请点击 /pay 获得独享的充值地址, 并根据提示交完公粮哈, 交了公粮我就又可以一心一意服侍你啦 😘, 放心, 活好不粘人哦... 🙈"

    # 连接本地数据库
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', pool_pre_ping=True)
    # if debug: print(f"DEBUG: engine: {engine}")
    metadata = MetaData()
    Session = sessionmaker(bind=engine)
    Base = declarative_base()


    # Define the table 'avatar_chat_history'
    class ChatHistory(Base):
        __tablename__ = 'avatar_chat_history'

        id = Column(Integer, primary_key=True, autoincrement=True)
        first_name = Column(String(255))
        last_name = Column(String(255))
        username = Column(String(255))
        from_id = Column(String(255))
        chat_id = Column(String(255))
        update_time = Column(DateTime)
        msg_text = Column(Text)
        black_list = Column(Integer, default=0)


    # Define the table 'avatar_owner_parameters'
    class OwnerParameter(Base):
        __tablename__ = 'avatar_owner_parameters'

        id = Column(Integer, primary_key=True, autoincrement=True)
        parameter_name = Column(String(255))
        parameter_value = Column(String(255))
        update_time = Column(DateTime)


    # Define the table 'avatar_system_prompt', id is the primary key autoincrement, INT; system_prompt is the TEXT, update_time is the DateTime
    class SystemPrompt(Base):
        __tablename__ = 'avatar_system_prompt'

        id = Column(Integer, primary_key=True, autoincrement=True)
        system_prompt = Column(Text)
        update_time = Column(DateTime)


    # Define the table 'avatar_dialogue_tone', `id` is the primary key autoincrement, INT; `tone_id` is INT,`role` Column(String(255)), `content` TEXT, update_time is the DateTime
    class DialogueTone(Base):
        __tablename__ = 'avatar_dialogue_tone'

        id = Column(Integer, primary_key=True, autoincrement=True)
        tone_id = Column(Integer)
        role = Column(String(255))
        content = Column(Text)
        update_time = Column(DateTime)


    # Define the table 'avatar_eth_wallet', `id` is the primary key autoincrement, INT; `address` is TEXT, `private_key` is TEXT, `user_from_id` is varchar(255), `create_time` is DateTime
    class EthWallet(Base):
        __tablename__ = 'avatar_eth_wallet'

        id = Column(Integer, primary_key=True, autoincrement=True)
        address = Column(Text)
        private_key = Column(Text)
        user_from_id = Column(String(255))
        create_time = Column(DateTime)


    # Define the table 'avatar_crypto_payments', `id` is the primary key autoincrement, INT; `user_from_id` is varchar(255), `address` is varchar(255), `usdt_paid_in` is FLOAT, `usdc_paid_in` is FLOAT, `eth_paid_in` is FLOAT, `update_time` is DateTime, `Hash_id` is TEXT
    class CryptoPayments(Base):
        __tablename__ = 'avatar_crypto_payments'

        id = Column(Integer, primary_key=True, autoincrement=True)
        user_from_id = Column(String(255))
        address = Column(String(255))
        usdt_paid_in = Column(Float, default=0)
        usdc_paid_in = Column(Float, default=0)
        eth_paid_in = Column(Float, default=0)
        update_time = Column(DateTime)
        Hash_id = Column(Text)


    # Define the table `avatar_user_priority`, `id` is the primary key autoincrement, INT; `user_from_id` is varchar(255), `priority` is TINYINT, `is_blacklist` is TINYINT, `free_until` is DateTime, `is_admin` is TINYINT, `is_owner` is TINYINT, `is_vip` is TINYINT, `is_paid` is TINYINT, `is_active` is TINYINT, `is_deleted` is TINYINT, `update_time` is DateTime, `next_payment_time` is DateTime, all the default value is 0; make sure user_from_id can not be duplicated, need to be unique
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


    '''mysql> DESCRIBE db_cmc_total_supply;
    +-----------------------+---------------+------+-----+---------+-------+
    | Field                 | Type          | Null | Key | Default | Extra |
    +-----------------------+---------------+------+-----+---------+-------+
    | symbol                | varchar(20)   | NO   | PRI | NULL    |       |
    | name                  | text          | YES  |     | NULL    |       |
    | cmc_rank              | double        | YES  |     | NULL    |       |
    | price                 | double        | YES  |     | NULL    |       |
    | max_supply            | double        | YES  |     | NULL    |       |
    | circulating_supply    | double        | YES  |     | NULL    |       |
    | total_supply          | double        | YES  |     | NULL    |       |
    | circulating_cap       | double        | YES  |     | NULL    |       |
    | fdm_cap               | double        | YES  |     | NULL    |       |
    | platform              | text          | YES  |     | NULL    |       |
    | token_address         | text          | YES  |     | NULL    |       |
    | date_added            | datetime      | YES  |     | NULL    |       |
    | last_updated          | datetime      | YES  |     | NULL    |       |
    | is_fiat               | bigint        | YES  |     | NULL    |       |
    | first_historical_data | datetime      | YES  |     | NULL    |       |
    | is_deleted            | bigint        | YES  |     | NULL    |       |
    | bep_token_address     | text          | YES  |     | NULL    |       |
    | tags                  | varchar(1000) | YES  |     | NULL    |       |
    | decimals              | int           | YES  |     | NULL    |       |
    | imple_address         | varchar(100)  | YES  |     | NULL    |       |
    | listed_in_binance     | tinyint       | YES  |     | 0       |       |
    | chain                 | varchar(10)   | YES  |     | NULL    |       |
    | token_abi             | blob          | YES  |     | NULL    |       |
    | in_1inch              | tinyint       | YES  |     | 0       |       |
    | in_mylist             | tinyint       | YES  |     | 0       |       |
    | in_blacklist          | tinyint       | YES  |     | 0       |       |
    | in_alertlist          | tinyint       | YES  |     | 0       |       |
    +-----------------------+---------------+------+-----+---------+-------+
    27 rows in set (0.00 sec)
    '''


    # define the bable 'db_cmc_total_supply'
    class CmcTotalSupply(Base):
        __tablename__ = 'db_cmc_total_supply'

        symbol = Column(String(20), primary_key=True)
        name = Column(Text)
        cmc_rank = Column(Float)
        price = Column(Float)
        max_supply = Column(Float)
        circulating_supply = Column(Float)
        total_supply = Column(Float)
        circulating_cap = Column(Float)
        fdm_cap = Column(Float)
        platform = Column(Text)
        token_address = Column(Text)
        date_added = Column(DateTime)
        last_updated = Column(DateTime)
        is_fiat = Column(Float)
        first_historical_data = Column(DateTime)
        is_deleted = Column(Float)
        bep_token_address = Column(Text)
        tags = Column(String(1000))
        decimals = Column(Integer)
        imple_address = Column(String(100))
        listed_in_binance = Column(Integer)
        chain = Column(String(10))
        token_abi = Column(Text)
        in_1inch = Column(Integer)
        in_mylist = Column(Integer)
        in_blacklist = Column(Integer)
        in_alertlist = Column(Integer)


    '''mysql> DESCRIBE db_daily_words;
    +----------------------+--------------+------+-----+---------+----------------+
    | Field                | Type         | Null | Key | Default | Extra          |
    +----------------------+--------------+------+-----+---------+----------------+
    | id                   | int unsigned | NO   | PRI | NULL    | auto_increment |
    | word                 | varchar(20)  | NO   |     | NULL    |                |
    | rank                 | int unsigned | YES  |     | NULL    |                |
    | counts               | int unsigned | NO   |     | 0       |                |
    | total_counts         | int unsigned | NO   |     | 0       |                |
    | us-phonetic          | varchar(100) | YES  |     | NULL    |                |
    | origin               | text         | YES  |     | NULL    |                |
    | synonyms             | text         | YES  |     | NULL    |                |
    | antonyms             | text         | YES  |     | NULL    |                |
    | tag                  | varchar(100) | YES  |     | NULL    |                |
    | chinese              | text         | YES  |     | NULL    |                |
    | chat_gpt_explanation | text         | YES  |     | NULL    |                |
    | note                 | text         | YES  |     | NULL    |                |
    | memo                 | text         | YES  |     | NULL    |                |
    | toefl                | tinyint      | NO   |     | 0       |                |
    | gre                  | tinyint      | NO   |     | 0       |                |
    | gmat                 | tinyint      | NO   |     | 0       |                |
    | sat                  | tinyint      | NO   |     | 0       |                |
    | scenario             | text         | YES  |     | NULL    |                |
    | mastered             | tinyint      | NO   |     | 0       |                |
    | level                | tinyint      | NO   |     | 0       |                |
    | sentence             | text         | YES  |     | NULL    |                |
    | last_check_time      | datetime     | YES  |     | NULL    |                |
    | youdao_synced        | tinyint      | NO   |     | 0       |                |
    | manually_updated     | tinyint      | NO   |     | 0       |                |
    | derivative           | text         | YES  |     | NULL    |                |
    | relevant             | text         | YES  |     | NULL    |                |
    | phrase               | text         | YES  |     | NULL    |                |
    | sealed               | tinyint      | NO   |     | 0       |                |
    +----------------------+--------------+------+-----+---------+----------------+
    29 rows in set (0.00 sec)
    '''


    # define the table 'db_daily_words'
    class DailyWords(Base):
        __tablename__ = 'db_daily_words'

        id = Column(Integer, primary_key=True, autoincrement=True)
        word = Column(String(20))
        rank = Column(Integer)
        counts = Column(Integer)
        total_counts = Column(Integer)
        us_phonetic = Column(String(100))
        origin = Column(Text)
        synonyms = Column(Text)
        antonyms = Column(Text)
        tag = Column(String(100))
        chinese = Column(Text)
        chat_gpt_explanation = Column(Text)
        note = Column(Text)
        memo = Column(Text)
        toefl = Column(Integer)
        gre = Column(Integer)
        gmat = Column(Integer)
        sat = Column(Integer)
        scenario = Column(Text)
        mastered = Column(Integer)
        level = Column(Integer)
        sentence = Column(Text)
        last_check_time = Column(DateTime)
        youdao_synced = Column(Integer)
        manually_updated = Column(Integer)
        derivative = Column(Text)
        relevant = Column(Text)
        phrase = Column(Text)
        sealed = Column(Integer)


    # 定义一个 GptEnglishExplanation 表, id 是主键, autoincrement, INT; word 是 varchar(20), explanation 是 TEXT, gpt_model 是 varchar(30), update_time 是 DateTime
    class GptEnglishExplanation(Base):
        __tablename__ = 'gpt_english_explanation'

        id = Column(Integer, primary_key=True, autoincrement=True)
        word = Column(String(30))
        explanation = Column(Text)
        gpt_model = Column(String(30))
        update_time = Column(DateTime)


    # 定义一个 GptStory 表, id 是主键, autoincrement, INT; prompt 是 TEXT, title 是 varchar(255), story 是 TEXT, gpt_model 是 varchar(30), from_id 是 varchar(30), chat_id 是 varchar(30), update_time 是 DateTime
    class GptStory(Base):
        __tablename__ = 'gpt_story'

        id = Column(Integer, primary_key=True, autoincrement=True)
        prompt = Column(Text)
        title = Column(Text)
        story = Column(Text)
        gpt_model = Column(String(30))
        from_id = Column(String(255))
        chat_id = Column(String(255))
        update_time = Column(DateTime)


    '''定义 ElevenLabsUser 表,
    from_id, string
    user_title, string
    elevenlabs_api_key, string
    voice_id string # 字符化的 dict
    last_time_voice_id, string
    original_voice_filepath, sting
    test_count, tinyint
    '''


    class ElevenLabsUser(Base):
        __tablename__ = 'elevenlabs_user'

        id = Column(Integer, primary_key=True, autoincrement=True)
        from_id = Column(String(255))
        user_title = Column(String(255))
        elevenlabs_api_key = Column(String(255))
        voice_id = Column(Text)
        last_time_voice_id = Column(String(255))
        original_voice_filepath = Column(String(255))
        test_count = Column(Integer, default=0)
        ready_to_clone = Column(Integer, default=0)


    class BaseRetriever(ABC):
        @abstractmethod
        def get_relevant_documents(self, query: str) -> List[Document]:
            """Get texts relevant for a query.

            Args:
                query: string to find relevant texts for

            Returns:
                List of relevant documents
            """


# def update avatar_user_priority table, input include (from_id, which_key='', key_value='', update_time=datetime.now()), check if the from_id exists, if exists then update the key_value, if not exists then insert the from_id and key_value
def update_user_priority(from_id, which_key='', key_value='', update_time=datetime.now()):
    if debug: print(f"DEBUG: update_user_priority()")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: insert_from_id_to_user_priority_table(): {from_id}")

    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: set_user_as_vip(): {from_id}")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: remove_user_from_vip_list(): {from_id}")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: get_vip_list_except_owner_and_admin()")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: set_user_blacklist()")
    try:
        return update_user_priority(from_id, 'is_blacklist', 1)
    except:
        return False


# Use update_user_priority() function to remove a from_id from bliacklist
def remove_user_blacklist(from_id):
    if debug: print(f"DEBUG: remove_user_blacklist()")
    try:
        return update_user_priority(from_id, 'is_blacklist', 0)
    except:
        return False


# initiate the avatar_user_priority table, set BOT_OWNER_ID as the owner, set BOT_OWNER_ID as the admin, set BOT_OWNER_ID as the vip, set BOT_OWNER_ID as the paid, set BOT_OWNER_ID as the active, set BOT_OWNER_ID as the deleted, set BOT_OWNER_ID as the priority 100, set BOT_OWNER_ID as the free_until 2099-12-31 23:59:59
def initialize_user_priority_table():
    if debug: print(f"DEBUG: initialize_user_priority_table()")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: initialize_owner_parameters_table()")

    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: update_owner_parameter()")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: get_owner_parameters()")
    # Create a new session
    with Session() as session:
        # Query the table 'avatar_owner_parameters'
        owner_parameters = session.query(OwnerParameter).all()
        # Create a new empty dictionary
        owner_parameters_dict = {}
        # Loop through the owner_parameters and add them into the dictionary
        for owner_parameter in owner_parameters: owner_parameters_dict[
            owner_parameter.parameter_name] = owner_parameter.parameter_value
    return owner_parameters_dict


def insert_system_prompt(system_prompt):
    if debug: print(f"DEBUG: insert_system_prompt()")
    # Create a new session
    with Session() as session:
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
    with Session() as session:
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
    if debug: print(f"DEBUG: insert_dialogue_tone_from_file()")

    # Read the dialogue_tone.xls file
    df = pd.read_excel(file_path, header=None, names=['role', 'content'])
    df = df.dropna()

    # Create a new session
    with Session() as session:
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
    with Session() as session:
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
    if debug: print(f"DEBUG: generate_eth_address_qrcode()")
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
    with Session() as session:
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
    with Session() as session:
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
    if debug: print(f"DEBUG: get_from_id_by_eth_address()")
    # Create a new session
    with Session() as session:
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
    if debug: print(f"DEBUG: check_token_symbol_in_db_cmc_total_supply()")
    # Create a new session
    with Session() as session:
        # Query the table 'db_cmc_total_supply' to check if the token_symbol exists
        token_symbol_exists = session.query(exists().where(CmcTotalSupply.symbol == token_symbol)).scalar()
        return token_symbol_exists


# 用 Pandas 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息并放入 df
def get_token_info_from_db_cmc_total_supply(token_address):
    if debug: print(f"DEBUG: get_token_info_from_db_cmc_total_supply()")
    # Create a new session
    with Session() as session:
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
    with Session() as session:
        Base.metadata.create_all(bind=engine)

    print(f"\nSTEP 2: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ...")
    if is_first_time_initiate:
        confirm = input(
            f"确认要清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表吗？请输入 'yes' 确认: ")
        if confirm == 'yes':
            with Session() as session:
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