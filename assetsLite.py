import assetsLibAmounts as lib
import time
import json
import connectWifi
import machine, ssd1306

import urequestsimport utime as time
import gc
import common

import mikeAssets as myAssets

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

def printPercentage(value, total):
    print('\t\t({:>4} %)'.format('{:.1f}'.format(value/total*100)))

def printAll(verbose=True):
    gc.enable()
    gc.collect()
    print('Before Free mem', gc.mem_free())
    current_prices_crypto = urequests.get('http://total-assets.appspot.com').json()
    stocks = lib.getStocks(myAssets.stocks, myAssets.stocks_amounts)
    cryptodistrib = lib.getCryptoPolo(current_prices_crypto, myAssets.bitcoin, myAssets.crypto_poloniex, myAssets.crypto_poloniex_amounts)
    crypto = cryptodistrib[0]
    other = getOther(myAssets)
    pm = lib.getPM(current_prices_crypto['goldeur'], current_prices_crypto['silvereur'], myAssets.gold_ounces, myAssets.silver_ounces)
    total = stocks+crypto+pm+other
    print('After Free mem', gc.mem_free())
    gc.collect()
    print('After GC Free mem', gc.mem_free())
    oled.fill(0)
    oledLine(common.prettyResultSmall('Stocks', stocks), 0)
    oledLine(common.prettyResultSmall('Crypto', crypto), 1)
    oledLine(common.prettyResultSmall('PM', pm), 2)
    oledLine(common.prettyResultSmall('Other', other), 3)
    oledLine(common.prettyResultSmall('Total', total, ' EUR'), 4)
    timestring = current_prices_crypto['TIME'][:-3]
    hour = int(timestring[:2])
    correctedhour = hour + myAssets.timezone
    oledLine(str(correctedhour)+timestring[2:], 5)
    oled.show()
    #print()

def oledLine(text, line):
    oled.text(text, 0, line*10)

def oledLineFull(text, line):
    oled.fill(0)
    oled.text(text, 0, line*10)
    oled.show()

def initWifiAndOled():
    i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
    global oled
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oledLineFull('Connect wifi...', 3)
    connectWifi.connect(myAssets.ssid, myAssets.password)

def run():
    initWifiAndOled()
    oledLineFull('Load prices...', 3)
    verbose = False
    toggle = True
    while True:
        try:
            printAll(verbose)
            for x in range(0, 600):
                oled.text('\\' if toggle else '/', 60, 50, 0)
                oled.show()
                oled.text('/' if toggle else '\\', 60, 50)
                oled.show()
                toggle = not toggle
                time.sleep(1)
        except Exception as e:
            print('Exception occured:',type(e), e.args, e)
            oledLineFull('Error, 1s sleep', 3)
            print('error')


if __name__ == '__main__':
    run()
