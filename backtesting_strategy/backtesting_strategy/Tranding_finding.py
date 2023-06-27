import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
from datetime import datetime, date
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema
import plotly.graph_objects as go 
import yfinance as yf
from utility.backtesting import Backtest
import pandas_ta as ta
import streamlit as st  
from streamlit_autorefresh import st_autorefresh



now = datetime.now()
current_time = now.strftime("%H:%M:%S")

df = yf.download(tickers='^NSEBANK', period='30d' , interval='15m')

max_idx = argrelextrema(df['High'].values, np.greater_equal, order=11)[0]
min_idx = argrelextrema(df['Low'].values, np.less_equal, order=11)[0]

df['max_high'] = df.iloc[max_idx]['High']
df['max_low'] = df.iloc[min_idx]['Low']
df['max_high'] = df['max_high'].fillna(method='ffill')
df['max_low']= df['max_low'].fillna(method='ffill')

df['trand-line'] = df['Close'].iloc[0]
trand = df['Close'].iloc[0]


for i in range(len(df)):
    if df['High'][i] == df['max_high'][i] or df['Close'][i] < df['max_high'][i-1]:
        trand = df['max_high'][i-1]
        df['trand-line'][i] = df['max_high'][i-1]    
    elif df['Low'][i] == df['max_low'][i] or df['Close'][i] > df['max_low'][i-1]:
        trand = df['max_low'][i-1]
        df['trand-line'][i] = df['max_low'][i-1]    
    else:
        df['trand-line'][i] = trand


investment = 500000
lot_size= 25  
position = 0
bt = Backtest()
buy_Trget = 0
sell_Trget =0 

for i in range(len(df)):
            if(df['Close'][i] > df['trand-line'][i-1]) & (position == 0):
                position = 1               
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] < df['trand-line'][i]) & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
            elif (df['Close'][i] < df['trand-line'][i-1]) &  (position == 0):
                position = -1                
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] > df['trand-line'][i]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])


bt.trade_transaction('High-Low-15min')
bt.Backtest_report(df, investment, "High-Low-15min", 15)

# ------ Create indicator ------ #


fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1800)
#fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['max_high_low'], marker=dict(color='Blue',size=12,), name="Buy"), row=1, col=1)
#fig.add_trace(go.Scatter(mode='markers', x=df.iloc[min_idx].index, y=df.iloc[min_idx]['Low'], marker=dict(color='Red',size=12,), name="Sell"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']))
fig.add_trace(go.Scatter(x=df.index, y=df['max_high'], marker=dict(color='green',size=3,)))
fig.add_trace(go.Scatter(x=df.index, y=df['max_low'], marker=dict(color='red',size=3,)))
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")