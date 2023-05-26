from src.bot.bot_branch.bot_branch import BotBranch
from src.utils.utils import *
from src.utils.logging_util import logging


# 从 Coinmarketcap 给定 token 的价格等数据, 返回一个字典
def get_token_info_from_coinmarketcap(token_symbol):
    # CoinMarketCap API endpoint
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={token_symbol}'

    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': Params().CMC_PA_API}

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data:
        token_data = data['data']
        token_info = token_data[token_symbol]
        return token_info
    return


# 从 Coinmarketcap 查询给定 token 的 cmc_rank、price、market_cap、volume_24h、
# percent_change_24h、market_cap、fully_diluted_market_cap、circulating_supply、total_supply、last_updated 等数据, 返回一个字典
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


# Check if a given symbol is in CmcTotalSupply : db_cmc_total_supply's symbol column, if yes, return True,
# else return False
def check_token_symbol_in_db_cmc_total_supply(token_symbol):
    print(f"DEBUG: check_token_symbol_in_db_cmc_total_supply()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'db_cmc_total_supply' to check if the token_symbol exists
        token_symbol_exists = session.query(sqlalchemy.exists().where(CmcTotalSupply.symbol == token_symbol)).scalar()
        return token_symbol_exists


class CoinMarketCapBranch(BotBranch):
    def __init__(self, *args, **kwargs):
        super(CoinMarketCapBranch, self).__init__(*args, **kwargs)

    def handle_single_msg(self, msg, bot):
        msg_text = msg.msg_text.replace('/', '').upper()
        r = check_token_symbol_in_db_cmc_total_supply(msg_text)
        if not r: return
        try:
            r = get_token_info_from_coinmarketcap_output_chinese(msg_text)
            bot.send_msg(r, msg.chat_id)
        except Exception as e:
            logging.error(
                f"local_bot_msg_command() get_token_info_from_coinmarketcap_output_chinese() FAILED: \n\n{e}")
        return
