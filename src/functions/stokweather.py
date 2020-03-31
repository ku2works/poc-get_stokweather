#!/use/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse, os, sys, logging, datetime, json, re, traceback
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "vendor"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import requests
from datetime import datetime
import pytz

def lambda_handler(event, context):
    try:
      code = os.environ.get("StockweatherCode")
      key = os.environ.get("StockweatherKey")
      url = "https://www.stockweather.co.jp/signage/json/getjsondata.aspx?code=%s&key=%s" % (code, key)

      expires = datetime.now().timestamp() + 36000
      dt = datetime.fromtimestamp(expires, tz=pytz.timezone("GMT"))
      headers = {
        "Last-Modified": "Fri Jan 01 2010 00:00:00 GMT",
        "Expires": dt.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        "Cache-Control": "private, max-age=36000",
        "Pragma": ""
      }
      r = requests.get(url, headers=headers)

      return {
        "statusCode": r.status_code,
        "isBase64Encoded": False,
        "body": r.text,
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "Content-Type",
          "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
      }
    except Exception as e:
      print(e)

if __name__ == "__main__":
    lambda_handler(None, None)
