import assetsLibAmounts as lib
import argparse
import time
import locale
import json

import myAssets

def getOther(myAssets):
    # cash euro
    total =  myAssets.cash_euro
    return total

def printFullResult(name, value, total):
    printResult(name, value)
    printPercentage(value, total)

def printResult(name, value):
    print('{}:\t\t{:>7} EUR'.format(name, locale.format('%.0f', value, True, True)), end='')

def printPercentage(value, total):
    print('\t\t({:>4} %)'.format(locale.format('%.1f', value/total*100, True, True)))

def printAll(verbose=True):
    if verbose: print('Datetime:\t{}\n'.format(time.strftime("%x @ %H:%M:%S")))
    stocks = lib.getStocks(myAssets.stocks, myAssets.stocks_amounts)
    crypto = lib.getCryptoPolo(myAssets.bitcoin, myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts)
    other = getOther(myAssets)
    pm = lib.getPM(myAssets.gold_ounces, myAssets.silver_ounces)
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
        args = parser.parse_args()
        verbose = not args.silent
        printAll(verbose)
    except ConnectionError as e:
        print("could not connect to internet")

if __name__ == '__main__':
    run()
