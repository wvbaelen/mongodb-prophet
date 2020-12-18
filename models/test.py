
import pandas as pd
import cryptocompare
import json
import ta
import requests
from pymongo import MongoClient
from datetime import date, datetime
import logging
logging.basicConfig(level=logging.INFO)


# connect to the database
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']

# reading collection to a dataframe
import pandas as pd
import plotly.express as px

all_docs = list(db['Price_by_Day'].find({},
    {"_id": 0, "Symbol": 1, "time": 1, "open": 1, "close": 1,
     "high": 1, "low": 1, "volumeto": 1}))

df = pd.DataFrame(all_docs, index=None)
df['date'] = pd.to_datetime(df.time, unit='s')
df.head(20)

# plotting price graph
symbol = "BTC"
dfs = df.loc[(df.Symbol == symbol) & (df.close != 0),].sort_values('date')

final = ta.add_all_ta_features(dfs,
    "open", "high", "low", "close", "volumeto", fillna=True)
final = final[['date', 'open', 'high', 'low', 'close', 'volumeto',
    'trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'momentum_rsi']] \
        .sort_values('date').set_index('date')
final.plot()

normalized_df=(final-final.min())/(final.max()-final.min())
plt.figure(figsize=(20,12))
normalized_df.loc[normalized_df.index > "2019-01-01", ['date', 'open', 'volumeto',
    'trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'momentum_rsi']] \
        .plot(figsize=(16, 12))



import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.tools as tls
plotly_fig = tls.mpl_to_plotly(final.plot())


# plotting price graph
pdata = df.query(f'Symbol == {symbol}').sort_values('date')
fig = px.line(pdata, x='date', y='open')
fig.show()
