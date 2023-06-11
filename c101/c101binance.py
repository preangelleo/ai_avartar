from c101variables import *
import c101format as fmt
from c101cmc import get_cmc_price


current_file = 'c101binance.py'

BINANCE_SECRET = binance_secret
BINANCE_BASE_URL = 'https://api.binance.com'

b = ccxt.binance({
    'apiKey': binance_api,
    'secret': binance_secret,
    'timeout': 30000,
    'enableRateLimit': True
})

BINANCE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'X-MBX-APIKEY': binance_api,
    "Content-Type": "application/json"
    }

def read_my_watchlist():
    df = pd.read_sql_query(f"SELECT * FROM db_address_watchlist WHERE is_deleted=0", remote_db_engine)
    return df

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

def network_name_change(str_name):
    str_name = str_name.upper()
    str_name = 'ETH' if str_name.startswith("ERC") else 'TRX' if str_name.startswith("TRC") else 'BSC' if str_name.startswith("BEP") else str_name
    return str_name


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
'''return:
 'XVS': {'depositStatus': True,
         'minWithdrawAmount': '0.034',
         'withdrawFee': '0.017',
         'withdrawStatus': True},
 'XYM': {'depositStatus': False,
         'minWithdrawAmount': '0.2',
         'withdrawFee': '0.1',
         'withdrawStatus': True},
 'YFI': {'depositStatus': True,
         'minWithdrawAmount': '0.00078',
         'withdrawFee': '0.00039',
         'withdrawStatus': True},
         'depositTip': "Delisted, Deposit Suspended"   //暂停充值的原因(如果暂停才有这一项)
'''


# Updated 2022-10-06 
# 用户万向划转 (USER_DATA)
# POST /sapi/v1/asset/transfer (HMAC SHA256)
''' type:
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
'''
'''
type	ENUM	YES	
asset	STRING	YES	
amount	DECIMAL	YES	
timestamp	LONG	YES
'''
def binance_internal_transfer(type_of_transfer, asset, amount, chat_id=''):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': type_of_transfer,
        'asset': asset,
        'amount': float(amount),
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200:
            send_msg(chat_id, r.text)
            return 
        data = r.json()
        return send_msg(chat_id, fmt.format_reply(data))
    except Exception as e:
        send_msg(chat_id, e)
        return

# type_of_transfer = 'MAIN_FUNDING'
# asset = 'NFT'
# amount = '8077335.41132700'
# data = binance_internal_transfer(type_of_transfer, asset, amount, debug=False)
# pp(data)


# 查询用户万向划转历史 (USER_DATA)
# GET /sapi/v1/asset/transfer (HMAC SHA256)
'''仅支持查询最近半年(6个月)数据
若startTime和endTime没传, 则默认返回最近7天数据'''
def get_binance_internal_transfer_history(type_of_transfer, since=1649491200000, debug=False):
    PATH = '/sapi/v1/asset/transfer'
    timestamp = int(time.time() * 1000)
    params = {
        'type': type_of_transfer,
        'startTime': since,
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
# type_of_transfer = 'MAIN_FUNDING'
# since = int(1649491200000)
# data = get_binance_internal_transfer_history(type_of_transfer, since, debug=False)
# pp(data)
# df = pd.DataFrame(data.get('rows'))
# pp(df)

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
'''return:
{
   "ipRestrict": false,  // 是否限制ip访问
   "createTime": 1623840271000,   // 创建时间
   "enableWithdrawals": false,   // 此选项允许通过此api提现。开启提现选项必须添加IP访问限制过滤器
   "enableInternalTransfer": true,  // 此选项授权此密钥在您的母账户和子账户之间划转资金
   "permitsUniversalTransfer": true,  // 授权该密钥可用于专用的万向划转接口，用以操作其支持的多种类型资金划转。各业务自身的划转接口使用权限，不受本授权影响
   "enableVanillaOptions": false,  // 欧式期权交易权限
   "enableReading": true,
   "enableFutures": false,  // 合约交易权限, 需注意开通合约账户之前创建的API Key不支持合约API功能
   "enableMargin": false,   // 此选项在全仓账户完成划转后可编辑
   "enableSpotAndMarginTrading": false, // 现货和杠杆交易权限
   "tradingAuthorityExpirationTime": 1628985600000  // 现货和杠杆交易权限到期时间，如果没有则不返回该字段
}
mine: 2022-10-06
{'createTime': 1659069823000,
 'enableFutures': True,
 'enableInternalTransfer': True,
 'enableMargin': False,
 'enableReading': True,
 'enableSpotAndMarginTrading': True,
 'enableVanillaOptions': False,
 'enableWithdrawals': True,
 'ipRestrict': True,
 'permitsUniversalTransfer': True}
'''


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
''' return:
{
    "data": {          // 账户API交易状态详情
            "isLocked": false,   // API交易功能是否被锁
            "plannedRecoverTime": 0,  // API交易功能被锁情况下的预计恢复时间
            "triggerCondition": { 
                    "GCR": 150,  // Number of GTC orders
                    "IFER": 150, // Number of FOK/IOC orders
                    "UFR": 300   // Number of orders
            },
            "updateTime": 1547630471725   
    }
}
mine:
{'data': {'isLocked': False,
          'plannedRecoverTime': 0,
          'triggerCondition': {'GCR': 150, 'IFER': 150, 'UFR': 300},
          'updateTime': 0}}
'''
# status = get_api_status()
# status = status.get('data').get('isLocked')


# 资金账户 (USER_DATA), 权重(IP): 1
# POST /sapi/v1/asset/get-funding-asset (HMAC SHA256)
# 目前仅支持查询以下业务资产：Binance Pay, Binance Card, Binance Gift Card, Stock Token
def get_funding_asset(debug=False):
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
'''return: 
[
    {
        "asset": "USDT",
        "free": "1",    // 可用余额
        "locked": "0",  // 锁定资金
        "freeze": "0",  //冻结资金
        "withdrawing": "0",  // 提币
        "btcValuation": "0.00000091"  // btc估值
    }
]'''

# 稳定币自动兑换划转查询 (USER_DATA), 权重(UID): 5
# POST /sapi/v1/asset/convert-transfer/queryByPage
def binance_stable_coin_convert_history(start_time=7):
    PATH = '/sapi/v1/asset/convert-transfer/queryByPage'
    start_time_delta = 1000 * 60 * 60 * 24 * int(start_time)
    timestamp = int(time.time() * 1000)
    starTime = timestamp - start_time_delta
    params = {
        'startTime': starTime,
        'endTime': timestamp,
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
        return data
    except Exception as e:
        print(e)
        return
# data = binance_stable_coin_convert_history(start_time=7)
# pp(data)
# df = pd.DataFrame(data.get('rows'))
# pp(df)
''' return
{'rows': [{'accountType': 'MAIN',
           'deductedAmount': '1000',
           'deductedAsset': 'USDC',
           'status': 'S',
           'targetAmount': '1000',
           'targetAsset': 'BUSD',
           'time': 1665556594000,
           'tranId': 119041545940,
           'type': 11},
          {'accountType': 'MAIN',
           'deductedAmount': '9457.898366',
           'deductedAsset': 'USDC',
           'status': 'S',
           'targetAmount': '9457.898366',
           'targetAsset': 'BUSD',
           'time': 1665556496000,
           'tranId': 119041424048,
           'type': 11}],
 'total': 2}
'''


# 获取 Pay 交易历史记录 (USER_DATA), GET /sapi/v1/pay/transactions (HMAC SHA256)
# 若startTime和endTime均未发送,只返回最近90天数据
# 权重(UID): 3000, 支持查询日期范围：近18个月以内的订单
# "walletType": 1, // 1 资金钱包；2 现货钱包
# https://binance-docs.github.io/apidocs/spot/cn/#user_data-107 
def get_binance_pay_history():
    df_old = pd.read_sql_query(f'SELECT * FROM db_binance_ltd_payment_history', remote_db_engine)
    start_time = df_old['transactionTime'].max()
    PATH = '/sapi/v1/pay/transactions'
    timestamp = int(time.time() * 1000)
    params = {
        'startTime':  int(start_time) + 1000, # 时区切换，+8 小时，并且向后顺延 1 秒 + (60 * 60 * 8 * 1000)
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code != 200 or not r.json().get('data'):
            return df_old
        df = pd.DataFrame(r.json().get('data'))
        df.drop(columns=['fundsDetail'], inplace=True)
        df.to_sql('db_binance_ltd_payment_history', remote_db_engine, if_exists='append', index=False)
        df = pd.read_sql_query(f'SELECT * FROM db_binance_ltd_payment_history', remote_db_engine)
        return df
    except Exception as e:
        print(e)
        return df_old


# 币安统一账户查询, 用户持仓 (USER_DATA), 获取用户持仓，仅返回>0的数据。权重(IP): 5
# POST /sapi/v3/asset/getUserAsset 
def get_user_asset(all_assets=False):
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
        if all_assets:
            return data
        return data.loc[data['btcValuation']!='0']
    except Exception as e:
        print(e)
        return


# 获取所有币信息 (USER_DATA), 获取针对用户的所有(Binance支持充提操作的)币种信息。权重(IP): 10
# GET /sapi/v1/capital/config/getall (HMAC SHA256)
# https://binance-docs.github.io/apidocs/spot/cn/#system
def get_account_all(debug=False):
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
# all = get_account_all(debug=True)

# 获取币安全部交易对最新价格
def get_balances_realtime_value_dataframe():
    df_one = update_db_binance_balances()
    if df_one.empty: 
        return print(f"DEBUG : NO balances in binance account.")
    # Get ticker data
    df_ticker = pd.read_json(BINANCE_TICKER_URL)
    df_ticker = df_ticker.loc[:, ['symbol', 'lastPrice']]
    df_ticker = df_ticker.rename(columns={'lastPrice': 'price'})
    # Merge balance and ticker data
    df = pd.merge(df_one, df_ticker, on='symbol', how='left')
    df['value'] = df['balance'] * df['price']
    # Assign USDTUSDT price to 1 and value equal to balance
    df.loc[df['symbol'] == 'USDTUSDT', 'price'] = 1
    df.loc[df['symbol'] == 'USDTUSDT', 'value'] = df.loc[df['symbol'] == 'USDTUSDT', 'balance']
    df = df.sort_values(by='value', ascending=False)
    df = df[df['value'] >= 100]
    df.to_sql('db_binance_balances', remote_db_engine, if_exists='replace', index=False)
    return df

# 获取交易对最新价格, 不包括 Volume, 权重 2
# GET /api/v3/ticker/price
# https://binance-docs.github.io/apidocs/spot/cn/#8ff46b58de
# df = pd.read_json('https://api.binance.com/api/v3/ticker/price') 权重 2, 返回所有交易对价格（不包括 volume）
def get_price_for_symbols(symbols_list):
    PATH = '/api/v3/ticker/price'
    url = BINANCE_BASE_URL + PATH
    response = requests.get(url, headers=BINANCE_HEADERS)
    if response.status_code != 200:
        print("response.status_code: ", response.status_code)
        print("response.text: ", response.text)
    else:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            if type(symbols_list) is list:
                df_list = pd.DataFrame(symbols_list, columns=['symbol'])
                df['price'] = df['price'].astype(float)
                df = pd.merge(df, df_list, how='inner', on='symbol')
                return df
            if type(symbols_list) is str:
                symbol = symbols_list.upper()
                df_symbol = df.loc[(df['symbol']==symbol) | (df['symbol']==symbol+'USDT')]
                if not df_symbol.empty:
                    return float(df_symbol.iloc[0]['price'])
    if type(symbols_list) is str:
        res = get_cmc_price(symbol)
        if res: return res.get('price', 0)
    return


# 24hr 价格变动情况, 24 小时滚动窗口价格变动数据。 请注意，不携带symbol参数会返回全部交易对数据，不仅数据庞大，而且权重极高(40), 20 ~ 100 Symbols (权重 20)
# GET /api/v3/ticker/24hr | 单个 symbol 权重 1
# https://binance-docs.github.io/apidocs/spot/cn/#24hr
def get_price_for_my_trading_list(symbol):
    PATH = '/api/v3/ticker/24hr'
    url = BINANCE_BASE_URL + PATH
    params = {
        'type': 'MINI',
        'symbol': symbol
        }
    response = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if response.status_code != 200:
        print("response.status_code: ", response.status_code)
        print("response.text: ", response.text)
        return
    else:
        data = response.json()
        return data
''' return:
{'closeTime': 1665575299142,
 'count': 34659,
 'firstId': 48787815,
 'highPrice': '0.00736000',
 'lastId': 48822473,
 'lastPrice': '0.00660000',
 'lowPrice': '0.00657000',
 'openPrice': '0.00683000',
 'openTime': 1665488899142,
 'quoteVolume': '14350779.19125200',
 'symbol': 'RSRUSDT',
 'volume': '2073521575.50000000'}
'''

# 稳定币自动兑换划转
# POST /sapi/v1/asset/convert-transfer
def stable_coin_swap(origin_coin, amount, target_coin='BUSD'):
    PATH = '/sapi/v1/asset/convert-transfer'
    timestamp = int(time.time() * 1000)    
    # client_swap_id = f_hash.hash_md5(MY_MAIN_ADDRESS)
    params = {
        'clientTranId': 'de2bf837e55dbeab1bd09d30611b299f',
        'asset': origin_coin,
        'amount': int(amount),
        'targetAsset': target_coin,
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    try:
        r = requests.post(url, headers=BINANCE_HEADERS, params=params)
        print(r.text)
        if r.status_code != 200:
            print(r.text)
            return
        data = r.json()
        return data
    except Exception as e:
        time.sleep(0.1)
        return 


def get_withdraw_and_deposit_network(coin):
    coin = coin.upper()
    data = get_account_all()
    df = pd.DataFrame(data)
    coin_list = df['coin'].tolist()
    if coin not in coin_list: return f"Sorry {coin} is not available in Binance"

    df_coin = df.loc[df['coin']==coin]
    network_list = df_coin['networkList']
    wd_list = []
    dp_list = []
    for n in network_list:
        df1 = pd.DataFrame(n)
        if df1.empty: continue
        wd_list = df1.loc[df1['withdrawEnable']==True]['network'].tolist()
        dp_list = df1.loc[df1['depositEnable']==True]['network'].tolist()
    return wd_list, dp_list


def get_withdraw_integer_multiple(coin, number, network='ETH', chat_id=bot_owner_chat_id):
    coin = coin.upper()
    data = get_account_all()
    df = pd.DataFrame(data)
    coin_list = df['coin'].tolist()
    if coin not in coin_list:
        send_msg(chat_id, f"Sorry {coin} is not available in Binance")
        return
    df_coin = df.loc[df['coin']==coin]
    try:
        network_list = df_coin.iloc[0]['networkList']
        df1 = pd.DataFrame(network_list)
        matched_network = df1.loc[df1['network']==network.upper()]
        withdrawIntegerMultiple = matched_network.iloc[0]['withdrawIntegerMultiple']
        number = int(number / float(withdrawIntegerMultiple)) * float(withdrawIntegerMultiple)
        return number
    except Exception as e:
        print(e)
        return number


# 获取充值历史(支持多网络) (USER_DATA), 权重(IP): 1
# GET /sapi/v1/capital/deposit/hisrec (HMAC SHA256)
def get_deposit_history_task():
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
        if df.empty:
            return
        else:
            df_status_is_1 = df.loc[df['status']==1]
            if not df_status_is_1.empty:
                return df_status_is_1
    return


def update_db_binance_balances():
    PATH = '/api/v3/account'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 6000
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code != 200: return

    df = pd.DataFrame(r.json()['balances'])
    df_one = df.loc[(df['free'].astype(float) > 0), ['asset', 'free']]
    df_one.rename(columns={'asset': 'coin', 'free': 'balance'}, inplace=True)
    df_one['symbol'] = df_one['coin'].astype(str) + 'USDT'
    df_one['balance'] = df_one['balance'].astype(float)
    
    return df_one

# 获取充值历史(支持多网络) (USER_DATA), 权重(IP): 1
# GET /sapi/v1/capital/deposit/hisrec (HMAC SHA256)
def get_deposit_history():
    df_old = pd.read_sql_query(f'SELECT MAX(insertTime) FROM db_binance_ltd_deposit_history', remote_db_engine)
    start_time = df_old.iloc[0]['MAX(insertTime)']
    PATH = '/sapi/v1/capital/deposit/hisrec'
    timestamp = int(time.time() * 1000)
    params = {
        'startTime': int(start_time) + 1000, # 向后延后 1 秒，否则会把上次最后一条记录再抓回来
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if df.empty: return
        else:
            df_status_is_1 = df.loc[df['status']==1]
            if not df_status_is_1.empty:
                df_status_is_1.to_sql('db_binance_ltd_deposit_history', remote_db_engine, if_exists='append', index=False)
                return df_status_is_1
    return
'''return:
[
    {
        "id": "769800519366885376",
        "amount": "0.001",
        "coin": "BNB",
        "network": "BNB",
        "status": 0,
        "address": "bnb136ns6lfw4zs5hg4n85vdthaad7hq5m4gtkgf23",
        "addressTag": "101764890",
        "txId": "98A3EA560C6B3336D348B6C83F0F95ECE4F1F5919E94BD006E5BF3BF264FACFC",
        "insertTime": 1661493146000,
        "transferType": 0,
        "confirmTimes": "1/1",
        "unlockConfirm": 0,
        "walletType": 0
    },
    {
        "id": "769754833590042625",
        "amount":"0.50000000",
        "coin":"IOTA",
        "network":"IOTA",
        "status":1,
        "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
        "addressTag":"",
        "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
        "insertTime":1599620082000,
        "transferType":0,
        "confirmTimes": "1/1",
        "unlockConfirm": 0,
        "walletType": 0
    }
]'''


# 获取提币历史 (支持多网络) (USER_DATA), 权重(IP): 1
# GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
# 0(0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
# https://binance-docs.github.io/apidocs/spot/cn/#user_data-6
def get_withdraw_history_task():
    PATH = '/sapi/v1/capital/withdraw/history'
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
        if df.empty:
            return
        else:
            df_status_is_6 = df.loc[df['status']==6]
            if not df_status_is_6.empty:
                return df_status_is_6
    return


# 获取提币历史 (支持多网络) (USER_DATA), 权重(IP): 1
# GET /sapi/v1/capital/withdraw/history (HMAC SHA256)
# 0(0:已发送确认Email,1:已被用户取消 2:等待确认 3:被拒绝 4:处理中 5:提现交易失败 6 提现完成)
# https://binance-docs.github.io/apidocs/spot/cn/#user_data-6
def get_withdraw_history():
    df_old = pd.read_sql_query(f'SELECT MAX(applyTime) FROM db_binance_ltd_withdraw_history', remote_db_engine)
    start_time = df_old.iloc[0]['MAX(applyTime)']
    start_time = int(datetime.fromisoformat(start_time).timestamp() * 1000)
    PATH = '/sapi/v1/capital/withdraw/history'
    timestamp = int(time.time() * 1000)
    params = {
        'startTime': int(start_time) + (60 * 60 * 8 * 1000) + 1000, # 时区切换，+8 小时，并且向后顺延 1 秒
        'timestamp': timestamp
        }
    query_string = urlencode(params)
    params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BINANCE_BASE_URL, PATH)
    r = requests.get(url, headers=BINANCE_HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        df = pd.DataFrame(data)
        if df.empty:
            return
        else:
            df_status_is_6 = df.loc[df['status']==6]
            if 'addressTag' in df_status_is_6.columns.tolist():
                df_status_is_6.drop(columns=['addressTag'], inplace=True)
            if not df_status_is_6.empty:
                df_status_is_6.to_sql('db_binance_ltd_withdraw_history', remote_db_engine, if_exists='append', index=False)
                return df_status_is_6
    return
'''return:
[
    {
        "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
        "amount": "8.91000000",   // 提现转出金额
        "applyTime": "2019-10-12 11:12:02",  // UTC 时间
        "coin": "USDT",
        "id": "b6ae22b3aa844210a7041aee7589627c",  // 该笔提现在币安的id
        "withdrawOrderId": "WITHDRAWtest123", // 自定义ID, 如果没有则不返回该字段
        "network": "ETH",
        "transferType": 0 // 1: 站内转账, 0: 站外转账    
        "status": 6,
        "transactionFee": "0.004", // 手续费
        "confirmNo":3,  // 提现确认数
        "info": "The address is not valid. Please confirm with the recipient",  // 提币失败原因
        "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"   // 提现交易id
    },
    {
        "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB",
        "amount": "0.00150000",
        "applyTime": "2019-09-24 12:43:45",
        "coin": "BTC",
        "id": "156ec387f49b41df8724fa744fa82719",
        "network": "BTC",
        "transferType": 0,  // 1: 站内转账, 0: 站外转账
        "status": 6,
        "transactionFee": "0.004",
        "confirmNo": 2,
        "info": "",
        "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354"
    }
]'''


# 获取充值地址 (支持多网络) (USER_DATA), 权重(IP): 10
# GET /sapi/v1/capital/deposit/address (HMAC SHA256)
def get_deposit_address(symbol, network, wd_dp):
    if not wd_dp or type(wd_dp) is str: return

    symbol = str(symbol).upper()
    network = symbol.upper() if not network else network.upper()
    network = network_name_change(network)
    PATH = '/sapi/v1/capital/deposit/address'
    timestamp = int(time.time() * 1000)
    params = {
        'coin': symbol,
        'network': network,
        'timestamp': timestamp
    }

    wd_list, dp_list = wd_dp
    if (network.upper() not in dp_list): return f"{network.upper()} not in deposit_list"

    else:
        query_string = urlencode(params)
        params['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(BINANCE_BASE_URL, PATH)
        r = requests.get(url, headers=BINANCE_HEADERS, params=params)
        if r.status_code == 200:
            data = r.json()
            data['network'] = network.upper()
            del(data['url'])
            if not data['tag']:
                del(data['tag'])
            if network.upper() in ['ETH', 'BSC', 'AVAXC', 'MATIC']:
                data['address'] = web3.toChecksumAddress(data['address'])
            return data
    return


def creat_task_for_db_withdraw_task(coin, amount, withdraw_to_address, chat_id=bot_owner_chat_id, network='eth', memo=''):
    remo_conn = remote_db_engine.connect()
    try:
        df = pd.read_sql_query(f"SELECT * FROM db_withdraw_task WHERE coin='{coin}' ORDER BY withdraw_task_id DESC LIMIT 1", remote_db_engine)
        if not df.empty:
            if (df.iloc[0]['amount'] == amount) and (df.iloc[0]['withdraw_to_address'] == withdraw_to_address):
                withdraw_task_id = df.iloc[0]['withdraw_task_id']
                remo_conn.close()
                reply_dict = df.iloc[0].to_dict()
                reply_dict['alert'] = f"looks like withdraw_task_id {withdraw_task_id} has the exact same withdraw data. don't double withdraw. if you insist to do that, please change memo info to make it different."
                return reply_dict
        remo_conn.execute("INSERT INTO db_withdraw_task (coin, amount, withdraw_to_address, chat_id, network, memo, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s)", (coin, amount, withdraw_to_address, chat_id, network, memo, datetime.now()))
        remo_conn.close()
    except Exception as e: return f"ERROR : creat_task_for_db_withdraw_task() failed.\n\n{e}"
    df = pd.read_sql_query(f"SELECT * FROM db_withdraw_task WHERE is_accomplished=0 AND is_dropped IS NULL AND coin='{coin}' ORDER BY withdraw_task_id DESC LIMIT 1", remote_db_engine)
    return df.iloc[0].to_dict()


# 2022年-10月-3日更新并测试 "withdraw_id": "dfb8f6d832984b8bb93dcc1dcfdf2738"
def withdraw(**kwargs):
    wait_sleep_time = 60
    exception_sleep_time = 1
    chat_id = BOTOWNER_CHAT_ID
    if 'chat_id' in kwargs:
        chat_id = kwargs['chat_id']
        del(kwargs['chat_id'])
    memo = None
    if 'memo' in kwargs:
        memo = kwargs.get('memo')
        del(kwargs['memo'])
    task_id = None
    if 'task_id' in kwargs:
        task_id = kwargs.get('task_id')
        del(kwargs['task_id'])
    transactions_id = None
    if 'transactions_id' in kwargs:
        transactions_id = kwargs.get('transactions_id')
        del(kwargs['transactions_id'])
    withdraw_task_id = None
    if 'withdraw_task_id' in kwargs:
        withdraw_task_id = kwargs.get('withdraw_task_id')
        del(kwargs['withdraw_task_id'])
    PATH = '/sapi/v1/capital/withdraw/apply'
    kwargs['coin'] = 'BUSD' if str(kwargs['coin']).upper() == 'USDC' else str(kwargs['coin']).upper()
    kwargs['amount'] = float(kwargs['amount'])
    kwargs['network'] = network_name_change(kwargs['network'])
    # coin_list_df = pd.read_sql_query(f"SELECT * FROM db_tokens_can_withdraw_from_binance WHERE coin='{kwargs['coin']}'", remote_db_engine)
    coin_list_df = pd.read_sql_query(f"SELECT * FROM db_cmc_total_supply WHERE symbol='{kwargs['coin']}' AND in_mylist=1 AND in_blacklist=0", remote_db_engine)
    if coin_list_df.empty:
        send_msg(chat_id, f"Sorry, {kwargs['coin']} is not in_mylist.")
        return
    token_address = coin_list_df.iloc[0]['token_address']
    decimals = coin_list_df.iloc[0]['decimals']
    data = get_account_all()
    df = pd.DataFrame(data)
    df_coin = df.loc[(df['coin']==kwargs['coin']) & (df['withdrawAllEnable']==True)]
    network_list = df_coin.iloc[0]['networkList']
    df1 = pd.DataFrame(network_list)
    if df1.empty:
        send_msg(chat_id, "withdraw() df1.empty networkList column is empty")
        return
    matched_network = df1.loc[(df1['withdrawEnable']==True) & (df1['network']==kwargs['network'])]
    if matched_network.empty:
        send_msg(chat_id, f"withdraw() matched_network.empty network {kwargs['network']} is not available")
        return
    if kwargs['network'] in ['ETH', 'BSC', 'AVAXC', 'MATIC', 'MOVR']:
        try:
            kwargs['address'] = web3.toChecksumAddress(kwargs['address'])
        except Exception as e:
            send_msg(chat_id, f"withdraw() Failed to transform {kwargs['address']} to a CheckSumAddress.")
            return
    elif kwargs['network'] == 'TRX':
        destination_address = re.findall(TRX_REGEX, kwargs['address'])
        if not destination_address:
            send_msg(chat_id, f"withdraw() network is 'TRX' but can't find any TRC20 Address from kwargs['address']:\n{kwargs['address']}")
            return
        kwargs['address'] = destination_address[0]
    try:
        free = float(df_coin.iloc[0]['free'])
        withdraw_fee = matched_network.iloc[0]['withdrawFee']
        withdraw_fee = float(withdraw_fee)
        withdraw_min = matched_network.iloc[0]['withdrawMin']
        withdraw_min = float(withdraw_min)
        withdraw_max = matched_network.iloc[0]['withdrawMax']
        withdraw_max = float(withdraw_max)
        if free - kwargs['amount'] >= withdraw_fee:
            kwargs['amount'] += withdraw_fee
        kwargs['amount'] = round(kwargs['amount'], 4)
    except Exception as e:
        send_msg(chat_id, f"withdraw() failed to get free balance or withdraw fee, or withdraw min or withdraw max\n{e}")
        return
    if kwargs['amount'] > withdraw_max or kwargs['amount'] < withdraw_min:
        send_msg(chat_id, f"withdraw() amount > withdraw_max or amount < withdraw_min")
        return
    # 检查是否可能重复提币, 看看最后一次提币是否重复.
    is_withdrawed = False
    df_status_is_6 = get_withdraw_history_task()
    if df_status_is_6 is not None and not df_status_is_6.empty:
        last_withdraw = df_status_is_6.head(1)
        last_amount = float(last_withdraw.iloc[0]['amount'])
        last_address = last_withdraw.iloc[0]['address']
        last_coin = last_withdraw.iloc[0]['coin']
        kwargs['withdraw_id'] = last_withdraw.iloc[0]['id']
        if last_address == kwargs['address'] and last_coin == kwargs['coin'] and (last_amount == kwargs['amount'] or last_amount == kwargs['amount'] - withdraw_fee):
            hash_tx = last_withdraw.iloc[0]['txId']
            if hash_tx:
                send_msg(chat_id, f"withdraw() 取款早前已经链上确认, 避免了重复取款 hash_tx: \n{hash_tx}\n正在更新到数据库中...")
                is_withdrawed = True
    # 如果没有重复提币，则进入提币环节.
    if not is_withdrawed:
        if free < kwargs['amount']:
            send_msg(chat_id, f"withdraw() df_coin.empty, coin name {kwargs['coin']} is wrong or amount {kwargs['amount']} is higher than balance, or coin is not available to withdraw.")
            return
        kwargs['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(kwargs)
        kwargs['signature'] = hmac.new(BINANCE_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(BINANCE_BASE_URL, PATH)
        r = requests.post(url, headers=BINANCE_HEADERS, params=kwargs)
        if r.status_code != 200 or 'id' not in r.json():
            send_msg(chat_id, f"withdraw() Failed, erro:\n{r.text}")
            return
        del(kwargs['signature'])
        del(kwargs['timestamp'])
        kwargs['withdraw_id'] = r.json()['id']
        # kwargs['withdraw_id'] = '07a3fb6a3cc74c05a714540ec059f695'
        send_msg(chat_id, f"withdraw() 取款成功提交, 取款 ID: \n{kwargs['withdraw_id']}\n正在等待生成 hash_tx (txID) 以便更新到数据库中。\n每隔 {wait_sleep_time}s 自动查看一次, 直到更新成功写入数据库, 并发出通知。")
        x = 1
        while True:
            time.sleep(wait_sleep_time)
            send_msg(chat_id, f"检查 withdraw() 取款是否已链上确认 第 {x} 次.")
            x += 1
            df_status_is_6 = get_withdraw_history_task()
            if df_status_is_6 is None or df_status_is_6.empty:
                continue
            last_withdraw = df_status_is_6.loc[df_status_is_6['id']==kwargs['withdraw_id']]
            if last_withdraw.empty:
                continue
            hash_tx = last_withdraw.iloc[0]['txId']
            if hash_tx:
                send_msg(chat_id, f"withdraw() 取款已链上确认, hash_tx: \n{hash_tx}\n正在更新到数据库中...")
                break
    conn = remote_db_engine.connect()
    while True:
        try:
            if transactions_id and not task_id:
                remote_conn.execute("REPLACE INTO db_token_transactions (hash_tx, binance_id, coin, network, token_address, decimals, value, cost_value, from_address, to_address, from_addr_balance, memo, update_time, transactions_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (hash_tx, kwargs['withdraw_id'] , kwargs['coin'], kwargs['network'], token_address, decimals, kwargs['amount'], withdraw_fee, 'binance', kwargs['address'], free, memo, datetime.now(), transactions_id))
                break
            elif task_id and not transactions_id:
                remote_conn.execute("REPLACE INTO db_token_transactions (hash_tx, binance_id, coin, network, token_address, decimals, value, cost_value, from_address, to_address, from_addr_balance, memo, update_time, task_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (hash_tx, kwargs['withdraw_id'] , kwargs['coin'], kwargs['network'], token_address, decimals, kwargs['amount'], withdraw_fee, 'binance', kwargs['address'], free, memo, datetime.now(), task_id))
                break
            elif withdraw_task_id and not transactions_id and not task_id:
                remote_conn.execute("REPLACE INTO db_token_transactions (hash_tx, binance_id, coin, network, token_address, decimals, value, cost_value, from_address, to_address, from_addr_balance, memo, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (hash_tx, kwargs['withdraw_id'] , kwargs['coin'], kwargs['network'], token_address, decimals, kwargs['amount'], withdraw_fee, 'binance', kwargs['address'], free, memo, datetime.now()))
                break
            time.sleep(exception_sleep_time)
            exception_sleep_time = exception_sleep_time * 2
        except Exception as e:
            send_msg(chat_id, f"withdraw() 数据库更新失败\n{e}\n\n等待 {exception_sleep_time}s 后继续尝试.")
            time.sleep(exception_sleep_time)
            exception_sleep_time = exception_sleep_time * 2
    conn.close()
    kwargs['hash_tx'] = hash_tx
    kwargs['withdraw_fee'] = withdraw_fee
    try:
        reply_msg = last_withdraw.iloc[0].to_dict()
        if reply_msg:
            send_msg(chat_id, fmt.format_reply(reply_msg))
    except Exception as e:
        print(e)
    return kwargs

def hand_update_trade_database(trade_side, task_id, relative_order_id, relative_usdt, relative_amount, relative_price, connected_task_id=0):
    try:
        if trade_side == 'buy':
            spend_usdt = relative_usdt
            remote_conn.execute(f"UPDATE db_deposit_trade_and_withdraw_task SET buy_order_id='{relative_order_id}', amount={relative_amount}, spend_usdt={spend_usdt}, buy_price={relative_price}, buy_time='{datetime.now()}' WHERE task_id={task_id}")
            if connected_task_id:
                connected_task_id = int(connected_task_id)
                df = pd.read_sql_query(f"SELECT spend_usdt, receive_usdt FROM db_deposit_trade_and_withdraw_task WHERE task_id={connected_task_id}", remote_db_engine)
                receive_usdt = df.iloc[0]['receive_usdt']
                is_closed = 1
                premium = receive_usdt - spend_usdt
                remote_conn.execute(f"UPDATE db_deposit_trade_and_withdraw_task SET premium={premium}, is_closed={is_closed}, connected_task_id={task_id} WHERE task_id={connected_task_id}")
        else:
            receive_usdt = relative_usdt
            remote_conn.execute(f"UPDATE db_deposit_trade_and_withdraw_task SET sell_order_id='{relative_order_id}', amount={relative_amount}, receive_usdt={receive_usdt}, sell_price={relative_price}, sell_time='{datetime.now()}' WHERE task_id={task_id}")
            if connected_task_id:
                connected_task_id = int(connected_task_id)
                df = pd.read_sql_query(f"SELECT spend_usdt, receive_usdt FROM db_deposit_trade_and_withdraw_task WHERE task_id={connected_task_id}", remote_db_engine)
                spend_usdt = df.iloc[0]['spend_usdt']
                is_closed = 1
                premium = receive_usdt - spend_usdt
                remote_conn.execute(f"UPDATE db_deposit_trade_and_withdraw_task SET premium={premium}, is_closed={is_closed}, connected_task_id={task_id} WHERE task_id={connected_task_id}")
        return
    except Exception as e:
        print(e)
    return


    
if __name__ == '__main__':
    print(f"{current_file} is running...")
