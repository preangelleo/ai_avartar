from tvariables import *

if place_holder:
    BINANCE_API = os.getenv('BINANCE_LTD_API_KEY')
    BINANCE_SECRET = os.getenv('BINANCE_LTD_API_SECRET')

    BINANCE_BASE_URL = 'https://api.binance.com'
    BINANCE_TICKER_URL = 'https://api.binance.com/api/v3/ticker/24hr'
    BINANCE_DEPOSIT_ADDRESS_FOR_ERC20 = '0x34B940120AEB9cadbCc4131fB034aD3B83B0367d'

    ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
    ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
    ETH_ADDRESS_STD = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    ETH_REGEX = r'0x[a-fA-F0-9]{40}'
    TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
    BTC_REGEX = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[bc1q|bc1p][0-9A-Za-z]{37,62}$'
    EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    IGNORE_LIST = ['BTC', 'ETH', 'XRP', 'AMB', 'LTC', 'ARB', 'BTS', 'SOL', 'JST', 'ADA', 'TRX', 'LUNA', 'LUNC', 'BCH', 'USTC', 'EOS', 'XMR', 'XLM', 'XEM', 'DOGE', 'AVAX', 'OP', 'MATIC', 'APT', 'COCOS', 'BTT', 'BTTT', 'BTTB', 'EUR', 'SUI']

    BINANCE_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'X-MBX-APIKEY': BINANCE_API,
        "Content-Type": "application/json"
        }

def network_name_change(str_name):
    str_name = str_name.upper()
    str_name = 'ETH' if str_name.startswith("ERC") else 'TRX' if str_name.startswith("TRC") else 'BSC' if str_name.startswith("BEP") else str_name
    return str_name

def server_time_diff():
    PATH = '/api/v1/time'
    params = None
    timestamp = int(time.time() * 1000)
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, params=params)
        data = r.json()
        diff = {timestamp - data['serverTime']}
        return diff
    except Exception as e:
        print(e)
        time.sleep(0.1)
        return
    
def get_listed_assets_info():
    PATH = '/sapi/v1/asset/assetDetail'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
        # df = pd.DataFrame(data)
        # return df.T
    except Exception as e:
        print(e)
        return
''' Return from get_listed_assets_info():
{
  "AGLD": {
    "withdrawFee": "13",
    "minWithdrawAmount": "26",
    "withdrawStatus": true,
    "depositStatus": true
  },
  "DGD": {
    "withdrawFee": "0.074",
    "minWithdrawAmount": "0.15",
    "withdrawStatus": true,
    "depositStatus": false,
    "depositTip": "Wallet Maintenance, Deposit Suspended"
  },
  "1INCHDOWN": {
    "withdrawFee": "0",
    "minWithdrawAmount": "0",
    "withdrawStatus": false,
    "depositStatus": false,
    "depositTip": "Not support deposit"
  },
  "COTI": {
    "withdrawFee": "86",
    "minWithdrawAmount": "172",
    "withdrawStatus": true,
    "depositStatus": true
  }
  ......
}
'''

# 查询用户API Key权限 (USER_DATA), 权重(IP): 1
# GET /sapi/v1/account/apiRestrictions (HMAC SHA256)
def get_api_functions():
    PATH = '/sapi/v1/account/apiRestrictions'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        print(e)
        return
'''return from get_api_functions():
{
  "ipRestrict": true,
  "createTime": 1665449424000,
  "enableSpotAndMarginTrading": true,
  "enableReading": true,
  "enableWithdrawals": true,
  "enableInternalTransfer": true,
  "permitsUniversalTransfer": true,
  "enableMargin": true,
  "enableFutures": true,
  "enableVanillaOptions": false
}
'''

# use get_api_fuction() resutl convert to string send to chat_id
def get_api_functions_str(chat_id):
    data = get_api_functions()
    if data: return send_msg('\n'.join([f'{key}: {value}' for key, value in data.items()]), chat_id, parse_mode='', base_url=telegram_base_url)
    else: return send_msg(f"You don't have a binance API key and secrets in database yet.", chat_id, parse_mode='', base_url=telegram_base_url)

# 账户API交易状态(USER_DATA), 获取 api 账户交易状态详情, 权重(IP): 1
# GET /sapi/v1/account/apiTradingStatus (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#api-user_data 
def get_api_status():
    PATH = '/sapi/v1/account/apiTradingStatus'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        print(e)
        return
''' return from get_api_status():
{
  "data": {
    "isLocked": false,
    "plannedRecoverTime": 0,
    "triggerCondition": {
      "UFR": 300,
      "IFER": 150,
      "GCR": 150
    },
    "updateTime": 0
  }
}'''


# 获取所有币信息 (USER_DATA), 获取针对用户的所有(Binance支持充提操作的)币种信息。权重(IP): 10
# GET /sapi/v1/capital/config/getall (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#system
def get_account_all():
    PATH = '/sapi/v1/capital/config/getall'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        return data
    except Exception as e:
        time.sleep(0.1)
        return 
''' return from get_account_all():
[
  {
    "coin": "AGLD",
    "depositAllEnable": true,
    "withdrawAllEnable": true,
    "name": "Adventure Gold",
    "free": "0",
    "locked": "0",
    "freeze": "0",
    "withdrawing": "0",
    "ipoing": "0",
    "ipoable": "0",
    "storage": "0",
    "isLegalMoney": false,
    "trading": true,
    "networkList": [
      {
        "network": "ETH",
        "coin": "AGLD",
        "entityTag": "main",
        "withdrawIntegerMultiple": "0.00000001",
        "isDefault": true,
        "depositEnable": true,
        "withdrawEnable": true,
        "depositDesc": "",
        "withdrawDesc": "",
        "specialTips": "",
        "specialWithdrawTips": "",
        "name": "Ethereum (ERC20)",
        "resetAddressStatus": false,
        "addressRegex": "^(0x)[0-9A-Fa-f]{40}$",
        "addressRule": "",
        "memoRegex": "",
        "withdrawFee": "13",
        "withdrawMin": "26",
        "withdrawMax": "9999999",
        "minConfirm": 12,
        "unLockConfirm": 64,
        "sameAddress": false,
        "estimatedArrivalTime": 5,
        "busy": false,
        "country": "AE,BINANCE_BAHRAIN_BSC,custody,KZ",
        "contractAddressUrl": "https://etherscan.io/token/",
        "contractAddress": "0x32353a6c91143bfd6c7d363b546e62a9a2489a20"
      }
    ]
  },
......
]'''

# from result of get_account_all(), check if a given coin is in the list, and the given network is in the list of the coin's networkList and withdrawEnable is True and check the withdrawFee, withdrawMin, withdrawMax, withdrawIntegerMultiple, and check the address is valid with addressRegex, return networkList
def check_coin_network(coin, network):
    coin = coin.upper()
    network = network.upper()
    data = get_account_all()
    if data:
        df = pd.DataFrame(data)
        df = df[df['coin'] == coin]
        if not df.empty:
            df_networkList = pd.DataFrame(df['networkList'].values[0])
            df_networkList = df_networkList[df_networkList['network'] == network]
            if not df_networkList.empty:
                df_networkList = df_networkList[df_networkList['withdrawEnable'] == True]
                if not df_networkList.empty: return df_networkList
''' return from check_coin_network('AGLD', 'eth'):
  network  coin entityTag withdrawIntegerMultiple  isDefault  depositEnable  withdrawEnable depositDesc withdrawDesc specialTips specialWithdrawTips              name  resetAddressStatus           addressRegex addressRule memoRegex withdrawFee withdrawMin withdrawMax  minConfirm  unLockConfirm  sameAddress  estimatedArrivalTime   busy                            country           contractAddressUrl                             contractAddress
0     ETH  AGLD      main              0.00000001       True           True            True                                                           Ethereum (ERC20)               False  ^(0x)[0-9A-Fa-f]{40}$                                13          26     9999999          12             64        False                     5  False  AE,BINANCE_BAHRAIN_BSC,custody,KZ  https://etherscan.io/token/  0x32353a6c91143bfd6c7d363b546e62a9a2489a20
'''

# 资金账户 (USER_DATA), 权重(IP): 1
# POST /sapi/v1/asset/get-funding-asset (HMAC SHA256)
# 目前仅支持查询以下业务资产：Binance Pay, Binance Card, Binance Gift Card, Stock Token
def get_funding_asset():
    PATH = '/sapi/v1/asset/get-funding-asset'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            return
        data = r.json()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(e)
        return
''' return from get_funding_asset():
  asset            free locked freeze withdrawing btcValuation
0   ENS               1      0      0           0            0
1   NFT  8077335.411327      0      0           0            0
2  USDT    100.00000051      0      0           0            0
'''


'''用户万向划转 (USER_DATA)
POST /sapi/v1/asset/transfer (HMAC SHA256)
权重(UID)): 900
参数:
名称	类型	是否必需	描述
type	ENUM	YES	
asset	STRING	YES	
amount	DECIMAL	YES	
fromSymbol	STRING	NO	
toSymbol	STRING	NO	
recvWindow	LONG	NO	
timestamp	LONG	YES
fromSymbol 必须要发送，当类型为 ISOLATEDMARGIN_MARGIN 和 ISOLATEDMARGIN_ISOLATEDMARGIN
toSymbol 必须要发送，当类型为 MARGIN_ISOLATEDMARGIN 和 ISOLATEDMARGIN_ISOLATEDMARGIN

目前支持的type划转类型:

MAIN_UMFUTURE 现货钱包转向U本位合约钱包
MAIN_CMFUTURE 现货钱包转向币本位合约钱包
MAIN_MARGIN 现货钱包转向杠杆全仓钱包
UMFUTURE_MAIN U本位合约钱包转向现货钱包
UMFUTURE_MARGIN U本位合约钱包转向杠杆全仓钱包
CMFUTURE_MAIN 币本位合约钱包转向现货钱包
MARGIN_MAIN 杠杆全仓钱包转向现货钱包
MARGIN_UMFUTURE 杠杆全仓钱包转向U本位合约钱包
MARGIN_CMFUTURE 杠杆全仓钱包转向币本位合约钱包
CMFUTURE_MARGIN 币本位合约钱包转向杠杆全仓钱包
ISOLATEDMARGIN_MARGIN 杠杆逐仓钱包转向杠杆全仓钱包
MARGIN_ISOLATEDMARGIN 杠杆全仓钱包转向杠杆逐仓钱包
ISOLATEDMARGIN_ISOLATEDMARGIN 杠杆逐仓钱包转向杠杆逐仓钱包
MAIN_FUNDING 现货钱包转向资金钱包
FUNDING_MAIN 资金钱包转向现货钱包
FUNDING_UMFUTURE 资金钱包转向U本位合约钱包
UMFUTURE_FUNDING U本位合约钱包转向资金钱包
MARGIN_FUNDING 杠杆全仓钱包转向资金钱包
FUNDING_MARGIN 资金钱包转向杠杆全仓钱包
FUNDING_CMFUTURE 资金钱包转向币本位合约钱包
CMFUTURE_FUNDING 币本位合约钱包转向资金钱包
MAIN_OPTION 现货钱包转向期权钱包
OPTION_MAIN 期权钱包转向现货钱包
UMFUTURE_OPTION U本位合约钱包转向期权钱包
OPTION_UMFUTURE 期权钱包转向U本位合约钱包
MARGIN_OPTION 杠杆全仓钱包转向期权钱包
OPTION_MARGIN 期权全仓钱包转向杠杆钱包
FUNDING_OPTION 资金钱包转向期权钱包
OPTION_FUNDING 期权钱包转向资金钱包
MAIN_PORTFOLIO_MARGIN 现货钱包转向统一账户钱包
PORTFOLIO_MARGIN_MAIN 统一账户钱包转向现货钱包
'''
# 定义 FUNDING_MAIN 资金钱包转向现货钱包功能
def funding_main_transfer(coin, amount):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': 'FUNDING_MAIN',
        'asset': coin.upper(),
        'amount': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        tranId = data['tranId']
        return tranId
    except Exception as e:
        print(e)
        return

# 通过用户input 的 coin 和 amount，调用 get_funding_asset() 获取 coin 的余额，如果余额大于 amount，则调用 funding_main_transfer(coin, amount) 转账
def funding_main_transfer_with_check_and_send(coin, amount, chat_id):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'转账失败，您输入的转账数量: {amount} 不是数字。', chat_id, parse_mode='', base_url=telegram_base_url)

    df = get_funding_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = funding_main_transfer(coin, amount)
                if tranId: return send_msg(f'已经成功将 {format_number(amount)} {coin} 从资金账户转入到现货账户, tranId: \n{tranId}', chat_id, parse_mode='', base_url=telegram_base_url)
            else: return send_msg(f'资金账户 {coin} 余额: {format_number(balance)} 小于转账数量: {format_number(amount)}', chat_id, parse_mode='', base_url=telegram_base_url)
        else: return send_msg(f'资金账户没有 {coin} 资产。', chat_id, parse_mode='', base_url=telegram_base_url)
    return send_msg(f'转账失败，可能是网络问题，请稍后再试。', chat_id, parse_mode='', base_url=telegram_base_url)

# 定义 MAIN_FUNDING 资金钱包转向现货钱包功能
def main_funding_transfer(coin, amount):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': 'MAIN_FUNDING',
        'asset': coin.upper(),
        'amount': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200: return
        data = r.json()
        tranId = data['tranId']
        return tranId
    except Exception as e:
        print(e)
        return

# 通过用户input 的 coin 和 amount，调用 get_user_asset() 获取 asset / coin 的余额，如果余额大于 amount，则调用 main_funding_transfer(coin, amount) 转账
def main_funding_transfer_with_check_and_send(coin, amount, chat_id):
    coin = coin.upper()
    try: amount = float(amount)
    except: return send_msg(f'转账失败，您输入的转账数量: {amount} 不是数字。', chat_id, parse_mode='', base_url=telegram_base_url)

    df = get_user_asset()
    if not df.empty:
        df = df[df['asset'] == coin]
        if not df.empty:
            balance = float(df['free'].values[0])
            if balance >= amount: 
                tranId = main_funding_transfer(coin, amount)
                if tranId: return send_msg(f'已经成功将 {format_number(amount)} {coin} 从现货账户转入到资金账户, tranId: \n{tranId}', chat_id, parse_mode='', base_url=telegram_base_url)
            else: return send_msg(f'现货账户 {coin} 余额: {format_number(balance)} 小于转账数量: {format_number(amount)}', chat_id, parse_mode='', base_url=telegram_base_url)
        else: return send_msg(f'现货账户没有 {coin} 资产。', chat_id, parse_mode='', base_url=telegram_base_url)
    return send_msg(f'转账失败，可能是网络问题，请稍后再试。', chat_id, parse_mode='', base_url=telegram_base_url)

# 通过 get_funding_asset 检查资金账户中的 USDT 余额，如果存在 USDT 余额，则调用 funding_main_transfer_with_check_and_send(coin, amount) 将所有 USDT 余额转入到现货账户
def funding_main_transfer_all_usdt(chat_id=BOTOWNER_CHAT_ID):
    df = get_funding_asset()
    if not df.empty:
        df = df[df['asset'] == 'USDT']
        if not df.empty:
            amount = float(df['free'].values[0])
            if amount > 0: return funding_main_transfer_with_check_and_send('USDT', amount, chat_id)


# 通过 get_funding_asset() 获取所有 coin 的余额并返回一个 dict key is asset, value is free
def get_coin_funding_balance_all():
    df = get_funding_asset()
    if not df.empty: 
        df = df[df['asset'] != 'NFT']
        return dict(zip(df['asset'].values, df['free'].values))
    else: return {}

# 通过 get_funding_asset() 获取某个 coin 的余额
def get_coin_funding_balance(coin):
    df = get_funding_asset()
    df = df[df['asset'] == coin.upper()]
    if not df.empty: return df['free'].values[0]
    else: return 0

# 币安统一账户查询, 用户持仓 (USER_DATA), 获取用户持仓, 仅返回>0的数据。权重(IP): 5
# POST /sapi/v3/asset/getUserAsset 
def get_user_asset():
    PATH = '/sapi/v3/asset/getUserAsset'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            print(r)
            return
        data = pd.DataFrame(r.json())
        return data
    except Exception as e:
        print(e)
        return
''' return from get_user_asset():
  asset           free locked freeze withdrawing ipoable btcValuation
0   BNB     3.28212843      0      0           0       0            0
1   BTC     0.00000232      0      0           0       0            0
2   ETH     0.00265824      0      0           0       0            0
3  LUNA    34.95886212      0      0           0       0            0
4   ONG      0.9774719      0      0           0       0            0
5  USDT  3203.81507667      0      0           0       0            0
'''

# 通过 get_user_asset() 获取所有 coin 的余额并返回一个 dict key is asset, value is free
def get_coin_wallet_balance_all():
    df = get_user_asset()
    if not df.empty: return dict(zip(df['asset'].values, df['free'].values))
    else: return {}

# 通过 get_user_asset() 获取某个 coin 的余额
def get_coin_wallet_balance(coin):
    df = get_user_asset()
    df = df[df['asset'] == coin.upper()]
    if not df.empty: return df['free'].values[0]
    else: return 0

# 获取币安全部交易对最新价格
def get_token_price_table():
    # Get ticker data
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'lastPrice']]
    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]
    df_ticker = df_ticker.reset_index(drop=True)
    # 增加一列, coin, coin = symbol[:-4]
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]
    return df_ticker
''' return from get_token_price_table():
        symbol     lastPrice   coin
0      BTCUSDT  27093.630000    BTC
1      ETHUSDT   1887.160000    ETH
2      BNBUSDT    306.300000    BNB
3      BCCUSDT      0.000000    BCC
4      NEOUSDT     10.510000    NEO
..         ...           ...    ...
444   PEPEUSDT      0.000001   PEPE
445  FLOKIUSDT      0.000032  FLOKI
446    ASTUSDT      0.121500    AST
447    SNTUSDT      0.023880    SNT
448  COMBOUSDT      1.501000  COMBO
'''

# 通过 df_ticker = pd.read_json(BINANCE_TICKER_URL) 获得最新的 ticker 信息
def binance_today_hot_coin(trading_volume_limit = 50_000_000):
    unique_coin_list = []
    # 读出 binance_ticker_top_30 中 的 openTime 在最近 30 天内的所有行 unique coin, 转换为 pandas df 并生成一个 unique_coin_list
    with engine.connect() as connection:
        # result = connection.execute(text('SELECT DISTINCT coin FROM binance_ticker_top_30 WHERE openTime > :openTime'), openTime=int(time.time() * 1000) - 30 * 24 * 60 * 60 * 1000)
        result = connection.execute(text('SELECT DISTINCT coin FROM binance_ticker_top_30 WHERE openTime > :openTime'), {'openTime': int(time.time() * 1000) - 30 * 24 * 60 * 60 * 1000})
        # 将 result 转换为 pandas df
        df = pd.DataFrame(result, columns=['coin'])
        # 将 df 转换为 list
        unique_coin_list = df['coin'].values.tolist()

    df_ticker = pd.read_json(BINANCE_TICKER_URL)

    # 保留 symbol, priceChangePercent, lastPrice, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime, closeTime
    df_ticker = df_ticker.loc[:, ['symbol', 'priceChangePercent', 'lastPrice', 'openPrice', 'highPrice', 'lowPrice', 'quoteVolume', 'openTime', 'closeTime']]

    # pick up the symbol endswith 'USDT'
    df_ticker = df_ticker[df_ticker['symbol'].str.endswith('USDT')]

    # 挑选出交易量最大而且 priceChangePercent 大于 0 以及交易量大于 5000w 的币
    df_ticker = df_ticker[(df_ticker['priceChangePercent'] > 0) & (df_ticker['quoteVolume'] > trading_volume_limit)]

    df_ticker = df_ticker.sort_values(by='quoteVolume', ascending=False)
    df_ticker['coin'] = df_ticker['symbol'].str[:-4]

    # 剔除 coin 包含 USD 的币
    df_ticker = df_ticker[~df_ticker['coin'].str.contains('USD')]

    # 剔除掉 IGNORE_LIST 中的币
    df_ticker = df_ticker[~df_ticker['coin'].isin(IGNORE_LIST)]

    df_ticker = df_ticker.head(30)

    # 剔除掉 unique_coin_list 中的币
    df_ticker = df_ticker[~df_ticker['coin'].isin(unique_coin_list)]
    if df_ticker.empty: return []

    #分析列表中的每一个 coin 的 token_info = get_token_market_cap_and_ratio(coin) token_info is None, 则剔除掉该行, 如果 token_info type is dict 则 df_ticker['market_cap'] = token_info['market_cap'] df_ticker['fully_diluted_market_cap'] = token_info['fully_diluted_market_cap'] df_ticker['ratio'] = token_info['ratio']
    df_ticker['market_cap'] = 0
    df_ticker['fully_diluted_market_cap'] = 0
    df_ticker['ratio'] = 0
    for index, row in df_ticker.iterrows():
        coin = row['coin']
        token_info = get_token_market_cap_and_ratio(coin)
        if token_info:
            df_ticker.loc[index, 'market_cap'] = token_info['market_cap']
            df_ticker.loc[index, 'fully_diluted_market_cap'] = token_info['fully_diluted_market_cap']
            df_ticker.loc[index, 'ratio'] = token_info['ratio']
        else:
            df_ticker.drop(index, inplace=True)

    if df_ticker.empty: return []

    df_ticker = df_ticker.reset_index(drop=True)

    # # 先删掉 binance_ticker_top_30
    # with engine.connect() as connection: connection.execute(text('DROP TABLE IF EXISTS binance_ticker_top_30'))

    update_id = 0
    # 如果 binance_ticker_top_30 存在，则读出最大的 update_id 值；如果不存在，则 update_id = 1
    with engine.connect() as connection:
        result = connection.execute(text('SELECT MAX(update_id) FROM binance_ticker_top_30'))
        for row in result: update_id = row[0]

    df_ticker['update_id'] = update_id + 1

    # append df_ticker to table 'binance_ticker_top_30', if not exit, create table
    df_ticker.to_sql('binance_ticker_top_30', con=engine, if_exists='append', index=False)

    # 读出 binance_ticker_top_30 中的 update_id = update_id + 1 的所有行, 赋值给 df_ticker
    with engine.connect() as connection: df_ticker = pd.read_sql(text('SELECT * FROM binance_ticker_top_30 WHERE update_id=:update_id'), connection, params={'update_id': update_id + 1})

    # create today_hot_coin_list
    today_hot_coin_list = df_ticker['coin'].values.tolist()

    return today_hot_coin_list
''' df_ticker
       symbol  priceChangePercent  lastPrice  openPrice  highPrice  lowPrice   quoteVolume       openTime      closeTime   coin    market_cap  fully_diluted_market_cap     ratio
0    LINAUSDT             -12.865   0.016858   0.019347   0.019950  0.016758  8.166821e+07  1685756785971  1685843185971   LINA  9.362306e+07              1.690495e+08  0.553820
1    PEPEUSDT               0.000   0.000001   0.000001   0.000001  0.000001  2.805064e+07  1685756783945  1685843183945   PEPE  4.987895e+08              5.355822e+08  0.931303
2    ARPAUSDT              -7.641   0.059110   0.064000   0.069590  0.057500  2.727382e+07  1685756784579  1685843184579   ARPA  7.361351e+07              1.184555e+08  0.621444
3   COMBOUSDT             -15.364   1.548000   1.829000   1.834000  1.475000  2.414374e+07  1685756779956  1685843179956  COMBO  1.137270e+08              1.600623e+08  0.710517
4     SXPUSDT               6.367   0.456100   0.428800   0.482900  0.428700  2.303637e+07  1685756786200  1685843186200    SXP  2.579746e+08              2.546665e+08  1.012990
5     CFXUSDT              -4.640   0.269200   0.282300   0.284400  0.265400  2.010361e+07  1685756786075  1685843186075    CFX  7.774646e+08              1.422788e+09  0.546437
6     EPXUSDT              21.801   0.000283   0.000232   0.000324  0.000231  1.886641e+07  1685756786279  1685843186279    EPX  1.903993e+07              3.780582e+07  0.503624
7    RNDRUSDT               2.284   2.597000   2.539000   2.638000  2.534000  1.811841e+07  1685756783529  1685843183529   RNDR  9.506594e+08              1.393014e+09  0.682448
8    SANDUSDT               0.053   0.567500   0.567200   0.582700  0.561600  1.635574e+07  1685756786288  1685843186288   SAND  1.053590e+09              1.705223e+09  0.617861
9     INJUSDT               0.744   7.854000   7.796000   8.172000  7.770000  1.550012e+07  1685756785581  1685843185581    INJ  6.309396e+08              7.886198e+08  0.800056
10    KEYUSDT              -7.082   0.007859   0.008458   0.008700  0.007800  1.543823e+07  1685756785128  1685843185128    KEY  4.179587e+07              4.727175e+07  0.884162
11    MTLUSDT               9.604   1.107000   1.010000   1.130000  1.009000  1.267358e+07  1685756785918  1685843185918    MTL  7.366251e+07              7.366251e+07  1.000000
12   MASKUSDT              -0.775   4.483000   4.518000   4.553000  4.407000  1.267285e+07  1685756780484  1685843180484   MASK  3.679589e+08              4.481156e+08  0.821125
13    FTMUSDT              -0.219   0.319200   0.319900   0.327000  0.317200  1.265156e+07  1685756783652  1685843183652    FTM  8.921519e+08              1.014947e+09  0.879014
14  MAGICUSDT              -2.043   1.006700   1.027700   1.059100  0.991300  1.207562e+07  1685756782567  1685843182567  MAGIC  2.177512e+08              3.501676e+08  0.621848
'''


# 通过 get_token_price_table() 获取某个 coin 的价格
def get_token_price(coin):
    df = get_token_price_table()
    df = df[df['coin'] == coin.upper()]
    if not df.empty: return df['lastPrice'].values[0]
    else: return 0
''' return from get_token_price('eth'):
1887.16
type: <class 'numpy.float64'>
'''


''' 获取充值历史(支持多网络) (USER_DATA), 权重(IP): 1
# GET /sapi/v1/capital/deposit/hisrec (HMAC SHA256)
参数:
名称	类型	是否必需	描述
coin	STRING	NO	
status	INT	NO	0(0:pending,6: credited but cannot withdraw,7=Wrong Deposit,8=Waiting User confirm,1:success)
startTime	LONG	NO	默认当前时间90天前的时间戳
endTime	LONG	NO	默认当前时间戳
offset	INT	NO	默认:0
limit	INT	NO	默认: 1000, 最大1000
recvWindow	LONG	NO	
timestamp	LONG	YES	
txId	STRING	NO
'''
# 获取给定 hours 小时内的充值记录并发送给 chat_id
def get_deposit_history_by_hours(chat_id, hours=1):
    hours = float(hours)
    PATH = '/sapi/v1/capital/deposit/hisrec'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'startTime': int(timestamp - 60*60*1000*hours),
        'endTime': timestamp,
        'limit': 1000
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)

    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.loc[:, ['coin', 'amount', 'address', 'txId', 'insertTime', 'status']]
            df = df.rename(columns={'coin': '提币名称', 'amount': '提币数量', 'address': '充值地址', 'txId': '链上哈希', 'insertTime': ' UTC时间', 'status': '充值状态'})
            for i in range(df.shape[0]):
                '''status (0:pending,6: credited but cannot withdraw,7=Wrong Deposit,8=Waiting User confirm,1:success)'''
                df.loc[i, '充值状态'] = 'pending' if df.loc[i, '充值状态'] == 0 else 'success' if df.loc[i, '充值状态'] == 1 else 'credited but cannot withdraw' if df.loc[i, '充值状态'] == 6 else 'Wrong Deposit' if df.loc[i, '充值状态'] == 7 else 'Waiting User confirm' if df.loc[i, '充值状态'] == 8 else 'unknown'
                df.loc[i, ' UTC时间'] = datetime.fromtimestamp(df.loc[i, ' UTC时间']/1000).strftime('%Y-%m-%d %H:%M:%S')
                # 将 df.loc[i] 转换成 dict
                df_dict = df.loc[i].to_dict()
                # 将 dict 转换成 str
                df_str = '\n'.join([f"{k}: {v}" for k, v in df_dict.items()])
                # 发送给 chat_id
                send_msg(df_str, chat_id, parse_mode='', base_url=telegram_base_url)
            return True
        # else: send_msg(f'No deposit history in the past {hours} hours.', chat_id, parse_mode='', base_url=telegram_base_url)
    return 


def get_deposit_history():
    PATH = '/sapi/v1/capital/deposit/hisrec'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty: 
            df_status_is_1 = df.loc[df['status']==1]
            if not df_status_is_1.empty: return df_status_is_1
    return
''' return from get_deposit_history():
                    id       amount  coin network  status                                     address addressTag                                               txId     insertTime  transferType confirmTimes  unlockConfirm  walletType
0  3384656949630549249        20950  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xb8a5941af952614b162323ee45c8b5a9471acb080443...  1679699675000             0        12/12             64           0
1  3367562419265538306  34.18681232   BTC     BTC       1          18a9tpwtVZsMUaU5cT2vYffo2vCFhwsop5             dd90460ca3d7d2817a1577180ab9ca0b707e9f0c4f72ef...  1678680762000             0          1/1              2           0
2  3364526220028378113        70000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xc8270959e315ca2e8c45dc90624854e971735fc24d88...  1678499790000             0        12/12             64           0
3  3364522261393931265        90000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x0fb0d5ec3cb4b7e71c52981d11b03b9c22e0ef228b67...  1678499554000             0        12/12             64           0
4  3364516246678109184        50000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x1a3981c917d413117ac7a5bfe5f71d6f24abe7028fa7...  1678499196000             0        12/12             64           0
5  3364514171839806464       150000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xa805da4d6c0dbe5ae4dbcedd522fd476e436d5f68abb...  1678499072000             0        12/12             64           0
6  3364506118323141633       130000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0xe06e748630f036e600a31db6756cb2c7769b62eaf542...  1678498592000             0        12/12             64           0
7  3364494037502884864       110000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x057559b3f99af4f8b8fdaa3a2da93a85f05845e6c629...  1678497872000             0        12/12             64           0
8  3364481977083722753       100000  USDT     ETH       1  0x34b940120aeb9cadbcc4131fb034ad3b83b0367d             0x79f101b1b102be0bd071a86b6fe06a1bc77e0011ae7a...  1678497153000             0        12/12             64           0
'''


'''获取提币历史 (支持多网络) (USER_DATA) 权重(IP): 1
GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
status = (0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
https://binance-docs.github.io/apidocs/spot/cn/#user_data-6
GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
参数:
名称	类型	是否必需	描述
coin	STRING	NO	
withdrawOrderId	STRING	NO	
status	INT	NO	0(0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
offset	INT	NO	
limit	INT	NO	默认: 1000, 最大, 1000
startTime	LONG	NO	默认当前时间90天前的时间戳
endTime	LONG	NO	默认当前时间戳
recvWindow	LONG	NO	
timestamp	LONG	YES
'''

# 获取给定 hours 小时内的提币记录并发送给 chat_id
def get_withdraw_history_by_hours(chat_id=BOTOWNER_CHAT_ID, hours=1):
    hours = float(hours)
    PATH = '/sapi/v1/capital/withdraw/history'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'startTime': int(timestamp - 60*60*1000*hours),
        'endTime': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty: 
            df = df.loc[:, ['coin', 'amount', 'address', 'txId', 'applyTime', 'status']]
            df = df.rename(columns={'coin': '提币名称', 'amount': '提币数量', 'address': '目标地址', 'txId': '链上哈希', 'applyTime': ' UTC时间', 'status': '提币状态'})
            for i in range(df.shape[0]):
                '''status = (0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成), 将 status 转换成中文'''
                df.loc[i, '提币状态'] = '已发送确认Email' if df.loc[i, '提币状态'] == 0 else '已被用户取消' if df.loc[i, '提币状态'] == 1 else '等待确认' if df.loc[i, '提币状态'] == 2 else '被拒绝' if df.loc[i, '提币状态'] == 3 else '处理中' if df.loc[i, '提币状态'] == 4 else '提现交易失败' if df.loc[i, '提币状态'] == 5 else '提现完成'
                # 将 df.loc[i] 转换成 dict
                df_dict = df.loc[i].to_dict()
                # 将 dict 转换成 str
                df_str = '\n'.join([f"{k}: {v}" for k, v in df_dict.items()])
                # 发送给 chat_id
                send_msg(df_str, chat_id, parse_mode='', base_url=telegram_base_url)
            return True
        # else: send_msg(f'No withdraw history in the past {hours} hours.', chat_id, parse_mode='', base_url=telegram_base_url)
    return
'''
                                 id amount transactionFee  coin  status                                     address                                               txId            applyTime network  transferType                                        info  confirmNo  walletType txKey         completeTime
0  47601e0a25c847e1ac4f3d55a0e42c9b     10              1  USDT       6          TGgqTRjJxTVCVq7QsxfjvKVhdUKM4yTmtP  6308c7dcd2f755a5784f39fa1de8b6b31c02fba39fb63a...  2023-06-04 17:25:40     TRX             0          TAzsQ9Gx8eqFNFSKbeXrbi45CuVPHzA8wr         50           0        2023-06-04 17:27:42
1  bd7e16c6d2a240e1b2f86b970f45a623     10           0.29  USDT       6  0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377  0xe19ad98e9f6ec2964a5de27eff46d0434282966b6929...  2023-06-03 22:10:54     BSC             0  0xa180fe01b906a1be37be6c534a3300785b20d947         20           0        2023-06-03 22:12:40'''

# 获取最近三个月的提币记录（默认）
def get_withdraw_history():
    PATH = '/sapi/v1/capital/withdraw/history'
    timestamp = int(time.time() * 1000)
    params = {'timestamp': timestamp}
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if not df.empty:
            df_status_is_6 = df.loc[df['status']==6]
            if not df_status_is_6.empty: return df_status_is_6
    return

'''提币 (USER_DATA)
Parameters:

Name	Type	Mandatory	Description
coin	STRING	YES	
withdrawOrderId	STRING	NO	client id for withdraw
network	STRING	NO	
address	STRING	YES	
addressTag	STRING	NO	Secondary address identifier for coins like XRP,XMR etc.
amount	DECIMAL	YES	
transactionFeeFlag	BOOLEAN	NO	When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
name	STRING	NO	Description of the address. Space in name should be encoded into %20.
walletType	INTEGER	NO	The wallet type for withdraw, 0-spot wallet, 1-funding wallet. Default walletType is the current "selected wallet" under wallet->Fiat and Spot/Funding->Deposit
recvWindow	LONG	NO	
timestamp	LONG	YES
'''
# Withdraw from binance to other address
def binance_withdraw(amount, network, coin, address):
    PATH = '/sapi/v1/capital/withdraw/apply'
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'address': address,
        'amount': amount,
        'network': network,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: return r.reason

''' return from binance_withdraw('eth', 0.1, '0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377'):
{
    "id":"7213fea8e94b4a5593d507237e5a555b"
}
'''

'''获取充值地址 (支持多网络) (USER_DATA)
GET /sapi/v1/capital/deposit/address (HMAC SHA256)
参数:
名称	类型	是否必需	描述
coin	STRING	YES	
network	STRING	NO	
recvWindow	LONG	NO	
timestamp	LONG	YES
'''

# 定义一个功能，获取给定 coin 给定 network 的充值地址
def get_coin_deposit_address(coin, network):
    PATH = '/sapi/v1/capital/deposit/address'
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'network': network,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: return r.reason
'''{'coin': 'USDT', 'address': '0x34b940120aeb9cadbcc4131fb034ad3b83b0367d', 'tag': '', 'url': 'https://etherscan.io/address/0x34b940120aeb9cadbcc4131fb034ad3b83b0367d'}'''

# get prepared for withdraw, check balance, check if target address is valid and convert to checksum address, check network is valid, make sure amount is float, make sure amount is not zero, make sure ballance is bigger than amount + fee and then call binance_withdraw() with prepared parameters
def binance_withdraw_prep_and_call(amount, network, coin, address):
    input_address = address
    coin = coin.upper()
    network = network_name_change(network)
    if network not in ['TRX', 'ETH', 'BTC', 'BSC']: return 'network: {} is not supported currently by this bot.'.format(network)

    df_network = check_coin_network(coin, network)
    if df_network is None: return 'network: {} is not valid for Coin: {}'.format(coin, network)

    withdrawFee = float(df_network['withdrawFee'].values[0])
    withdrawMin = float(df_network['withdrawMin'].values[0])
    withdrawMax = float(df_network['withdrawMax'].values[0])
    withdrawIntegerMultiple = float(df_network['withdrawIntegerMultiple'].values[0])
    addressRegex = df_network['addressRegex'].values[0]
    addressRegex = addressRegex.replace('(', '').replace(')', '')

    print(withdrawFee, withdrawMin, withdrawMax, withdrawIntegerMultiple, addressRegex)

    # extract valid network address from address using addressRegex
    address = re.findall(addressRegex, address)

    if not address: return f'Address: \n{input_address}\nis not valid for network: {network}'
    else: address = address[0]
    
    amount = float(amount) + withdrawFee

    if amount < withdrawMin: return f'Amount {amount} is smaller than withdrawMin: {withdrawMin}'
    if amount > withdrawMax: return f'Amount {amount} is bigger than withdrawMax: {withdrawMax}'
    
    # check balance
    df_balance = get_user_asset()
    df_balance = df_balance[df_balance['asset']==coin]
    if df_balance.empty: return 'No balance for coin: {}'.format(coin)

    balance = float(df_balance['free'].values[0])
    if balance < amount: return f'Balance {balance} is not enough for amount + fee: {amount}'

    print(amount, network, coin, address)

    return binance_withdraw(amount, network, coin, address)

def binance_today_hot_coins_check(chat_id=BOTOWNER_CHAT_ID, user_nick_name='亲爱的', crontab=False, trading_volume_limit = 50_000_000, check_size = 1000):
    today_hot_coin_list = binance_today_hot_coin(trading_volume_limit)
    if not today_hot_coin_list: 
        if not crontab: send_msg(f"{user_nick_name}, 今天币安没有热门币种, 你可以明天再来看看哦 😘", chat_id)
        return 

    query_list  = []
    for coin in today_hot_coin_list:
        
        token_info = get_token_info_from_coinmarketcap(coin)
        if not token_info: continue

        output_dict = {
            '名称': token_info['name'],
            '排名': token_info['cmc_rank'],
            '现价': f"{format_number(token_info['quote']['USD']['price'])} usd/{coin.lower()}",
            '交易量': f"{format_number(token_info['quote']['USD']['volume_24h'])} usd",
            '流通市值': f"{format_number(token_info['quote']['USD']['market_cap'])} usd | {token_info['circulating_supply'] / token_info['total_supply'] * 100:.1f}%",
            '24小时波动': f"{token_info['quote']['USD']['percent_change_24h']:.2f}%",
            '全流通市值': f"{format_number(token_info['quote']['USD']['fully_diluted_market_cap'])} usd",
            '代币总发行': f"{format_number(token_info['total_supply'])} {coin.lower()}",
            '本次更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # 用 '\n' join k: v
        output_dict_str = '\n'.join([f"{k}: {v}" for k, v in output_dict.items()])
        send_msg(output_dict_str, chat_id, parse_mode='', base_url=telegram_base_url)

        # 检查 binance_position_buy table 中 is_closed = 0 的 row 是否超过 10 个，如果没有超过 10 个则调用 binance_market_buy() 买入 1000 usdt
        df_balance = pd.read_sql_query('SELECT * FROM binance_position_buy WHERE is_closed = 0', engine)
        if df_balance.shape[0] < 10: 
            # 检查 coin 是否在 binance_position_buy table 中，如果不在则调用 binance_market_buy() 买入 1000 usdt
            if coin not in df_balance['coin'].values: send_msg(do_market_buy(coin, check_size), chat_id, parse_mode='', base_url=telegram_base_url)
        
        query_list.append(f"Latest news about crypto project: {token_info['name']} {coin}")

    for query in query_list:
        try: create_crypto_news_from_bing_search(query, chat_id, parse_mode='', base_url=telegram_base_url)
        except: pass

    return

'''
权重(UID): 1 权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
side	ENUM	YES	详见枚举定义：订单方向
type	ENUM	YES	详见枚举定义：订单类型
timeInForce	ENUM	NO	详见枚举定义：有效方式
quantity	DECIMAL	NO	
quoteOrderQty	DECIMAL	NO	
price	DECIMAL	NO	
newClientOrderId	STRING	NO	客户自定义的唯一订单ID。 如果未发送，则自动生成。
stopPrice	DECIMAL	NO	仅 STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT 和 TAKE_PROFIT_LIMIT 需要此参数。
trailingDelta	LONG	NO	用于 STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT 和 TAKE_PROFIT_LIMIT 类型的订单。更多追踪止盈止损订单细节, 请参考 追踪止盈止损(Trailing Stop)订单常见问题。
icebergQty	DECIMAL	NO	仅使用 LIMIT, STOP_LOSS_LIMIT, 和 TAKE_PROFIT_LIMIT 创建新的 iceberg 订单时需要此参数。
newOrderRespType	ENUM	NO	设置响应JSON。ACK，RESULT 或 FULL；MARKET 和 LIMIT 订单类型默认为 FULL，所有其他订单默认为 ACK。
selfTradePreventionMode	ENUM	NO	允许的 ENUM 取决于交易对的配置。支持的值有 EXPIRE_TAKER，EXPIRE_MAKER，EXPIRE_BOTH，NONE。
strategyId	INT	NO	
strategyType	INT	NO	不能低于 1000000
recvWindow	LONG	NO	赋值不能大于 60000
timestamp	LONG	YES'''

# 定义一个Market sell 交易功能 Input: coin, amount
def binance_market_sell(coin, amount):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': amount,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: 
        print(r.reason)
        return
'''
{
  "symbol": "CAKEUSDT",
  "orderId": 513572490,
  "orderListId": -1,
  "clientOrderId": "zCg1E3eUBhiLWtMI17xtjn",
  "transactTime": 1685855174465,
  "price": "0.00000000",
  "origQty": "571.00000000",
  "executedQty": "571.00000000",
  "cummulativeQuoteQty": "999.24718000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL",
  "workingTime": 1685855174465,
  "fills": [
    {
      "price": "1.75000000",
      "qty": "46.92000000",
      "commission": "0.00020124",
      "commissionAsset": "BNB",
      "tradeId": 73422414
    },
    ...
  ],
  "selfTradePreventionMode": "NONE"
}
'''    

# 定义一个 Limit sell 交易功能 Input: coin, amount, price
def binance_limit_sell(coin, amount, price):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'SELL',
        'type': 'LIMIT',
        'quantity': amount,
        'price': price,
        'timeInForce': 'GTC',
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: 
        print(r.reason)
        return
    
# 定义一个 do_limit_sell 功能，输入 coin, 从数据库中读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录, 用这条记录的 amount, update_id, buy_cost_value, buy_cost_bnb, buy_bnb_price, open_position_time, 调用 binance_limit_sell(coin, amount, price)
def do_limit_sell(coin, target_profit_ratio=0.05):
    coin = coin.upper()
    reply_msg = ''
    # 读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录
    try:
        df_balance = pd.read_sql_query(f"SELECT * FROM binance_position_buy WHERE coin = '{coin}' AND is_closed = 0 ORDER BY price ASC LIMIT 1", engine)
        if df_balance.empty: reply_msg = f'No open position for coin: {coin}'
    except: reply_msg = f'No open position for coin: {coin}'

    if reply_msg: return reply_msg

    amount = float(df_balance['executedQty'].values[0])
    buy_cost_value = float(df_balance['cummulativeQuoteQty'].values[0])

    # check coin balance see if it is enough
    df_coin_balance = get_user_asset()
    df_coin_balance = df_coin_balance[df_coin_balance['asset']==coin]
    if df_coin_balance.empty: 
        reply_msg = f'No balance for coin: {coin}'
        return reply_msg
    
    balance = float(df_coin_balance['free'].values[0])
    if balance < amount: 
        reply_msg = f'Balance {balance} is not enough for amount: {amount}'
        return reply_msg

    target_price = buy_cost_value * (1 + target_profit_ratio) / amount
    target_price = round(target_price, 4)

    data = binance_limit_sell(coin, amount, target_price)
    if not data: 
        reply_msg = f'Failed to do limit sell for coin: {coin}'
        return reply_msg
    
    print(json.dumps(data, indent=2))
    return data


# do_market_sell('eth', 0.1)
def do_market_sell(coin):
    coin = coin.upper()
    reply_msg = ''
    # 读取 binance_position_buy 中 coin == coin, is_closed == 0 的记录, 按照 price 从小到大排序, 取第一条记录
    try:
        df_balance = pd.read_sql_query(f"SELECT * FROM binance_position_buy WHERE coin = '{coin}' AND is_closed = 0 ORDER BY price ASC LIMIT 1", engine)
        if df_balance.empty: reply_msg = f'No open position for coin: {coin}'
    except: reply_msg = f'No open position for coin: {coin}'

    if reply_msg: return reply_msg

    amount = float(df_balance['executedQty'].values[0])
    update_id = int(df_balance['update_id'].values[0])
    buy_cost_value = float(df_balance['cummulativeQuoteQty'].values[0])
    buy_cost_bnb = float(df_balance['buy_cost_bnb'].values[0])
    buy_bnb_price = float(df_balance['buy_bnb_price'].values[0])
    open_position_time = int(df_balance['transactTime'].values[0])

    # check coin balance see if it is enough
    df_coin_balance = get_user_asset()
    df_coin_balance = df_coin_balance[df_coin_balance['asset']==coin]
    if df_coin_balance.empty: 
        reply_msg = f'No balance for coin: {coin}'
        return reply_msg
    
    balance = float(df_coin_balance['free'].values[0])
    if balance < amount: 
        reply_msg = f'Balance {balance} is not enough for amount: {amount}'
        return reply_msg

    data = binance_market_sell(coin, amount)
    if not data: 
        reply_msg = f'Failed to do market sell for coin: {coin}'
        return reply_msg

    # convert data['fills] to dataframe
    df_fills = pd.DataFrame(data['fills'])

    # calculate sum of commission
    sell_cost_bnb = df_fills['commission'].astype(float).sum()

    # check price of bnb
    df_bnb_price = get_token_price('BNB')
    sell_bnb_price = df_bnb_price if df_bnb_price else 0

    total_bnb_cost_value = buy_cost_bnb * buy_bnb_price + sell_cost_bnb * sell_bnb_price

    profit = float(data['cummulativeQuoteQty']) - buy_cost_value - total_bnb_cost_value

    # delete fills from data
    del data['fills']

    data['update_id'] = update_id
    data['sell_cost_bnb'] = sell_cost_bnb
    data['sell_bnb_price'] = sell_bnb_price
    data['total_bnb_cost_value'] = total_bnb_cost_value
    data['price'] = float(data['cummulativeQuoteQty']) / float(data['executedQty'])
    data['profit'] = profit

    # convert data to dataframe
    df_sellout_result = pd.DataFrame(data, index=[0])

    # 如果没有 binance_position_sell table, 就创建一个，如果 table 存在，就 append df_buyin_result
    df_sellout_result.to_sql('binance_position_sell', engine, if_exists='append', index=False)

    # 读取 binance_position_sell table 中的 profit 列，计算 sum(profit)
    df_profit = pd.read_sql_query('SELECT * FROM binance_position_sell', engine)
    if not df_profit.empty: profit_sum = df_profit['profit'].astype(float).sum()

    # update binance_position_buy table where update_id == update_id, set is_closed = 1
    sql = f"UPDATE binance_position_buy SET is_closed = 1 WHERE update_id = {update_id}"
    with engine.begin() as con: con.execute(text(sql))

    order_id = data['orderId']

    duration = (data['transactTime'] - open_position_time) / 1000 / 60 / 60
    # 讲 duration 变为 xx 天 xx 小时
    duration = f'{int(duration / 24)} 天 {int(duration % 24)} 小时' if duration > 24 else f'{int(duration)} 小时'

    reply_msg = f'''
卖出币种: {coin}
卖出价格: {format_number(data['price'])}
卖出数量: {format_number(amount)}
交易佣金: {format_number(total_bnb_cost_value)} usdt
交易获利: {format_number(profit)} usdt
持仓周期: {duration}
交易_ID: {order_id}
更新_ID: {update_id}
累计获利: {format_number(profit_sum)} usdt
'''

    return reply_msg
'''
      symbol    orderId  orderListId           clientOrderId   transactTime     price       origQty   executedQty cummulativeQuoteQty  status timeInForce    type  side    workingTime selfTradePreventionMode  update_id  sell_cost_bnb  sell_bnb_price  total_bnb_cost_value   profit
0  CAKEUSDT  513576898           -1  ixTpmGNbj5w3J2vW1NPAel  1685860174026  1.746501  572.40000000  572.40000000        999.69736000  FILLED         GTC  MARKET  SELL  1685860174026                    NONE          1        0.00245      306.124284               1.50045 -1.78589
'''

# 定义一个Market buy 交易功能 Input: coin, value
def binance_market_buy(coin, value):
    coin = coin.upper()
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': coin + 'USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quoteOrderQty': value,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        return data
    else: 
        print(r.reason)
        return 
'''
{
  "symbol": "CAKEUSDT",
  "orderId": 513570977,
  "orderListId": -1,
  "clientOrderId": "1uDKFPwUZ3KciXE0UTY1XR",
  "transactTime": 1685853893276,
  "price": "0.00000000",
  "origQty": "571.10000000",
  "executedQty": "571.10000000",
  "cummulativeQuoteQty": "999.99610000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "BUY",
  "workingTime": 1685853893276,
  "fills": [
    {
      "price": "1.75100000",
      "qty": "199.50000000",
      "commission": "0.00085585",
      "commissionAsset": "BNB",
      "tradeId": 73422265
    },
    ......
  ],
  "selfTradePreventionMode": "NONE"
}'''

# do_market_buy('eth', 1000)
def do_market_buy(coin, value):
    coin = coin.upper()
    reply_msg = ''
    # check USDT balance see if it is bigger than value
    df_usdt_balance = get_user_asset()
    df_usdt_balance = df_usdt_balance[df_usdt_balance['asset']=='USDT']
    if df_usdt_balance.empty: 
        reply_msg = 'No balance for coin: USDT'
        return reply_msg
    
    balance = float(df_usdt_balance['free'].values[0])
    if balance < value: 
        reply_msg = f'USDT Balance {balance} is not enough for value: {value}'
        return reply_msg

    data = binance_market_buy(coin, value)
    if not data: 
        reply_msg = f'Failed to do market buy for coin: {coin}'
        return reply_msg
    
    data['coin'] = data['symbol'].replace('USDT', '')
    data['price'] = float(data['cummulativeQuoteQty']) / float(data['executedQty'])

    # convert data['fills] to dataframe
    df_fills = pd.DataFrame(data['fills'])

    # calculate sum of commission, commision is string, convert to float first then sum
    commission = df_fills['commission'].astype(float).sum()
    data['buy_cost_bnb'] = commission

    # get bnb price
    df_bnb_price = get_token_price('BNB')
    bnb_price = df_bnb_price if df_bnb_price else 300

    data['buy_bnb_price'] = bnb_price

    # trading fee value
    trading_fee_value = commission * bnb_price

    # delete fills from data
    del data['fills']

    update_id = 0
    # 读取 binance_position_buy 最大的 update_id + 1
    try:
        df_max_update_id = pd.read_sql_query('SELECT MAX(update_id) FROM binance_position_buy', engine)
        if not df_max_update_id.empty: update_id = df_max_update_id['MAX(update_id)'].values[0]
    except: pass

    data['update_id'] = update_id + 1
    data['is_closed'] = 0

    # convert data to dataframe
    df_buyin_result = pd.DataFrame(data, index=[0])

    # 如果没有 binance_position_buy table, 就创建一个，如果 table 存在，就 append df_buyin_result
    df_buyin_result.to_sql('binance_position_buy', engine, if_exists='append', index=False)

    # 从 binance_position 读出最大的 update_id 的记录并打印
    df = pd.read_sql_query(f"SELECT * FROM binance_position_buy WHERE update_id = {update_id + 1}", engine)
    if not df.empty: 
        reply_msg = f'''
买入币种: {coin}
买入价格: {format_number(data["price"])} usdt/{coin.lower()}
买入数量: {format_number(data["executedQty"])} {coin.lower()}
买入佣金: {format_number(trading_fee_value)} usdt
交易_ID: {data["orderId"]}
更新_ID: {update_id + 1}
'''
        return reply_msg

'''
      symbol    orderId  orderListId           clientOrderId   transactTime  price       origQty   executedQty cummulativeQuoteQty  status timeInForce    type side    workingTime selfTradePreventionMode  coin  buy_cost_bnb  buy_bnb_price  update_id  is_closed
0  CAKEUSDT  513576831           -1  7F2qDttXThZ31GyHgmYa2D  1685860139703  1.747  572.40000000  572.40000000        999.98280000  FILLED         GTC  MARKET  BUY  1685860139703                    NONE  CAKE      0.002451     306.124284          1          0'''

# check binance_position_buy and calculate profit based on current price for all coins
def binance_position_buy_check_all(chat_id, coin=None, target_profit=0.05, crontab=False):
    # get df_balance from binance_position_buy
    df_balance = pd.read_sql_query('SELECT * FROM binance_position_buy WHERE is_closed = 0', engine)
    if df_balance.empty: return 'No open position for all coins'

    if coin: 
        df_balance = df_balance[df_balance['coin']==coin.upper()]
        if df_balance.empty: return f'No open position for coin: {coin}'

    # get current price for all coins
    df = get_token_price_table()
    if df.empty: return 'No price info for all coins'

    # merge df_balance and df based on coin since df and df_balance all have coin column
    df_balance = pd.merge(df_balance, df, on='coin', how='left')

    # convert df_balance first row to dict
    # print(json.dumps(df_balance.iloc[0].to_dict(), indent=2))
    '''
    {
      "symbol_x": "CAKEUSDT",
      "orderId": 513582692,
      "orderListId": -1,
      "clientOrderId": "VUxnvBkLBvuNSVzmLKV2NM",
      "transactTime": 1685863960460,
      "price": 1.7495544727679897,
      "origQty": "571.57000000",
      "executedQty": "571.57000000",
      "cummulativeQuoteQty": "999.99285000",
      "status": "FILLED",
      "timeInForce": "GTC",
      "type": "MARKET",
      "side": "BUY",
      "workingTime": 1685863960460,
      "selfTradePreventionMode": "NONE",
      "coin": "CAKE",
      "buy_cost_bnb": 0.0024476899999999998,
      "buy_bnb_price": 306.7,
      "update_id": 3,
      "is_closed": 0,
      "symbol_y": "CAKEUSDT",
      "lastPrice": 1.749
    }'''

    # convert df_balance['executedQty'] to float and calculate profit
    df_balance['executedQty'] = df_balance['executedQty'].astype(float)
    df_balance['profit'] = (df_balance['lastPrice'] - df_balance['price']) * df_balance['executedQty']

    # calculate up_ratio in % format
    df_balance['up_ratio'] = df_balance['lastPrice']/ df_balance['price'] - 1

    # calculate bnb_cost_value
    df_balance['bnb_cost_value'] = df_balance['buy_cost_bnb'] * df_balance['buy_bnb_price']
    
    # sort by profit
    df_balance = df_balance.sort_values(by='profit', ascending=False)

    for_reply = {}
    for i in range(df_balance.shape[0]):
        # ignore coin BNB
        if df_balance.iloc[i]['coin'] == 'BNB': continue

        reply_dict = df_balance.iloc[i].to_dict()
        # format_number for amount, profit, up_ratio, buy_price, current_price
        for_reply['持仓币种'] = reply_dict['coin']
        for_reply['持仓数量'] = format_number(reply_dict['executedQty'])
        for_reply['账面浮盈'] = format_number(reply_dict['profit'])
        for_reply['价格浮动'] = f"{reply_dict['up_ratio']:.2f}%"
        for_reply['建仓价格'] = f"{reply_dict['price']:.2f}"
        for_reply['当前价格'] = f"{reply_dict['lastPrice']:.2f}"
        for_reply['建仓佣金'] = format_number(reply_dict['bnb_cost_value'])
        for_reply['建仓时间'] = datetime.fromtimestamp(reply_dict['transactTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        for_reply['交易_ID'] = reply_dict['orderId']
        for_reply['更新_ID'] = reply_dict['update_id']

        reply_msg = '\n'.join([f"{k}: {v}" for k, v in for_reply.items()])
        if not crontab: send_msg(reply_msg, chat_id, parse_mode='', base_url=telegram_base_url)

        # 如果浮盈超过 5%, 就自动平仓
        if reply_dict['up_ratio'] > target_profit: send_msg(do_market_sell(reply_dict['coin']), chat_id, parse_mode='', base_url=telegram_base_url)

    if not crontab: 
        # 读取 binance_position_sell table 中的 profit 列，计算 sum(profit)
        df_profit = pd.read_sql_query('SELECT * FROM binance_position_sell', engine)
        if not df_profit.empty: 
            # 从 df_profit 中读取最早的 transactTime 并计算距离当前的时间
            earliest_transactTime = df_profit['transactTime'].astype(int).min()
            duration = (int(time.time() * 1000) - earliest_transactTime) / 1000 / 60 / 60
            # 讲 duration 变为 xx 天 xx 小时
            duration = f'{int(duration / 24)} 天 {int(duration % 24)} 小时' if duration > 24 else f'{int(duration)} 小时'
            profit_sum = df_profit['profit'].astype(float).sum()
            # 发送累计获利给 chat_id
            send_msg(f'Bot 运行 {duration} 累计获利: \n\n{format_number(profit_sum)} usdt', chat_id, parse_mode='', base_url=telegram_base_url)

    return

'''小额资产转换 (USER_DATA)
POST /sapi/v1/asset/dust (HMAC SHA256)
把小额资产转换成 BNB. 权重(UID): 10
参数:
名称	类型	是否必需	描述
asset	ARRAY	YES	正在转换的资产。 例如: asset=BTC,USDT
recvWindow	LONG	NO	
timestamp	LONG	YES
'''
# 定义一个功能，把小额资产转换成 BNB
def binance_dust_convert(coin):
    coin = coin.upper()
    print(f"Converting dust {coin} to BNB")
    PATH = '/sapi/v1/asset/dust'
    timestamp = int(time.time() * 1000)
    params = {
        'asset': coin,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.post(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        # print(json.dumps(data, indent=2))
        '''
        {
            "totalServiceCharge":"0.02102542",
            "totalTransfered":"1.05127099",
            "transferResult":[
                {
                    "amount":"0.03000000",
                    "fromAsset":"ETH",
                    "operateTime":1563368549307,
                    "serviceChargeAmount":"0.00500000",
                    "tranId":2970932918,
                    "transferedAmount":"0.25000000"
                },
                {
                    "amount":"0.09000000",
                    "fromAsset":"LTC",
                    "operateTime":1563368549404,
                    "serviceChargeAmount":"0.01548000",
                    "tranId":2970932918,
                    "transferedAmount":"0.77400000"
                },
                {
                    "amount":"248.61878453",
                    "fromAsset":"TRX",
                    "operateTime":1563368549489,
                    "serviceChargeAmount":"0.00054542",
                    "tranId":2970932918,
                    "transferedAmount":"0.02727099"
                }
            ]
        }'''
        totalTransfered = float(data['totalTransfered'])
        return totalTransfered
    else: 
        print(r)
        return
    
# 定义一个功能，把小额资产转换成 BNB 并吧 totalTransfered 发送给 chat_id
def binance_dust_convert_and_send_msg(coin, chat_id):
    totalTransfered = binance_dust_convert(coin)
    if not totalTransfered: return send_msg(f'转换 {coin} 到 BNB 失败, 六小时内只能请求一次, 请等待六小时再试吧。', chat_id)
    return send_msg(f'转换 {coin} 到 BNB 成功, 总共转换了 {totalTransfered} BNB', chat_id)

'''上架资产详情 (USER_DATA) 权重(IP): 1
GET /sapi/v1/asset/assetDetail (HMAC SHA256)
参数:
名称	类型	是否必需	描述
asset	STRING	NO	
recvWindow	LONG	NO	
timestamp	LONG	YES'''

# 查看给定币种的上架资产详情
def binance_asset_details(coin, chat_id):
    coin = coin.upper()
    PATH = '/sapi/v1/asset/assetDetail'
    timestamp = int(time.time() * 1000)
    params = {
        'asset': coin,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        # print(json.dumps(data, indent=2))
        '''
        {
        "RSR": {
            "withdrawFee": "2167",
            "minWithdrawAmount": "4334",
            "withdrawStatus": true,
            "depositStatus": true
        }
        }'''
        real_data = data[coin]
        real_data_str = '\n'.join([f"{k}: {v}" for k, v in real_data.items()])
        send_msg(real_data_str, chat_id)
        return 

'''查询每日资产快照 (USER_DATA) 权重(IP): 2400
参数:
名称	类型	是否必需	描述
type	STRING	YES	"SPOT", "MARGIN", "FUTURES"
startTime	LONG	NO	
endTime	LONG	NO	
limit	INT	NO	min 7, max 30, default 7
recvWindow	LONG	NO	
timestamp	LONG	YES	

查询时间范围最大不得超过30天
仅支持查询最近 1 个月数据
若startTime和endTime没传，则默认返回最近7天数据
'''

# 查询每日资产快照
def binance_daily_account_snapshot(type='SPOT', startTime=None, endTime=None, limit=1):
    PATH = '/sapi/v1/accountSnapshot'
    timestamp = int(time.time() * 1000)
    params = {
        'type': type,
        'limit': limit,
        'timestamp': timestamp
        }
    if startTime: params['startTime'] = startTime
    if endTime: params['endTime'] = endTime
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        print(json.dumps(data, indent=2))
        '''
        {
        "snapshotVos": [
            {
                "type": "SPOT",
                "updateTime": 1576281599000,
                "data": {
                    "balances": [
                        {
                            "asset": "BTC",
                            "free": "4723846.89208129",
                            "locked": "0.00000000"
                        },
                        {
                            "asset": "USDT",
                            "free": "4763366.68006011",
                            "locked": "1000.00000000"
                        }
                    ],
                    "totalAssetOfBtc": "0.00000000"
                }
            }
        ],
        "success": true
        }'''
        return data
    else: 
        print(r.reason)
        return


if __name__ == '__main__':
    print('tg_binance.py is working')


