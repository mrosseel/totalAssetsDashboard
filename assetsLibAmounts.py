import assetsLibRaw as lib

def getStocks(myStocks, myStocksAmount):
    total = 0
    result = lib.getStocksRaw(','.join(myStocks))
    holdings = [a*b for a,b in zip(result, myStocksAmount)]
    total = sum(holdings)
    return total

def getCryptoPolo(current_prices, bitcoin, myPoloniexCrypto, myPoloniexAmounts):
    total = 0
    eurbtc = current_prices['EUR_BTC']
    total += bitcoin * eurbtc
    for currency, amount in zip(myPoloniexCrypto, myPoloniexAmounts):
        total += current_prices['BTC_'+currency]*amount*eurbtc
    return total

def getPM(goldeur, silvereur, gold_ounces, silver_ounces):
    return gold_ounces*goldeur + silver_ounces*silvereur
