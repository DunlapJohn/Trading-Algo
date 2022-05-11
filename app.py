import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st 
import pandas_datareader as web
import yfinance as yf
import requests
from bs4 import BeautifulSoup

st.set_page_config(
     page_title="Algo Trading",
     page_icon="",
     layout="wide"
 )


price_data = yf.download(tickers='BTC-USD', period = '24h', interval = '1h')


price_data.reset_index(level=0, inplace=True)


exp1 = price_data.Close.ewm(span=10, adjust=False).mean()
exp2 = price_data.Close.ewm(span=26, adjust=False).mean()


price_data['MACD'] = exp1-exp2

price_data['Signal Line'] = price_data['MACD'].ewm(span=9, adjust=False).mean()

price_data['Signal Change'] = price_data['Signal Line'].pct_change().fillna(0).round(2)
price_data['MACD Change']  = price_data['MACD'].pct_change().fillna(0).round(2)
price_data['Ind'] = np.where(price_data['MACD Change'] > 0, 1, 0)


price_data['Long'] = np.where( price_data['Signal Line'] < price_data['MACD'] , 1, 0 )
price_data['Short'] = np.where( price_data['Signal Line'] > price_data['MACD'], 1, 0 )

dfd=price_data['Short'].max()


price_data['Returns'] = price_data['Close'].pct_change()




short_returns= ((price_data['Returns']*-1) * price_data['Short'])
long_returns = (price_data['Returns']) * price_data['Long']



true = np.where(price_data['Long'] > 0,'Long','Short')

## idk maybe something here

# price_data[['Long',  'Long1','Short', 'Short1']]


price_data['MA7']=price_data.Close.rolling(7, min_periods=1).mean()

# price_data[['Date','Close', 'S', 'L']]
price_data[['index', 'Close', 'MACD', 'Signal Line']]
avg_rets = price_data['Returns'].sum()
avg_rets_long = long_returns.sum()
avg_rets_short = short_returns.sum()
totals = short_returns + long_returns
# Finding sums
long_returns=long_returns.sum()
short_returns=short_returns.sum()



true= true[-1]

# Portfolio value after time period and constant trading within the intervals

avg_rets_short = (avg_rets_short.round(3))
avg_rets_long = (avg_rets_long.round(3))
total = avg_rets_long + avg_rets_short
total = (total.round(3))








fig2, ax1 = plt.subplots()
plt.rcParams["figure.figsize"] = (8,3)
ax2 = ax1.twinx()
ax1.plot(price_data['index'],price_data['MACD'], label = 'MACD')
ax1.plot(price_data['index'],price_data['Signal Line'], label = 'Signal Line', c='g')
ax2.plot(price_data['index'],price_data['Close'], label = 'Price', c='y')
ax2.plot(price_data['index'],price_data['MA7'], label = 'MA7', c='r')
# ax1.plot(fastd, label = 'Asset', c='g')
# ax2.plot(fastk, label = 'Asset', c='g')
ax1.set_xlabel('Date and Hour')
ax1.set_ylabel(' ')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.axis() 
st.pyplot(fig2)

col1, col2, col3 , col4 = st.columns(4)
col1.metric(value =total, label = 'Total Portfolio Returns')
col3.metric(value =avg_rets_short, label = 'Total Short Returns ')
col2.metric(value =avg_rets_long, label = 'Total Long Returns ')
col4.metric(value =true, label = 'Current Action')



