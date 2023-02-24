import sys
sys.path.insert(0, 'D:/trading_algorithms_project')
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import streamlit as st  
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from scipy.signal import argrelextrema
from plotly.subplots import make_subplots
import pandas_ta as ta
from utility.backtesting import Backtest

now = datetime.now()


current_time = now.strftime("%H:%M:%S")


df = yf.download(tickers="^NSEBANK",
                                period="3d",
                                interval="15m",
                                auto_adjust=True)
#df = pd.read_csv(r'D:/trading_algorithms_project/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')

def heikin_ashi(df):
    heikin_ashi_df = df
    
    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)
    
    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
    
    return heikin_ashi_df

df = heikin_ashi(df)

# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater_equal, order=11)[0]
min_idx = argrelextrema(df['Close'].values, np.less_equal, order=11)[0]
# max_idx= max_idx[:-1]
# min_idx= min_idx[:-1]
#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['Close']
df['max_low'] = df.iloc[min_idx]['Close']

df['trand-line'] = df['Close'].iloc[0]
trand = df['Close'].iloc[0]


for i in range(len(df)):
        if df['Close'][i-1] == df['max_high'][i-1]:
            trand = df['High'][i]
            df['trand-line'][i] = df['High'][i]
        elif df['Close'][i-1] == df['max_low'][i-1]:
            trand = df['Low'][i]
            df['trand-line'][i] = df['Low'][i]
        else:
            df['trand-line'][i] = trand


fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
# fig.add_trace(go.Scatter(x=df.index, y=df['max_low']),)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")