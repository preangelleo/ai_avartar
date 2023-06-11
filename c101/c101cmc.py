from c101variables import *

current_file = 'c101cmc.py'

class CMC:
    # https://coinmarketcap.com/api/documentation/v1/
    def __init__(self, token):
        self.api_url = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token, }
        self.session = Session()
        self.session.headers.update(self.headers)

    def getAllCoins(self):
        url = self.api_url + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data

    def getInfo(self, symbol):
        url = self.api_url + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        failed = False if r.json()['data'] else True
        if failed:
            message = f"CMC has no info for {symbol}"
            print(message)
            return {
                "code": 404,
                "msg": message
            }
        elif r.json()['data'][symbol]['quote']['USD']['fully_diluted_market_cap'] < 10000:
            message = f"Market cap is around 0"
            return {
                "code": 404,
                "msg": message
            }
        else:
            # print(json.dumps(r.json(), indent=2))
            volume_fdm = r.json()['data'][symbol]['quote']['USD']['volume_24h'] / \
                        r.json()['data'][symbol]['quote']['USD']['fully_diluted_market_cap']
            data = {
                'NAME': r.json()['data'][symbol]['name'],
                'PRICE': float(r.json()['data'][symbol]['quote']['USD']['price']),
                'VOLUME': math.floor(r.json()['data'][symbol]['quote']['USD']['volume_24h']),
                'PERCENTAGE': math.floor(r.json()['data'][symbol]['quote']['USD']['percent_change_24h']),
                'CAP': math.floor(r.json()['data'][symbol]['quote']['USD']['market_cap']),
                'FDM': math.floor(r.json()['data'][symbol]['quote']['USD']['fully_diluted_market_cap']),
                'RANK': int(r.json()['data'][symbol]['cmc_rank']) if str(r.json()['data'][symbol]['cmc_rank']).isnumeric() else 0,
                'V_FDM': format(volume_fdm, '.4f'),
                'CURRENT_TIME': r.json()['status']['timestamp']
            }
        return data

    def getDetail(self, symbol):
        time.sleep(0.2)
        url = self.api_url + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        if r.status_code != 200:
            print(f"{symbol} wrong with cmc check.")
            return
        elif not r.json()['data']:
            print(f"CMC = {symbol} has empty data.")
            return
        else:
            return r.json()

# cmc = CMC(CMC_PA_API)
cmc = CMC(CMC_PA_API)

# Replacement of Binance get_price function, in case some symbol is not listed in Binance.
def get_cmc_price(symbol):
    try:
        symbol = symbol.upper()
        data = cmc.getInfo(symbol)
        r = {
            'symbol': symbol.upper() + "USDT",
            'price': float(data['PRICE']) if 'code' not in data else 0
            }
        '''r = {'symbol': 'ETHUSDT', 'price': 1466.4717353959272}'''
        return r
    except Exception as e: 
        print(f"ERROR : get_cmc_price() failed for {symbol}, {e}")
        return


if __name__ == '__main__':
    print(f"{current_file} is running...")

    r = get_cmc_price('ETH')
    print(r)