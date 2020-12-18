
from pymongo import MongoClient
import pandas as pd
import logging
import sys, time


API_KEY = 'SD6OYR6MFXCKTNQC'

# All available cryptocurrencies on alpha vantage
alpha_coins = pd.read_csv('../data/found_digital_currency_list.csv', dtype=str)

meta = pd.read_csv('../data/cryptocompare_metadata.csv', dtype=str)
meta = meta[['Id', 'ContentCreatedOn', 'Symbol', 'CoinName',
        'Algorithm', 'ProofType', 'FullyPremined', 'TotalCoinSupply',
        'Access', 'FCA', 'FINMA', 'Industry']] \
    .sort_values('TotalCoinSupply')
meta.head()

