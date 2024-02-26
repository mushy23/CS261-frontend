from prophet import Prophet
import pandas as pd
import yfinance as yf
from prophet.plot import plot_plotly, plot_components_plotly
from sklearn.metrics import mean_squared_error,mean_absolute_error

import matplotlib
import matplotlib.pyplot as plt


# Load your stock price data into a pandas DataFrame
# Assuming 'features' contains your feature columns and 'target' is the target variable (stock prices)
# Replace this with your actual data loading and preprocessing steps

matplotlib.use("TkAgg")
# Replace 'AAPL' with the stock symbol of your choice
stock_symbol = 'AAPL'

# Download historical stock data
stock_data = yf.download(stock_symbol, start='2010-01-01', end='2022-12-31')
stock_data.head()

features = stock_data[['Open', 'High', 'Low', 'Volume']]


features.rename(index={0: "ds", 1: "ds"})
help = stock_data['Close']
target = pd.DataFrame(help)

df = target.reset_index().rename(columns={'index': 'ds', 'Date' : 'ds', 'Close': 'y'})

print(df)

m = Prophet()
m.fit(df)


future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())


m.plot(forecast)

#fig1 = m.plot(forecast)
plt.show()

train = df.drop(df.index[-12:])
print(train.tail())

y_true = df['y'][-12:].values
y_pred = forecast['yhat'][-12:].values
mae = mean_absolute_error(y_true, y_pred)
print('MAE: %.3f' % mae)

# plot expected vs actual
plt.plot(y_true, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.show()

