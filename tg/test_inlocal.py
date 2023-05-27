# from moralis import evm_api
import requests, json, pytz
from datetime import datetime


api_key = "oYa3si8DJ41gaQWoggoNEfEQ5lrmuRTTodYUi7NpMiu8q73cfeo5XwHGS5CVuxLX"
TELEGRAM_BOT_RUNNING = '5808241965:AAFGxm4xAGeAndPj2l_E-raK7W8qN7c0Fw0'
telegram_base_url = "https://api.telegram.org/bot" + TELEGRAM_BOT_RUNNING + "/"   
chat_id = "2118900665"
ETHERSCAN_WALLET_URL_PREFIX = 'https://etherscan.io/address/'
ETHERSCAN_TX_URL_PREFIX = 'https://etherscan.io/tx/'
ETHERSCAN_TOKEN_URL_PREFIX = 'https://etherscan.io/token/'
USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
USDT_ERC20_DECIMALS = 6

USDC_ERC20 = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
USDC_ERC20_DECIMALS = 6
FINNHUB_API='cb2o472ad3i3uh8vhpng'

def send_msg(message, chat_id, parse_mode='', base_url=telegram_base_url):
    if not message: return
    if not chat_id: return print(f"DEBUG: no chat_id, noly print:\n\n{message}")

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

