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


df = yf.download(tickers="CL=F",
                            period="1d",
                            interval="5m",
                            auto_adjust=True)

# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater)[0]
min_idx = argrelextrema(df['Close'].values, np.less)[0]

#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['Close']
df['max_low'] = df.iloc[min_idx]['Close']

Tande = 0

for i in range(len(df)):
    if df['Close'][i] == df['max_high'][i]:
        df['max_high'][i] = df['max_high'][i-1]
    elif df['Close'][i] == df['max_low'][i]:
        df['max_high'][i] = df['max_low'][i-1]
 

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.add_trace(go.Scatter(x=df.index, y=df['max_high']),)
fig.add_trace(go.Scatter(x=df.index, y=df['max_low']),)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[max_idx].index, y=df.iloc[max_idx]['Close'], marker=dict(color='Blue',size=12,)))
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[min_idx].index, y=df.iloc[min_idx]['Close'], marker=dict(color='Red',size=12,)))
# fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell].index, y=df.iloc[sell]['Close'], marker=dict(color='black',size=12,)))
# fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell_exit].index, y=df.iloc[sell_exit]['Close'], marker=dict(color='yellow',size=12,)))

fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)


st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)


st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")