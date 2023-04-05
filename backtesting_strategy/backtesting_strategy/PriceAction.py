import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
import streamlit as st  
import yfinance as yf
import pandas_ta as ta
from utility.technical_indicators import heikin_ashi
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from scipy.signal import argrelextrema
from utility.backtesting import Backtest


df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')

# ------ Create indicator ------ #

df['max_high'] =  df['Close'].rolling(9).max()
df['max_low'] =  df['Close'].rolling(9).min()
df['max_high'].fillna(method='pad', inplace=True)
df['max_low'].fillna(method='pad', inplace=True)

df['trand-line'] = df['Close'].iloc[0]
trand = df['Close'].iloc[0]

for i in range(len(df)):
        if df['Close'][i] > df['max_high'][i]:
            trand = df['max_low'][i]
            df['trand-line'][i] = df['max_low'][i]
        elif df['Close'][i] < df['max_low'][i]:
            trand = df['max_high'][i-1]
            df['trand-line'][i] = df['max_high'][i]
        else:
            df['trand-line'][i] = trand


investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['Close'][i] > df['trand-line'][i-1]) & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] < df['trand-line'][i-1]) & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
            elif (df['Close'][i] < df['trand-line'][i-1])  & (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] > df['trand-line'][i-1]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])


bt.trade_transaction('rolling_higher_high_lower_low_21')
bt.Backtest_report(df, investment, "rolling_higher_high_lower_low_21", 15)

#-----Ploting Data
fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1750)
# fig.add_trace(go.Scatter(x=df.iloc[max_idx].index, y=df.iloc[max_idx]['Close'], mode="markers", marker_size=15, marker_color='green'),)
# fig.add_trace(go.Scatter(x=df.iloc[min_idx].index, y=df.iloc[min_idx]['Close'], mode="markers", marker_size=15, marker_color='red'),)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
#fig.add_trace(go.Scatter(x=df.index, y=df['SAM-18']),)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.write(fig)