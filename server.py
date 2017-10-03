#!/usr/bin/env python
import assetsLibRaw as assets
import json
import time
import datetime
from datetime import timedelta

from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  last_pm_datetime = datetime.datetime.now()
  gold_silver = assets.getPMRaw()
  delta_1hour = timedelta(hours=1)

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        current_time = '{}'.format(time.strftime("%H:%M:%S"))
        # Send message back to client
        message = assets.getCryptoRaw()
        # only update PM every hour
        if datetime.datetime.now() - last_pm_datetime > delta_1hour:
            last_pm_datetime = datetime.datetime.now()
            gold_silver = assets.getPMRaw()
        message['TIME'] = current_time
        message['goldeur'] = gold_silver['goldeur']
        message['silvereur'] = gold_silver['silvereur']
        # Write content as utf-8 data
        self.wfile.write(bytes(json.dumps(message), "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
