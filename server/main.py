import webapp2

import assetsLibRaw as assets
import json
import time
import datetime
from datetime import timedelta

import requests
import requests_toolbelt.adapters.appengine
from google.appengine.api import memcache

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

# [START get_data]
def get_data():
    data = memcache.get('key')
    if data is not None:
        return data
    else:
        data = query_for_data()
        memcache.add('key', data, 60)
    return data
# [END get_data]

def getCrypto():
    crypto = memcache.get('crypto')
    if crypto is None:
        crypto = assets.getCryptoRaw()
        # cache crypto results for 5 mins
        memcache.add(key="crypto", value=json.dumps(crypto), time=300)
        memcache.add(key="crypto_time", value=getTime(), time=300)
    else:
        crypto = json.loads(crypto)
    return crypto

def getPM():
    pm = memcache.get('pm')
    if pm is None:
        pm = assets.getPMRaw()
        # cache pm results for 1h
        memcache.add(key="pm", value=json.dumps(pm), time=3600)
        memcache.add(key="pm_time", value=getTime(), time=3600)
    else:
        pm = json.loads(pm)
    return pm

def getTime():
    return '{}'.format(time.strftime("%H:%M:%S"))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        message = getCrypto()
        gold_silver = getPM()
        message['TIME'] = getTime()
        message['goldeur'] = gold_silver['goldeur']
        message['silvereur'] = gold_silver['silvereur']

        # Write content as utf-8 data
        self.response.write(json.dumps(message))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
