import assetsLibAmounts as lib
import time
import json
import connectWifi
import machine, ssd1306
import urequests
import time

import myAssets

def getOther(myAssets):
    # cash euro
    total =  myAssets.cash_euro
    return total

def printFullResult(name, value, total):
    printResult(name, value)
    printPercentage(value, total)

def printResult(name, value):
    print(prettyResult(name, value))

def prettyResult(name, value):
    return '{}:\t\t{:>7} EUR'.format(name, '{:.0f}'.format(value))

def prettyResultSmall(name, value, suffix=''):
    label = '{}:'.format(name)
    if(value > 100000):
        numbervalue = '{:>n}K'.format(round(value/1000.0))
    else:
        numbervalue = '{:>,n}'.format(round(value))
    spaces = 16 - len(label) - len(numbervalue) - len(suffix)
    filler = ''
    if spaces > 0:
        filler = ' '*spaces
    return label + filler + numbervalue + suffix

def printPercentage(value, total):
    print('\t\t({:>4} %)'.format('{:.1f}'.format(value/total*100)))

def printAll(verbose=True):
    current_prices_crypto = urequests.get('http://192.168.0.135:8081').json()
    stocks = lib.getStocks(myAssets.stocks, myAssets.stocks_amounts)
    crypto = lib.getCryptoPolo(current_prices_crypto, myAssets.bitcoin, myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts)
    other = getOther(myAssets)
    pm = lib.getPM(current_prices_crypto['goldeur'], current_prices_crypto['silvereur'], myAssets.gold_ounces, myAssets.silver_ounces)
    total = stocks+crypto+pm+other
    #printFullResult("stocks", stocks, total)
    #printFullResult("crypto", crypto, total)
    #printFullResult("pm", pm, total)
    #printFullResult("other", other, total)
    #printResult('Total', total)
    oled.fill(0)
    showOled(prettyResultSmall('Stocks', stocks), 0)
    showOled(prettyResultSmall('Crypto', crypto), 1)
    showOled(prettyResultSmall('PM', pm), 2)
    showOled(prettyResultSmall('Other', other), 3)
    showOled(prettyResultSmall('Total', total, ' EUR'), 4)
    showOled(current_prices_crypto['TIME'][:-3], 5)
    oled.show()
    #print()

def showOled(text, line):
    oled.text(text, 0, line*10)

def initWifiAndOled():
    connectWifi.connect(myAssets.ssid, myAssets.password)
    i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
    global oled
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def run():
    initWifiAndOled()
    oled.fill(0)
    oled.text('Loading prices ...', 0, 30)
    oled.show()
    verbose = False
    while True:
        printAll(verbose)
        time.sleep(60*10)

if __name__ == '__main__':
    run()
