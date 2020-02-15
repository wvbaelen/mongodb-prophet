#!/usr/bin/env python3
"""
On your terminal run:
pip3 install cryptocompare

Links to the documentation:
https://github.com/lagerfeuer/cryptocompare
https://min-api.cryptocompare.com/
"""

import pandas as pd
import cryptocompare
import datetime, json
from datetime import date


# connect to the database
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']

# get list of top cryptocoins by market cap
top_by_market_cap = db['Toplist_by_Market_Cap']
xs = top_by_market_cap.find({}, {'_id': 0, 'Symbol': 1})
symbols = [x['Symbol'] for x in xs]

# historical daily prices
toTs = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) \
    .timestamp() - (60 * 60 * 24)

for symbol in symbols:
    url = ("https://min-api.cryptocompare.com/data/v2/histoday" +
        "?fsym={}&tsym=USD&limit=1&toTs={}")
    response = requests.request("GET", url.format(symbol, toTs))
    data = json.loads(response.text)['Data']

    found_record = [x for x in data['Data'] if x['time'] == toTs]
    if found_record:
        found_record['createdAt'] = datetime.now().isoformat()
        db['Price_by_Daily'].insert_one(record)
