import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import streamlit as st  
import yfinance as yf
from plotly.subplots import make_subplots
import pandas_ta as ta
from utility.backtesting import Backtest
from utility.technical_indicators import heikin_ashi
from scipy.signal import argrelextrema

#----- df

#df = yf.download(tickers='^NSEBANK', period='10d' , interval='15m')

df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/historical_data_nifty_bank_5minute.csv', index_col='Date')
#-----technical_indicators
df = ta.ha(open_=df.Open, high=df.High, low=df.Low, close=df.Close,)
df['SUPERT_10_3.0'] = ta.supertrend(high=df.HA_high, low=df.HA_low, close=df.HA_close, length=10, multiplier=3)['SUPERT_10_3.0']
df['SAM-9-High'] = ta.sma(close=df['HA_high'], length=9)
df['SAM-9-Low'] = ta.sma(close=df['HA_low'], length=9)
df['ATR'] = ta.atr(high=df.HA_high, low=df.HA_low, close=df.HA_close, length=14)
df['ATR-20'] = ta.sma(close=df['ATR'], length=20)

buy=[]
sell=[]

investment = 500000
lot_size= 25  
position = 0
bt = Backtest()
buy_Trget = 0
sell_Trget =0 

for i in range(len(df)):
            if(df['HA_close'][i] > df['SAM-9-High'][i]) & (df['ATR'][i]  > df['ATR-20'][i])  & (position == 0):
                position = 1               
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['HA_close'][i], exit_price=0)
                buy.append(i)
            elif (df['HA_close'][i] < df['SAM-9-Low'][i]) & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['HA_close'][i])
                buy.append(i)
            elif (df['HA_close'][i] < df['SAM-9-Low'][i]) & (df['ATR'][i]  > df['ATR-20'][i]) &  (position == 0):
                position = -1                
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['HA_close'][i], exit_price=0)
                sell.append(i)
            elif (df['HA_close'][i] > df['SAM-9-High'][i]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['HA_close'][i])
                sell.append(i)


bt.trade_transaction('SAM-9-High-Low-15min')
bt.Backtest_report(df, investment, "SAM-9-High-Low-15min", 5)

#-----Ploting df
fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-9-High']),)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-9-Low']),)
fig.update_yaxes(fixedrange=False)
st.set_page_config(layout="wide")
st.write(fig)