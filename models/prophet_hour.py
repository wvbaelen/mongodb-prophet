"""
pip install fbprophet lunarcalendar

Fixing prophet loading errors by replacing hdays.py:
https://raw.githubusercontent.com/facebook/prophet/master/python/fbprophet/hdays.py
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import matplotlib.pyplot as plt
import plotly.offline as py
py.init_notebook_mode()
import plotly.express as px

# connect to the database
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']


raw = pd.DataFrame(list(db['Price_by_Hour'].find({},
    {"_id": 0, "Symbol": 1, "time": 1, "open": 1, "close": 1,
     "high": 1, "low": 1, "volumeto": 1})), index=None)
raw['date'] = pd.to_datetime(raw.time, unit='s')

df = raw.loc[(raw.close != 0) & (raw.date > "2017-01-01 00:00:00")].sort_values('date')

buyOrSell = df[(df.high > df.over) | (df.high < df.over)]
buyOrSell['day'] = buyOrSell['date'].dt.date
buyOrSell['buy'] = buyOrSell.high > buyOrSell.over

# Buy/sell once a day
buyOrSell = buyOrSell.groupby('day').head(1)
buyOrSell.head()


# Plot with moving average confidence interval
n_steps = 24*5
df['smooth'] = df.high.rolling(n_steps).mean()
df['std'] = df.high.rolling(n_steps).std()

df = df.dropna()
df['under'] = df.smooth - 2.5*df['std']
df['over'] = df.smooth + 2.5*df['std']

fig = px.line(df, x='date', y='high')
fig.add_scatter(x=df['date'], y=df['over'], mode='lines')
fig.add_scatter(x=df['date'], y=df['under'], mode='lines')
fig.show()


# Simulations
bitcoin = 1
cash = 1000
pct = 0.90
last_action = 'buy'

for idx, row in buyOrSell.reset_index().iterrows():
    if row['buy'] and cash > 0 and last_action == 'sell':
        bitcoin = bitcoin + pct*cash/row['high']
        cash -= pct*cash
        last_action = 'buy'

    elif bitcoin > 0 and last_action == 'buy':
        cash = cash + pct*bitcoin*row['high']
        bitcoin -= pct*bitcoin
        last_action = 'sell'

print(f"cash: {cash + bitcoin * row['high']}")
print(f"BTC: {bitcoin + cash/row['high']}")






