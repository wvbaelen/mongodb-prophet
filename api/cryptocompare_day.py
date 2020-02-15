#!/usr/bin/env python3
"""
On your terminal run:
pip3 install cryptocompare

Links to the documentation:
https://github.com/lagerfeuer/cryptocompare
https://min-api.cryptocompare.com/

Start mongodb:
mongod --dbpath ~/data/db &
"""

import requests, json, datetime
from pymongo import MongoClient
from time import sleep
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)


# connect to the database
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']

# get list of top cryptocoins by market cap
top_by_market_cap = db['Toplist_by_Market_Cap']
xs = top_by_market_cap.find({}, {'_id': 0, 'Symbol': 1})
symbols = [x['Symbol'] for x in xs]

# historical daily prices
url = ("https://min-api.cryptocompare.com/data/v2/histoday" +
    "?fsym={}&tsym=USD&limit=2000{}")

# transfer cryptocompare data to mongodb
min_timestamp = ""
for symbol in symbols:
    logging.info(f"Processing {symbol}...")

    while True:
        toT = "&toTs={}".format(min_timestamp) if min_timestamp != "" else ""
        response = requests.request("GET", url.format(
            symbol, toT))
        data = json.loads(response.text)['Data']

        for record in data['Data']:
            record['Symbol'] = symbol
            db['Price_by_Day'].insert_one(record)

        min_timestamp = min(x['time'] for x in data['Data'])
        if min_timestamp < 0:
            break

# cleanup empty documents
btc_release = datetime(year=2009, month=1, day=1).timestamp()
db['Price_by_Day'].delete_many({"time": {"$lt": btc_release}})
