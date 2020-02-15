#!/usr/bin/env python3
"""
Link to the documentation:
https://alternative.me/crypto/fear-and-greed-index/#fng
"""

import requests, json
import pandas as pd


# Make Fear and Greed API call
url = "https://api.alternative.me/fng/"
querystring = {"limit":"0", "format":"json", "date_format":"cn"}
response = requests.request("GET", url, params=querystring)

# Parse response and write to csv
data = json.loads(response.text)['data']
df = pd.DataFrame.from_dict(data).set_index('timestamp')
del df['time_until_update']

df.to_csv(f'../data/fear_and_greed_index.csv', index=True)
