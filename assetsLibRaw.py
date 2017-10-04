
import gc

try:
    import urequests
except ImportError:
    import requests as urequests

# arg is array of stocks
def getStocksRaw(myStocks):
    r = urequests.get('http://download.finance.yahoo.com/d/quotes.csv?s={0}&f=l1'.format(myStocks))
    text = r.text.split('\n')
    result = list(map(lambda x: float(str(x)), text[:-1]))
    return result

def getCryptoRaw(myPoloniexCrypto):
    krakeneur = urequests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    btceur = float(str(krakeneur.json()['result']['XXBTZEUR']['c'][0]))
    krakeneur = ""
    gc.enable()
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    crypto = urequests.get('https://poloniex.com/public?command=returnTicker')
    print(dir(crypto))
    gc.collect();
    cryptojson = crypto.json()
    crypto = ""

    result = {'btceur': btceur}
    for currency in myPoloniexCrypto:
        result[currency] = float(str(cryptojson['BTC_{0}'.format(currency)]['last']))
    return result

def getCryptoRaw():
    krakeneur = urequests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    btceur = float(str(krakeneur.json()['result']['XXBTZEUR']['c'][0]))
    krakeneur = ""
    crypto = urequests.get('https://poloniex.com/public?command=returnTicker')
    cryptojson = crypto.json()
    crypto = ""
    result = {'EUR_BTC': btceur}
    for currency in cryptojson:
        result[currency] = float(str(cryptojson[currency]['last']))
    return result

def getPMRaw():
    # gold
    gold = urequests.get('https://www.quandl.com/api/v1/datasets/LBMA/GOLD.json')
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
        silver = urequests.get('https://www.quandl.com/api/v1/datasets/LBMA/SILVER.json')
        silverdate = str(silver.json()['data'][0][0])
        silverpriceeur = float(str(silver.json()['data'][0][-1]))
    except KeyError as e:
        print("no silver data")
        silverpriceeur = 16
    return {'goldeur': goldpriceeur, 'silvereur': silverpriceeur}
