import sys
sys.path.insert(0, 'C:/Shirish/strategy_analysis/trading_algorithms_project/backtesting_strategy/')
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

def data_feed():
    df = yf.download(tickers='CL=F', period='1d' , interval='1m')

    df = df[-1:]

    df.to_csv(r'C:/Shirish/strategy_analysis/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/testing.csv', mode='a', index=True, header=False)

data_feed()

df = pd.read_csv(r'C:/Shirish/strategy_analysis/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/testing.csv', index_col='Datetime')

#print(df)

# ------ Create indicator ------ #
df = ta.ha(open_=df.Open, high=df.High, low=df.Low, close=df.Close,)
max_idx = argrelextrema(df['HA_close'].values, np.greater_equal, order=21)[0]
min_idx = argrelextrema(df['HA_close'].values, np.less_equal, order=21)[0]

#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['HA_close']
df['max_low'] = df.iloc[min_idx]['HA_close']

max_high = df['HA_close'].iloc[0]
max_low = df['HA_close'].iloc[0]

df['trand-line'] = df['HA_close'].iloc[0]
trand = df['HA_close'].iloc[0]


for i in range(len(df)):
    if df['HA_close'][i] >= df['max_high'][i]:
        trand = df['HA_low'][i]
        df['trand-line'][i] = df['HA_low'][i]
    elif df['HA_close'][i] <= df['max_low'][i]:
        trand = df['HA_high'][i]
        df['trand-line'][i] = df['HA_high'][i]
    else:
        df['trand-line'][i] = trand


fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']))
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")