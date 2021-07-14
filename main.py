from pycoingecko import CoinGeckoAPI
import requests
import os
import datetime
import time

cg = CoinGeckoAPI()

ethv_id = 'ethereum-volatility-index-token'
iethv_id = 'inverse-ethereum-volatility-index-token'
btcv_id = 'bitcoin-volatility-index-token'
ibtcv_id = 'inverse-bitcoin-volatility-index-token'

eth_pair = (ethv_id, iethv_id)
btc_pair = (btcv_id, ibtcv_id)

pairs = {
    'eth': eth_pair,
    'btc': btc_pair
}
def price(token):
    return cg.get_price(token, 'usd')[token]['usd']

def get_index(asset):
    query = '''
        query getImpliedVolatility {
          impliedVolatilitys(limit:1, offset: 0, query: {
            asset: ''' + asset.upper() + '''
          }, sort: "-epoch") {
            index
          }
        }
    '''

    resp = requests.post('https://api.volmex.finance/graphql', json={'query': query})
    data =resp.json()
    return data['data']['impliedVolatilitys'][0]['index']

CONVERSION_PRICE = 250

def pct_change(final, initial):
    return final/initial - 1

def run_asset(asset, long, short):
    print('---', asset, '---')
    long_price = price(long)
    short_price = price(short)
    total_price = long_price + short_price
    index_value = get_index(asset) * 100
    print('long =',long_price, '/ short =',short_price, '/ sum = ', total_price, '/ index = ', index_value)
    action = 'buy and redeem' if total_price < CONVERSION_PRICE else 'mint and sell'
    profit = abs(total_price - CONVERSION_PRICE)
    print('potential profit from', action, '= ${:0.2f} ({:0.2f}%)'.format(profit, pct_change(250, total_price)*100))
    print('long vol price off index by {:0.2f}%'.format(pct_change(long_price, index_value)*100))

    header = 'asof,asset,long,short,index\n' if not os.path.exists('data.csv') else ''
    asof = datetime.datetime.utcnow()
    with open('data.csv', 'a') as outf:
        outf.write(header)
        outf.write(f'{asof.isoformat()},{asset},{long_price},{short_price},{index_value}\n')

def run_one():
    assets = ['eth', 'btc']
    for asset in assets:
        run_asset(asset, *pairs[asset])

def main():
    run_one()


if __name__ == '__main__':
    main()

