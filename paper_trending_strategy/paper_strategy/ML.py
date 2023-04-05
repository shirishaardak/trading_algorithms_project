import os
os.chdir(r'D:\\trading_algorithms_project\\paper_trending_strategy')
import pandas as pd
import numpy as np
import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from scipy.signal import argrelextrema
import pandas_ta as ta
from utility.technical_indicators import heikin_ashi
import yfinance as yf
from datetime import datetime

now = datetime.now()


current_time = now.strftime("%H:%M:%S")


df = yf.download(tickers='JPY=X', period='1d' , interval='5m')

# ------ Create indicator ------ #
df['EMA-21'] = ta.ema(close=df['Close'], length=21)
df['max_high'] = np.where(df['Close'] == df['Close'].rolling(9).max(), df['Close'], None)
df['max_low'] = np.where(df['Close'] == df['Close'].rolling(9).min(), df['Close'], None)
df['max_high'].fillna(method='pad', inplace=True)
df['max_low'].fillna(method='pad', inplace=True)


df['trand-line'] = df['Close'].iloc[0]
trand = df['Close'].iloc[0]


for i in range(len(df)):
        if df['Close'][i] == df['max_high'][i]:
            trand = df['max_low'][i]
            df['trand-line'][i] = df['max_low'][i]
        elif df['Close'][i] == df['max_low'][i]:
            trand = df['max_high'][i]
            df['trand-line'][i] = df['max_high'][i]
        else:
            df['trand-line'][i] = trand

buy=[]
sell=[]
position = 0

for i in range(len(df)):
            if (df['Close'][i] > df['trand-line'][i])  & (position == 0):
                position = 1               
                buy.append(i)
            elif (df['Close'][i] < df['trand-line'][i])  & (position == 1):
                position = 0                
                buy.append(i)
            elif (df['Close'][i] < df['trand-line'][i-1])  & (position == 0) :        
                position = -1                
                sell.append(i)
            elif (df['Close'][i] > df['trand-line'][i])  & (position == -1) :         
                position = 0                
                sell.append(i)


fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1200, width=1750)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']), row=1, col=1)
#fig.add_trace(go.Scatter(x=df.index, y=df['max_low']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA-21']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.iloc[buy].index, y=df.iloc[buy]['Close'], mode="markers", marker_size=15, marker_color='green'),)
fig.add_trace(go.Scatter(x=df.iloc[sell].index, y=df.iloc[sell]['Close'], mode="markers", marker_size=15, marker_color='red'),)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(df)
st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")