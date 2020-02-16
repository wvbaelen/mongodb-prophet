"""
pip install fbprophet lunarcalendar

Fixing prophet loading errors by replacing hdays.py:
https://raw.githubusercontent.com/facebook/prophet/master/python/fbprophet/hdays.py
"""

import pandas as pd
from pymongo import MongoClient
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py
py.init_notebook_mode()


# connect to the database
client = MongoClient('127.0.0.1', 27017)
db = client['crypto']


raw = pd.DataFrame(list(db['Price_by_Day'].find({},
    {"_id": 0, "Symbol": 1, "time": 1, "open": 1, "close": 1,
     "high": 1, "low": 1, "volumeto": 1})), index=None)
raw['date'] = pd.to_datetime(raw.time, unit='s')

df = raw.loc[(raw.Symbol == "BTC") & (raw.close != 0),
# df = raw.loc[(raw.Symbol == "BCH") & (raw.close != 0),
# df = raw.loc[(raw.Symbol == "ETH") & (raw.close != 0),
    ["date", "close"]].sort_values('date')
df.columns = ['ds', 'y']
df.head(20)


# Train the model
m = Prophet(seasonality_mode='multiplicative', growth = 'linear',
    daily_seasonality = True, yearly_seasonality= True, weekly_seasonality=True)
m.fit(df.query('ds > "2015-01-01"'))

# Extend the datafame
future = m.make_future_dataframe(periods=365)
future.tail()


# Make predictions
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# Plot the forecast
fig1 = m.plot(forecast)

# See the forecast components
fig2 = m.plot_components(forecast)

# Plotly the forecast
fig = plot_plotly(m, forecast)
py.iplot(fig)

