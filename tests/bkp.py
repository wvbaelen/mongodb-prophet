

len(list(db['Price_by_Day'].find({"time": {"$gte": btc_release}})))  # 406.500
len(list(db['Price_by_Day'].find()))  # 2.001.000
len(list(db['Price_by_Day_Filter'].find()))  # 2.001.000

data = db['Price_by_Day'].find({"time": {"$gte": btc_release}})

x = 1
for record in data:
    logging.info(x)
    if x == 10:
        break
    x += 1
    #db['Price_by_Day_Filter'].insert_one(record)


db.clone

symbol = "BTC"
list(db['Toplist_by_Market_Cap'].find().limit(2))

querystring = '{"fsym":"BTC","tsym":"USD","limit":2000{},"toTs":{timestamp}'

while  min_timestamp > 0:

    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)['Data']
    values = data['Data']

    for record in data['Data']:
        record['Symbol'] = symbol
        db['Price_by_Day'].insert_one(record)
    
    min_timestamp = min(x['time'] for x in data['Data'])

    logging.error(data['Data'][0]['time'])
    sleep(0.2)


# TODO: cleanup + terminate and clean zero's

response = cryptocompare.get_historical_price_day('BTC', curr='USD', limit=1440)





# copying collections
btc_release = datetime(year=2009, month=1, day=1).timestamp()
docs = db['Price_by_Day'].find({"time": {"$gte": btc_release}})
db['Price_by_Day_Filter'].insert_many(docs)
db['Price_by_Day_Filter'].drop()


# reading collection to a dataframe
import pandas as pd
import plotly.express as px

all_docs = list(db['Price_by_Day_Filter'] \
    .find({}, {"_id": 0, "Symbol": 1, "time": 1, "open": 1, "close": 1}))

df = pd.DataFrame(all_docs, index=None)
df['date'] = pd.to_datetime(df.time, unit='s')
df.head(20)

# plotting price graph
pdata = df.query('Symbol == "BTC"').sort_values('date')
fig = px.line(pdata, x='date', y='open')
fig.show()

