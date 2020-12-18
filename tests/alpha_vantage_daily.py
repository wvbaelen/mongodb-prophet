#!/usr/bin/env python3
"""
On your terminal run:
pip install alpha_vantage

Links to the documentation:
https://github.com/RomelTorres/alpha_vantage
https://www.alphavantage.co/documentation/

Add to crontab file:
# m h d M dw
*/6 * * * *  $HOME/Develop/crypto/av_cron.bash
"""

from settings import API_KEY
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas as pd
import logging
import sys, time

logging.basicConfig(filename='../logs/alpha_vantage.log', filemode='a',
    format='%(asctime)s:%(levelname)s: %(message)s',
    datefmt='%H:%M:%S', level=logging.INFO)


# All available cryptocurrencies on alpha vantage
coins = pd.read_csv('../data/digital_currency_list.csv', dtype=str)

missing_coins = list(coins[coins.success.isna()]['currency code'].values)
if not missing_coins:
    # All crypto data has been successfully loaded
    sys.exit(0)

cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
# Make API call for each coin
for coin in missing_coins:
    try:
        # EUR market is not kept up to date, use USD
        data, meta = cc.get_digital_currency_daily(symbol=coin, market='CNY')
        data.to_csv(f'../output/{coin}_currency_daily.csv', index=True)

        logging.info(f'{data.index.min()} - {data.index.max()} ({coin})')

        coins.loc[coins['currency code'] == coin, ['success']] = '1'
        coins.to_csv(f'../data/digital_currency_list.csv', index=False)
    except ValueError as e:
        if 'Thank you for using Alpha Vantage!' in str(e):
            logging.error(f'Reached API call limit ({coin})')
            sys.exit(0)
        if 'Invalid API call' in str(e):
            logging.error(f'Invalid API call ({coin})')

            coins.loc[coins['currency code'] == coin, ['success']] = '0'
            coins.to_csv(f'../data/digital_currency_list.csv', index=False)
    except:
        logging.exception(f'Unknown error fetching {coin} data')
        sys.exit(1)
    
    time.sleep(0.5)

logging.info(f'Done')
