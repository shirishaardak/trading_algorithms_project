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

#----- Data

#df = yf.download(tickers='^NSEBANK', period='30d' , interval='15m')

df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')

#df.reset_index(inplace = True)

#-----technical_indicators
#df = heikin_ashi(df)

df['SAM-10'] = ta.sma(close=df['Close'], length=25)
df['SAM-20'] = ta.sma(close=df['Close'], length=50)
df['SAM-30'] = ta.sma(close=df['Close'], length=30)
df['SAM-200'] = ta.sma(close=df['Close'], length=200)
df['ADX_14'] = ta.adx(high=df.High, low=df.Low, close=df.Close, length=14)['ADX_14']



#--------- Buy and Sell 
buy=[]
sell=[]

investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['Close'][i] > df['Close'][i-1]) &  (df['SAM-10'][i] > df['SAM-20'][i]) &  (df['ADX_14'][i] > 30)  & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
                buy.append(i)
            elif (df['Close'][i] < df['SAM-20'][i])  & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
                buy.append(i)
            elif (df['Close'][i] < df['Close'][i-1]) &  (df['SAM-10'][i] < df['SAM-20'][i]) &  (df['ADX_14'][i] > 30) & (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
                sell.append(i)
            elif (df['Close'][i] > df['SAM-20'][i])  & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])
                sell.append(i)


bt.trade_transaction('SAM-9_and_SAM-18')
bt.Backtest_report(df, investment, "SAM-9_and_SAM-18", 15)

#-----Ploting Data
fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1750)
fig.add_trace(go.Scatter(x=df.iloc[buy].index, y=df.iloc[buy]['Close'], mode="markers", marker_size=15, marker_color='green'),)
fig.add_trace(go.Scatter(x=df.iloc[sell].index, y=df.iloc[sell]['Close'], mode="markers", marker_size=15, marker_color='red'),)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-10']),)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-200']),)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.write(fig)