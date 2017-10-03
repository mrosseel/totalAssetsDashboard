import urequests
import argparse
import time
import locale
import json

# arg is array of stocks
def getStocksRaw(myStocks):
    r = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s={0}&f=l1'.format(myStocks))
    text = r.text.split('\n')
    result = list(map(lambda x: float(str(x)), text[:-1]))
    return result

def getStocks(myStocks):
    total = 0
    result = getStocksRaw(','.join(myStocks))
    holdings = [a*b for a,b in zip(result, myAssets.stocks_amounts)]
    total = sum(holdings)
    return total

def getCryptoRaw(myPoloniexCrypto):
    krakeneur = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    btceur = float(str(krakeneur.json()['result']['XXBTZEUR']['c'][0]))
    crypto = requests.get('https://poloniex.com/public?command=returnTicker')
    result = {'btceur': btceur}
    for currency in myAssets.crypto_poloniex:
        result[currency] = float(str(crypto.json()['BTC_{0}'.format(currency)]['last']))
    return result

def getCrypto(myPoloniexCrypto):
    total = 0
    dictresult = getCryptoRaw(myPoloniexCrypto)
    btceur = dictresult['btceur']
    del dictresult['btceur']
    total += myAssets.bitcoin * btceur
    for currency, amount in zip(myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts):
        total += dictresult[currency]*amount*btceur
    return total

def getPMRaw():
    # gold
    gold = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/GOLD.json')
    try:
        goldpriceeur = float(str(gold.json()['data'][0][-1]))
    except ValueError as e:
        try:
            goldpriceeur = float(str(gold.json()['data'][0][-2]))
        except:
            goldpriceeur = 1000
    except KeyError as e:
        print(gold.json())
        print("no gold data")
        goldpriceeur = 1000

    # silver
    try:
        silver = requests.get('https://www.quandl.com/api/v1/datasets/LBMA/SILVER.json')
        silverdate = str(silver.json()['data'][0][0])
        silverpriceeur = float(str(silver.json()['data'][0][-1]))
    except KeyError as e:
        print("no silver data")
        silverpriceeur = 16
    return {'goldeur': goldpriceeur, 'silvereur': silverpriceeur}

def getPMRawJson():
    return json.dumps(getPMRaw())

def getPM(verbose=False):
    dictresult = getPMRaw()
    total = myAssets.gold_ounces*dictresult['goldeur'] + myAssets.silver_ounces*dictresult['silvereur']
    return total

def getOther(verbose=False):
    # cash euro
    total =  myAssets.cash_euro
    #printResult("Cash", total)
    return total

def printFullResult(name, value, total):
    printResult(True, name, value)
    printPercentage(True, value, total)

def printResult(name, value):
    print('{}:\t\t{:>7} EUR'.format(name, locale.format('%.0f', value, True, True)), end='')

def printPercentage(value, total):
    print('\t\t({:>4} %)'.format(locale.format('%.1f', value/total*100, True, True)))

def printAll(verbose=True):
    if verbose: print('Datetime:\t{}\n'.format(time.strftime("%x @ %H:%M:%S")))
    stocks = getStocks(myAssets.stocks)
    crypto = getCrypto(myAssets.crypto_poloniex)
    other = getOther()
    pm = getPM()
    total = stocks+crypto+pm+other
    printFullResult("stocks", stocks, total)
    printFullResult("crypto", crypto, total)
    printFullResult("pm", pm, total)
    printFullResult("other", other, total)
    printResult('Total', total)
    print()

def run():
    try:
        locale.setlocale(locale.LC_ALL, 'de_DE')
        parser = argparse.ArgumentParser(description='Asset arguments.')
        parser.add_argument('--silent', dest='silent', action='store_true')
        parser.set_defaults(silent=False)
        parser.add_argument('--myAssets', dest='myAssets', nargs = 1, action='store', required=True)
        parser.set_defaults(silent=False)
        args = parser.parse_args()
        verbose = not args.silent
        myAssets = args.myAssets
        printAll(verbose)
    except ConnectionError as e:
        print("could not connect to internet")

if __name__ == '__main__':
    run()
