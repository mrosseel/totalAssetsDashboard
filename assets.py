import myAssets as myAssets
import requests
from requests import ConnectionError
import numpy as np

def getStocks():
    r = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s={0}&f=l1'.format(','.join(myAssets.stocks)))
    text = r.text.split('\n')
    result = map(lambda x: float(str(x)), text[:-1])
    holdings = np.multiply(result,myAssets.stocks_amounts)
    total = sum(holdings)
    return total

def getCrypto():
    total = 0
    krakeneur = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    btceur = float(str(krakeneur.json()['result']['XXBTZEUR']['c'][0]))
    total += myAssets.bitcoin * btceur
    crypto = requests.get('https://poloniex.com/public?command=returnTicker')
    for currency, amount in zip(myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts):
        lastcur = float(str(crypto.json()['BTC_{0}'.format(currency)]['last']))
        total += lastcur*amount*btceur
    return total

def getPM():
    # gold
    gold = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/GOLD.json')
    golddate = str(gold.json()['data'][0][0])
    try:
        goldpriceeur = float(str(gold.json()['data'][0][-1]))
    except ValueError as e:
        print "unable to fetch gold price"
        goldpriceeur = 0


    # silver
    silver = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/SILVER.json')
    silverdate = str(silver.json()['data'][0][0])
    silverpriceeur = float(str(silver.json()['data'][0][-1]))

    return myAssets.gold_ounces*goldpriceeur + myAssets.silver_ounces*silverpriceeur

try:
    print(getStocks()+getCrypto()+getPM()+cash)
except ConnectionError as e:
    print "could not connect to internet"
