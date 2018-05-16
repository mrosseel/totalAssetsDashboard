import assetsLibAmounts as lib
import server.assetsLibRaw as raw
import argparse
import time
import locale
import json
import common

import assetsMike as myAssets
#import assetsAnnelies as myAssets

def getOther(myAssets):
    # cash euro
    total =  myAssets.cash_euro
    return total

def printFullResult(name, value, total):
    printResult(name, value)
    printPercentage(value, total)

def printFullCryptoResult(name, value, total, distrib):
    printResult(name, value)
    printPercentage(value, total, '')
    for coin, coinvalue in distrib:
        print(' | ' + coin + ":" + common.getSmallNumberValue(coinvalue) + '={:>4}%'.format(locale.format('%.1f', coinvalue/value*100, True, True)), end = '')
    print()

def printResult(name, value):
    print('{}:\t\t{:>7} EUR'.format(name, locale.format('%.0f', value, True, True)), end='')

def printPercentage(value, total, endChar='\n'):
    print('\t\t({:>4} %)'.format(locale.format('%.1f', value/total*100, True, True)), end=endChar)

def printAll(verbose=True):
    if verbose: print('Datetime:\t{}\n'.format(time.strftime("%x @ %H:%M:%S")))
    #stocks = lib.getStocks(myAssets.stocks, myAssets.stocks_amounts)
    stocks = 0
    cryptoDistrib = lib.getCryptoPolo(raw.getCryptoRaw(), myAssets.bitcoin, myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts)
    crypto = cryptoDistrib[0]
    other = getOther(myAssets)
    pm_raw = raw.getPMRaw()
    pm = lib.getPM(pm_raw['goldeur'], pm_raw['silvereur'], myAssets.gold_ounces, myAssets.silver_ounces)
    total = stocks+crypto+pm+other
    printFullResult("stocks", stocks, total)
    printFullCryptoResult("crypto", crypto, total, cryptoDistrib[1])
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
        args = parser.parse_args()
        verbose = not args.silent
        printAll(verbose)
    except ConnectionError as e:
        print("could not connect to internet")

if __name__ == '__main__':
    run()
