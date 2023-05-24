# -*- coding: utf-8 -*-

debug = True
place_holder = True
if place_holder:
    import os, re, json, base64, hashlib, math, string, time, uuid, time, urllib, imaplib, email, random, requests, chardet, subprocess, xlrd, pytz
    import azure.cognitiveservices.speech as speechsdk
    from pydub import AudioSegment
    from sqlalchemy import DateTime, Table, create_engine, insert, update, Column, Integer, String, Text, Float, text, Boolean, exists, inspect
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

    from eth_account import Account
    from mnemonic import Mnemonic
    from web3 import Web3, EthereumTesterProvider
    from moralis import evm_api
    from logging_util import logging

    from dotenv import load_dotenv

    # if debug: print(f"DEBUG: engine: {engine}")




if __name__ == '__main__':
    print(f"TELEGRAM_BOT initialing for {TELEGRAM_USERNAME}...")

    make_a_choise = input(f"这是系统从镜像 IMAGE 文件启动后的首次初始化还是代码更新后的初始化？\n首次初始化要输入 'first_time_initiate'; \n代码更新后的初始化请直接按回车键: ")
    is_first_time_initiate = True if make_a_choise == 'first_time_initiate' else False

    print(f"\nSTEP 1: 创建所有数据库表单 ...")
    with Session() as session: Base.metadata.create_all(bind=engine)

    print(f"\nSTEP 2: 清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表 ...")
    if is_first_time_initiate:
        confirm = input(f"确认要清空 ChatHistory, EthWallet, CryptoPayment, UserPriority, SystemPrompt, DialogueTone 表吗？请输入 'yes' 确认: ")
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

    print(f"\nSTEP 5: 将 System Prompt 写入数据库表单 ...")
    insert_system_prompt_from_file(file_path='files/system_prompt.txt')

    print(f"\nSTEP 6: 读取并打印出 System Prompt ...")
    system_prompt = get_system_prompt()
    print(f"System Prompt: \n\n{system_prompt}")

    print(f"\nSTEP 7: 将 Dialogue Tone 写入数据库表单 ...")
    # 读取 files/dialogue_tone.xls 并插入到 avatar_dialogue_tone 表中
    insert_dialogue_tone_from_file(file_path='files/dialogue_tone.xls')

    print(f"\nSTEP 8: 读取并打印出 Dialogue Tone ...")
    msg_history = get_dialogue_tone()
    # print msg_history in json format indented
    print(json.dumps(msg_history, indent=2, ensure_ascii=False))

    print(f"\nSTEP 9: 测试生成 eth address ...")
    user_from_id='2118900665'
    address = generate_eth_address(user_from_id)
    print(f"{user_from_id} ETH Address: {address}")

    print(f"\nSTEP 10: 初始化用户状态列表 ...")
    initialize_user_priority_table()

    print(f"\nTELEGRAM_BOT initialing for {TELEGRAM_USERNAME} finished!")
