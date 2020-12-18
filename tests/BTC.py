
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib.pyplot as plt

cc = CryptoCurrencies(key='SD6OYR6MFXCKTNQC', output_format='pandas')
data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='EUR')

data.index.min()

data['4b. close (USD)'].plot()
plt.tight_layout()
plt.title('Daily close value for bitcoin (BTC)')
plt.grid()
plt.show()

data.to_csv('../data/BTC_currency_daily.csv')
