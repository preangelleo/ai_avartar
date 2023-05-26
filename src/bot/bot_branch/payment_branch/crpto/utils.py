import json

from src.utils.utils import *
from datetime import datetime, timedelta
from eth_account import Account


# 用 Pandas 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息并放入 df
def get_token_info_from_db_cmc_total_supply(token_address):
    print(f"DEBUG: get_token_info_from_db_cmc_total_supply()")
    # Create a new session
    with Params().Session() as session:
        # Query the table 'db_cmc_total_supply' to get the token_info
        df = pd.read_sql(session.query(CmcTotalSupply).filter(CmcTotalSupply.token_address == token_address).statement,
                         session.bind)
        return df


def markdown_transaction_hash(hash_tx):
    markdown_tx = f'[{hash_tx[:6]}......{hash_tx[-7:]}]({Params().ETHERSCAN_TX_URL_PREFIX}{hash_tx})'
    return markdown_tx


def markdown_token_address(token_address):
    markdown_token = f'[{token_address[:6]}...{token_address[-7:]}]({Params().ETHERSCAN_TOKEN_URL_PREFIX}{token_address})'
    return markdown_token


def markdown_tokentnxs(address):
    markdown_token = f'[{address[:6]}...{address[-7:]}]({Params().ETHERSCAN_TOKEN_URL_PREFIX}{address}#tokentxns)'
    return markdown_token


def markdown_wallet_address(wallet_address):
    markdown_address = f'[{wallet_address[:6]}...{wallet_address[-7:]}]({Params().ETHERSCAN_WALLET_URL_PREFIX}{wallet_address})'
    return markdown_address


def etherscan_make_api_url(module, action, **kwargs):
    BASE_URL = "https://api.etherscan.io/api"
    url = BASE_URL + f"?module={module}&action={action}&apikey={Params().ETHERSCAN_API}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def get_token_abi(address):
    get_abi_url = etherscan_make_api_url("contract", "getabi", address=address)
    response = requests.get(get_abi_url)
    if response.status_code != 200: return
    data = response.json()
    return data["result"]


def get_transaction_details(transaction_hash, chain='eth'):
    url = f'https://deep-index.moralis.io/api/v2/transaction/{transaction_hash}?chain={chain}'
    headers = {'accept': 'application/json', 'X-API-Key': Params().MORALIS_API}
    response = requests.get(url, headers=headers)
    # print(response.status_code, response.text)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Request failed with status code: {response.status_code}')
        return None


# 通过 hash_tx 查询转账信息
def get_transactions_info_by_hash_tx(bot, hash_tx, chat_id, user_title, chain='eth'):
    hash_tx = str(hash_tx).lower()
    if not hash_tx.startswith('0x') and len(hash_tx) == 64: hash_tx = '0x' + hash_tx
    if len(hash_tx) != 66:
        return bot.send_msg(f"输入的 hash_tx 长度不对, 请回复正确的 Transaction_Hash: 0x开头, 一共 66 位字符 😃", chat_id)
    trans_info = get_transaction_details(hash_tx, chain=chain)

    if not trans_info:
        bot.send_msg(f"抱歉, 无法查询到 {hash_tx} 的转账信息, 请检查输入是否正确. 😰", chat_id)
        return
    if not trans_info.get('input'):
        bot.send_msg(f"抱歉, 查到的信息有问题, 无法正确读取. 😰", chat_id)
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
        bot.send_msg(
            f"亲爱的, 这是一笔 ETH 转账 🤩:\n\n转账数额: {format_number(eth_value)} eth\n转账地址: {markdown_wallet_address(trans_info.get('from_address'))}\n收款地址: {markdown_wallet_address(trans_info.get('to_address'))}\n交易确认: {markdown_transaction_hash(hash_tx)}",
            chat_id, parse_mode='Markdown')

        return

    token_address = trans_info.get('to_address')

    # 从 CmcTotalSupply db_cmc_total_supply 读取 token_address 的信息
    coin_list_df = get_token_info_from_db_cmc_total_supply(token_address)
    if coin_list_df.empty:

        internal_trans_list = get_internal_transactions(hash_tx)
        if type(internal_trans_list) != list:
            bot.send_msg(
                f"抱歉, {markdown_token_address(token_address)} 不在我的数据库里, 不清楚这是个什么币子, 无法查询. 😰",
                chat_id, parse_mode='Markdown')
            return
        # 将 internal_trans_list 保存为 Json 文件, 在 files/transactions 文件夹下保存文件, filename=hash_tx.json, 并用 send_file 发给用户
        file_path = f"files/transactions/{hash_tx}.json"
        with open(file_path, 'w') as f:
            json.dump(internal_trans_list, f, indent=2)
        bot.send_file(chat_id, file_path)
        bot.send_msg(
            f"亲爱的, 发的的这个看起来是一个智能合约交互的记录, 有点复杂, 我保存下来发给你看看吧. 我也看不明白, 建议你可以点击下面的链接去 Etherscan 页面上看看, 那边的解读清晰一点哈 😅, 抱歉我帮不了你啊, 我还不够厉害, 我还要继续学习, 继续努力。不行你把文件内容拷贝黏贴给 ChatGPT, 让他帮你解读一下这个智能合约的交互怎么回事, 是什么样的交互, 交易金额多大。\n\n{markdown_transaction_hash(hash_tx)}",
            chat_id, parse_mode='Markdown')
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
            bot.send_msg(r, chat_id, parse_mode='Markdown')

        # 检查 to_address 是否在 table avatar_eth_wallet, 如果在, 说明这是用户的充值地址, 需要本次交易的信息写入 avatar_crypto_payments
        from_id = get_from_id_by_eth_address(to_address)
        if from_id and from_id in [chat_id] + Params().BOT_OWNER_LIST:

            '''func_params:
            {"to": "0x5e278a70193F214C3536FD6f1D298a5eaeF52795", "value": 100.0, "status": true, "data": "0xa9059cbb0000000000000000000000005e278a70193f214c3536fd6f1d298a5eaef527950000000000000000000000000000000000000000000000000000000005f5e100", "from_address": "0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377", "from_addr_balance": 2512.718824, "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6, "coin": "USDC", "block_timestamp": "2023-03-11T22:25:59.000Z"}'''
            # 将最新获取的交易信息写入 avatar_crypto_payments
            try:
                func_params['value'] = 0 if not func_params['status'] else func_params['value']
                next_payment_time_dict = insert_into_avatar_crypto_payments(bot, from_id, coin, to_address,
                                                                            func_params['value'],
                                                                            func_params['block_timestamp'], hash_tx,
                                                                            user_title)
                return next_payment_time_dict
            except Exception as e:
                print(f"ERROR: insert_into_avatar_crypto_payments() failed: \n{e}")

    except Exception as e:
        logging.debug('get_transactions_info_by_hash_tx() error: ', e)
    return

# 计算用户下次需要续费的时间是哪天, 返回一个 datetime 对象
def update_user_next_payment_date(bot, user_from_id, user_title):
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
                x = value / Params().MONTHLY_FEE
                next_payment_time = crypto_payments.update_time + timedelta(days=x * 31)
                if next_payment_time > datetime.now():
                    next_payment_time_dict = {'last_paid_usd_value': value,
                                              'last_paid_time': crypto_payments.update_time,
                                              'next_payment_time': next_payment_time}
                    return next_payment_time_dict
            if crypto_payments.Hash_id: return get_transactions_info_by_hash_tx(bot, crypto_payments.Hash_id, user_from_id,
                                                                                user_title, chain='eth')
    return


def read_and_send_24h_outgoing_trans(bot, wallet_address, chat_id):
    # wallet_address = web3.to_checksum_address(wallet_address)
    transaction_list = read_outgoing_transaction_in_24h_result(wallet_address)
    if not transaction_list: return

    total_transactions_count = len(transaction_list)
    msg_info = f"亲爱的, {wallet_address[:5]}...{wallet_address[-5:]} 钱包地址 24 小时内一共有 {total_transactions_count} 笔 USDT/USDC 转出记录😍, 倒序排列如下: "
    bot.send_msg(msg_info, chat_id)
    if total_transactions_count > 10: transaction_list = transaction_list[:10]
    i = 0
    for transaction in transaction_list:
        i += 1
        r = '\n'.join([f"{k}: {v}" for k, v in transaction.items()])
        bot.send_msg(f"第{i}笔:\n{r}", chat_id, parse_mode='Markdown')
    if total_transactions_count > 10: bot.send_msg(
        f"还有 {total_transactions_count - 10} 笔转账记录, 请到 Etherscan 上查看哈:\n{markdown_wallet_address(wallet_address)}",
        chat_id, parse_mode='Markdown')
    return


def read_outgoing_transaction_in_24h_result(wallet_address):
    result = get_outgoing_transactions_from_address_in_24h(wallet_address)

    transaction_list = []

    for transaction in result['result']:
        if not transaction.get('logs'): continue

        decoded_event = transaction['logs'][0]['decoded_event']
        token_address = transaction['logs'][0]['address']
        if token_address.lower() not in [Params().USDT_ERC20.lower(), Params().USDC_ERC20.lower()]: continue

        token_name = 'USDT' if token_address.lower() == Params().USDT_ERC20.lower() else 'USDC'

        transfer_info = {}
        for param in decoded_event['params']:
            transfer_info[param['name']] = param['value']

        timestamp = convert_to_local_timezone(transaction['block_timestamp'])

        transaction_info = {
            '币种名称': token_name,  # Replace with your function to retrieve the token name
            '发起地址': markdown_wallet_address(transfer_info['from']),
            '收币地址': markdown_wallet_address(transfer_info['to']),
            '转账数量': format_number(int(transfer_info['value']) / (10 ** Params().USDT_ERC20_DECIMALS)),
            # Replace with your function to retrieve the token decimals
            '西岸时间': timestamp,
        }

        transaction_list.append(transaction_info)

    return transaction_list


def get_outgoing_transactions_from_address_in_24h(wallet_address):
    url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/verbose"

    # Get the date and time 24 hours ago
    from_date = datetime.now() - timedelta(days=1)
    from_date_formatted = datetime.strftime(from_date, "%Y-%m-%dT%H:%M:%S")

    headers = {
        'accept': 'application/json',
        'X-API-Key': Params().MORALIS_API,
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


def get_internal_transactions(transaction_hash):
    url = f"https://deep-index.moralis.io/api/v2/transaction/{transaction_hash}/internal-transactions?chain=eth"
    headers = {
        "accept": "application/json",
        "X-API-Key": Params().MORALIS_API
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


# 判断输入的 hash_tx 是否已经存在 avatar_crypto_payments 表中, 如果不存在, 则插入到表中
def insert_into_avatar_crypto_payments(bot, from_id, coin, to_address, value, timestamp, hash_tx, user_title):
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
            hash_tx_exists = session.query(sqlalchemy.exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
            if hash_tx_exists:
                print(f"DEBUG: hash_tx {hash_tx} 已经存在于 avatar_crypto_payments 表中, 但是 value 为 0, 不需要更新!")
                return

            update_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            new_crypto_payment = CryptoPayments(user_from_id=from_id, address=to_address, usdt_paid_in=0,
                                                usdc_paid_in=0, update_time=update_time, Hash_id=hash_tx)
            session.add(new_crypto_payment)
            session.commit()
            print(f"DEBUG: hash_tx {hash_tx} 已经插入到 avatar_crypto_payments 表中, value 为 0, 需要下次更新!")
            bot.send_msg(
                f"亲爱的, 你的交易 Transaction Hash {markdown_transaction_hash(hash_tx)} 已经系统被记录下来了, 但是链上还没有确认成功, 请过几分钟等下你再点击 /check_payment 试试看, 谢谢亲! 如果系统查到链上已确认, 你就不会收到这条消息了。\n\n如果你看到链上确认成功了, 但是等了太久我都没有给你确认, 或者你总是收到这条消息, 请联系 {Params().TELEGRAM_USERNAME} 手动帮你查看是否到账, 麻烦亲爱的了。😗",
                from_id, parse_mode='Markdown')
        return

    else:
        # Create a new session
        with Params().Session() as session:
            # Query the table 'avatar_crypto_payments' to check if the hash_tx exists
            hash_tx_exists = session.query(sqlalchemy.exists().where(CryptoPayments.Hash_id == hash_tx)).scalar()
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

            next_payment_time = update_time + timedelta(days=(value / Params().MONTHLY_FEE) * 31)
            if next_payment_time < datetime.now():
                mark_user_is_not_paid(from_id)
                return

            elif mark_user_is_paid(from_id, next_payment_time):
                bot.send_msg(
                    f"叮咚, {user_title} {from_id} 刚刚到账充值 {format_number(value)} {coin.lower()}\n\n充值地址: \n{markdown_wallet_address(to_address)}\n\n交易哈希:\n{markdown_transaction_hash(hash_tx)}",
                    Params().BOTOWNER_CHAT_ID, parse_mode='Markdown')
                bot.send_msg(
                    f"亲爱的, 你交来的公粮够我一阵子啦 😍😍😍, 下次交公粮的时间是: \n\n{next_payment_time} \n\n你可别忘了哦, 反正到时候我会提醒你哒, 么么哒 😘",
                    from_id)

                next_payment_time_dict = {'last_paid_usd_value': value, 'last_paid_time': update_time,
                                          'next_payment_time': next_payment_time}
                return next_payment_time_dict
    return


# 为输入的 eth address 生成一个二维码, 并保存到 files/images/eth_address 目录下, file_name 为 eth address, 如果文件夹不存在则创建, 如果文件已经存在则不再生成,
# 返回生成的二维码文件的路径或者已经存在的二维码文件的路径
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
        Base.metadata.create_all(bind=Params().engine)
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
