import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
from datetime import datetime, date
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema
import plotly.graph_objects as go 
import yfinance as yf

import pandas_ta as ta
import streamlit as st  
from streamlit_autorefresh import st_autorefresh



now = datetime.now()
current_time = now.strftime("%H:%M:%S")

df = yf.download(tickers='CL=F', period='1d' , interval='5m')

df = ta.ha(open_=df.Open, high=df.High, low=df.Low, close=df.Close,)
df['RSI'] = ta.rsi(close=df.HA_close, length=14)
df['ATR'] = ta.atr(high=df.HA_high, low=df.HA_low, close=df.HA_close, length=14)
df['ATR-20'] = ta.sma(close=df['ATR'], length=20)
max_idx = argrelextrema(df['HA_high'].values, np.greater_equal, order=10)[0]
min_idx = argrelextrema(df['HA_low'].values, np.less_equal, order=10)[0]
# max_idx = max_idx[:-1]
# min_idx = min_idx[:-1]

print(max_idx)
print(min_idx)

high_low= np.concatenate((max_idx, min_idx))
high_low_up = np.sort(high_low)
high_low_up = high_low_up[:-1]

df['max_high_low'] = df.iloc[high_low_up]['HA_close']
df['max_high'] = df.iloc[max_idx]['HA_close']
df['max_low'] = df.iloc[min_idx]['HA_close']

df['trand-line'] = df['HA_close'].iloc[0]
trand = df['HA_close'].iloc[0]


for i in range(len(df)):
    if df['HA_close'][i] == df['max_high'][i]:
        trand = df['HA_high'][i]
        df['trand-line'][i] = df['HA_high'][i]
    elif df['HA_close'][i] == df['max_low'][i]:
        trand = df['HA_low'][i]
        df['trand-line'][i] = df['HA_low'][i]
    else:
        df['trand-line'][i] = trand


# ------ Create indicator ------ #


fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1800)
fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['max_high_low'], marker=dict(color='Blue',size=12,), name="Buy"), row=1, col=1)
#fig.add_trace(go.Scatter(mode='markers', x=df.iloc[min_idx].index, y=df.iloc[min_idx]['HA_low'], marker=dict(color='Red',size=12,), name="Sell"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']))
#fig.add_trace(go.Scatter(x=df.index, y=df['max_high_low']))
# fig.add_trace(go.Scatter(x=df.index, y=df['RSI']), row=2, col=1)
# fig.add_trace(go.Scatter(x=df.index, y=df['ATR']), row=3, col=1)
# fig.add_trace(go.Scatter(x=df.index, y=df['ATR-20']), row=3, col=1)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")