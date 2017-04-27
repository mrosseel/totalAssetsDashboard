import assetsMike as myAssets
import requests
from requests import ConnectionError
import numpy as np
import argparse
import time

def getStocks(verbose=False):
    r = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s={0}&f=l1'.format(','.join(myAssets.stocks)))
    text = r.text.split('\n')
    print text
    result = map(lambda x: float(str(x)), text[:-1])
    holdings = np.multiply(result,myAssets.stocks_amounts)
    total = sum(holdings)
    if verbose: print("stocks",total)
    return total

def getCrypto(verbose=False):
    total = 0
    krakeneur = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    btceur = float(str(krakeneur.json()['result']['XXBTZEUR']['c'][0]))
    total += myAssets.bitcoin * btceur
    crypto = requests.get('https://poloniex.com/public?command=returnTicker')
    for currency, amount in zip(myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts):
        lastcur = float(str(crypto.json()['BTC_{0}'.format(currency)]['last']))
        total += lastcur*amount*btceur
    if verbose: print("crypto",total)
    return total

def getPM(verbose=False):
    # gold
    gold = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/GOLD.json')
    try:
        goldpriceeur = float(str(gold.json()['data'][0][-1]))
    except ValueError as e:
        print "unable to fetch gold price"
        goldpriceeur = float(str(gold.json()['data'][0][-2]))
    except KeyError as e:
	print(gold.json())
	print "no gold data"
	goldpriceeur = 1000

    # silver
    try:
        silver = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/SILVER.json')
        silverdate = str(silver.json()['data'][0][0])
        silverpriceeur = float(str(silver.json()['data'][0][-1]))
    except KeyError as e:
        print "no silver data"
        silverpriceeur = 16

    total = myAssets.gold_ounces*goldpriceeur + myAssets.silver_ounces*silverpriceeur
    if verbose: print("pm",total)
    return total

def getOther(verbose=False):
    # cash euro
    total =  myAssets.cash_euro
    if verbose: print("cash_euro",total)
    return total

try:
    parser = argparse.ArgumentParser(description='Asset arguments.')
    parser.add_argument('--silent', dest='silent', action='store_true')
    parser.set_defaults(silent=False)
    args = parser.parse_args()
    verbose = not args.silent
    if verbose: print(time.strftime("%x %H:%M:%S"))
    print(getStocks(verbose)+getCrypto(verbose)+getPM(verbose)+getOther(verbose))
except ConnectionError as e:
    print "could not connect to internet"
