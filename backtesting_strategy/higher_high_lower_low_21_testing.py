import sys
sys.path.insert(0, 'D:/trading_algorithms_project')
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import plotly.graph_objects as go 
import plotly.express as px
import streamlit as st  
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime


now = datetime.now()


current_time = now.strftime("%H:%M:%S")


df = yf.download(tickers="^NSEBANK",
                            period="5d",
                            interval="15m",
                            auto_adjust=True)

# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater, order=9)[0]
min_idx = argrelextrema(df['Close'].values, np.less, order=9)[0]

#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['Close']
df['max_low'] = df.iloc[min_idx]['Close']

df['trand-line'] = df['Close'].iloc[1]
trand = df['Close'].iloc[1]


for i in range(len(df)):
        if df['Close'][i-1] == df['max_high'][i-1]:
            trand = df['High'][i]
            df['trand-line'][i] = df['High'][i]
        elif df['Close'][i-1] == df['max_low'][i-1]:
            trand = df['Low'][i]
            df['trand-line'][i] = df['Low'][i]
        else:
            df['trand-line'][i] = trand

buy=[]
buy_exit =[]
sell=[]
sell_exit=[]
position = 0
for i in range(len(df)):
            if (df['Close'][i] > df['trand-line'][i-1]) & (position == 0):
                position = 1
                buy.append(i)
            elif (df['Close'][i] < df['trand-line'][i-1]) & (position == 1):
                position = 0
                buy_exit.append(i)
            elif (df['Close'][i] < df['trand-line'][i-1])  & (position == 0) :        
                position = -1
                sell.append(i)
            elif (df['Close'][i] > df['trand-line'][i-1]) & (position == -1) :          
                position = 0
                sell_exit.append(i)

 

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[buy].index, y=df.iloc[buy]['Close'], marker=dict(color='Blue',size=12,)))
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[buy_exit].index, y=df.iloc[buy_exit]['Close'], marker=dict(color='yellow',size=12,)))
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell].index, y=df.iloc[sell]['Close'], marker=dict(color='Red',size=12,)))
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell_exit].index, y=df.iloc[sell_exit]['Close'], marker=dict(color='green',size=12,)))
# fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell].index, y=df.iloc[sell]['Close'], marker=dict(color='black',size=12,)))
# fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell_exit].index, y=df.iloc[sell_exit]['Close'], marker=dict(color='yellow',size=12,)))

fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)


st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)


st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")