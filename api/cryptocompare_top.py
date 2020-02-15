#!/usr/bin/env python3

import cryptocompare
import requests, json
from pymongo import MongoClient
from datetime import datetime


# Time of update
current_time = datetime.now().isoformat()

# Full list of available coins on Cryptocompare
meta = cryptocompare.get_coin_list(format=False)

# Connect to MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']


# Top 100 Cryptocurrencies by Market Capitalization
response = requests.request("GET", params={"limit":"100", "tsym":"USD"},
    url="https://min-api.cryptocompare.com/data/top/mktcapfull")
data = json.loads(response.text)['Data']
top_market_caps = [x['CoinInfo']['Internal'] for x in data]

db['Toplist_by_Market_Cap'].drop()
values = {x: meta[x] for x in meta.keys() if x in top_market_caps}
for symbol in values:
    values[symbol]['CreatedOn'] = current_time
    db['Toplist_by_Market_Cap'].insert_one(values[symbol])

# Top 100 Cryptocurrencies by 24H Volume
response = requests.request("GET", params={"limit":"100", "tsym":"USD"},
    url="https://min-api.cryptocompare.com/data/top/totalvolfull?limit=100&tsym=USD")
top_volumes = [x['CoinInfo']['Internal'] for x in data]

db['Toplist_by_Volume'].drop()
values = {x: meta[x] for x in meta.keys() if x in top_volumes}
for symbol in values:
    values[symbol]['CreatedOn'] = current_time
    db['Toplist_by_Volume'].insert_one(values[symbol])
