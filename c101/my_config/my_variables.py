import base64
import email
import hashlib
import hmac
import imaplib
import io
import json
import math
import os
import pickle
import random
import re
import socket
import string
import struct
import sys
import time
import urllib
import uuid
from collections import Counter
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode, urljoin
from urllib.request import urlretrieve
import boto3
import chardet
import openai
import pandas as pd
import pytz
import requests
import streamlit as st
import streamlit_authenticator as stauth
import whisper
import replicate
import yaml
from yaml import SafeLoader
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect
from matplotlib import pyplot as plt
from PIL import Image
from requests import Session, get
from requests_oauthlib import OAuth1Session
from sqlalchemy import create_engine, MetaData, Table, DateTime, insert, update
from sqlalchemy.orm import sessionmaker
from uniswap import Uniswap
from web3 import Web3
from web3.types import Timestamp
from ecdsa.curves import SECP256k1
from qrcode import constants
from ens import ENS
from googletrans import Translator
from snscrape.modules.twitter import Tweet
import finnhub
import ccxt
import tweepy
import pytesseract
import pyotp
import numpy as np
import mplfinance as mpf
from cryptography.fernet import Fernet
from base58 import b58encode_check
from mnemonic import Mnemonic
import struct
import pickle
import pytz
import imaplib
import email

PRIVATE_TERM_LIST = ['private', 'privately', 'secret', 'secretly', 'p', 's', '-p', '-s']

COINMARKETCAP_API = '1a2148f7-23d0-4028-8948-11e7cca71ebb'
# CMC PA API
CMC_PA_API = 'bbac788f-ab81-41c8-88f5-bd930b14f886'
BSCSCAN_API = 'TEGJRNWNWRWT2RP19USPGTH57DYPU8J2CW'
FINNHUB_API ='cb2o472ad3i3uh8vhpng'
ETHERSCAN_API = 'NFPJHR4T6UFT6ENWPAAZI6489V4PS73221'

MORALIS_API = 'oYa3si8DJ41gaQWoggoNEfEQ5lrmuRTTodYUi7NpMiu8q73cfeo5XwHGS5CVuxLX'
MORALIS_ID = '4aeb95005e52ca251121e7af'
MORALIS_APP_ID = 'LuqQgGIT8g5KPSx7KcnWOJKQUxoFXkrIHdv2GFDQ'

WEB_SECRETKEY = 'c8a71460740cf8caad8fa44bb19f52b5'
OTP_KEY = 'G5DKABKM6M76XTOMA3C3T6QI2AJJYKVZ'
DEBANK_API = '66851eb001290da8bdc25434cb78c5bc495da2dd'

URLsafe_B64encode = 'xWADfWLMTKXQjLsvVU9HO-1NGlQMdFZFVxcl6eKBjPc='

GMAIL_NAME = 'laogegecoding@gmail.com'
GMAIL_LGG_APP_PASSWORD = 'xwalrdjyrpdntmmp'
GMAIL_LGG_APP_PASSWORD_IMAP = 'lcvodrwmyktydxif'

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

IGNORE_POSITIONS = ['USDT', 'BNB', 'NFT']
SPECIAL_CHARS = " .~!@#${%^&*()_+-*/<>},[]\/;?:'"

ONE_DAY_SECONDS = 60 * 60 * 24

SPLIT_LINE = '='*33

if __name__ == '__main__':
    print(f"my_variables.py is running...")