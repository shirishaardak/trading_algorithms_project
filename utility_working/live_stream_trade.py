import numpy as np  
import pandas as pd  
import plotly.graph_objects as go 
import streamlit as st  
import sys
sys.path.insert(0, 'D:/trading_algorithms_project/paper_trading/')
from scipy.signal import argrelextrema
import yfinance as yf
from utility.backtesting import Backtest
from streamlit_autorefresh import st_autorefresh
from datetime import datetime


now = datetime.now()

current_time = now.strftime("%H:%M:%S")

# update every 5 mins

st.set_page_config(layout="wide")


df = yf.download(tickers="^NSEBANK",
                            period="5d",
                            interval="15m",
                            auto_adjust=True)

    
# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater, order=21)[0]
min_idx = argrelextrema(df['Close'].values, np.less, order=21)[0]

#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['Close']
df['max_low'] = df.iloc[min_idx]['Close']

max_high = 42500
max_low = 42500
df['trand-line'] = 42500
trand = 42500


for i in range(1, len(df)):
    if df['Close'][i-1] == df['max_high'][i-1]:
        trand = df['High'][i]
        df['trand-line'][i] = df['High'][i]
    elif df['Close'][i-1] == df['max_low'][i-1]:
        trand = df['Low'][i]
        df['trand-line'][i] = df['Low'][i]
    else:
        df['trand-line'][i] = trand

lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['Close'][i] > df['trand-line'][i]) & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, buy_sell='Buy', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] < df['trand-line'][i])  & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
            elif (df['Close'][i] < df['trand-line'][i]) & (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] > df['trand-line'][i]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])
bt.trade_transaction('high_low_paper_trade')
bt.Backtest_report(df, 500000, "high_low_paper_trade_repot", 15)

print(bt)
        
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1650)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
fig.update_xaxes(type='category')
fig.update_yaxes(fixedrange=False)

st.title(current_time)

st.write(fig, use_container_width=True)

st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")