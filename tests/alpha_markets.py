
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas as pd
import logging
import sys, time


API_KEY = 'SD6OYR6MFXCKTNQC'

# All available cryptocurrencies on alpha vantage
coins = pd.read_csv('../data/digital_currency_list.csv', dtype=str)
missing_coins = list(coins[coins.success.isna()]['currency code'].values)

cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
fiats = pd.read_csv('../data/physical_currency_list.csv', dtype=str)
data, meta = cc.get_digital_currency_daily(symbol='ABT', market='CNY')

data = None
for market in list(fiats['currency code']):
    if data is None:
        try:
            data, meta = cc.get_digital_currency_daily(symbol='ABT', market=market)
            logging.info(f'getting data from {market} market worked')
        except:
            logging.error(f'getting data from {market} market failed')
