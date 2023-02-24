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
                                period="5d",
                                interval="15m",
                                auto_adjust=True)


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



df['sam-11'] = ta.ema(close=df['Close'], length=11)
df['sam-14-sam-28'] = df['Close'] - df['sam-28']

# ------ Create indicator ------ #
investment = 500000
lot_size= 25   
position = 0
bt = Backtest()
orders = []
buy=[]
sell=[]
for i in range(len(df)):
            if (df['sam-14-sam-28'][i] > 100) & (position == 0):
                position = 1
                buy.append(i)
                orders.append({'Date': df.index[i],  'buy_sell':'Buy',  "entry_price": df['Close'][i], "exit_price":0})
            elif (df['sam-14-sam-28'][i] < 0) & (position == 1):
                position = 0
                buy.append(i)
                orders.append({'Date': df.index[i],  'buy_sell':'Buy-exit',  "entry_price": 0, "exit_price":df['Close'][i]})
            elif (df['sam-14-sam-28'][i] < -100) &  (position == 0) :        
                position = -1
                sell.append(i)
                orders.append({'Date': df.index[i],  'buy_sell':'Sell',  "entry_price":df['Close'][i], "exit_price":0})
            elif (df['sam-14-sam-28'][i] > 0) & (position == -1) :          
                position = 0
                sell.append(i)
                orders.append({'Date': df.index[i],  'buy_sell':'sell-exit',  "entry_price": 0, "exit_price":df['Close'][i]})


orders = pd.DataFrame(orders)

orders.to_csv(r'D:/trading_algorithms_project/report_data/paper_data/close_ema_11_days_different_paper.csv',)

fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[buy].index, y=df.iloc[buy]['Close'], marker=dict(color='Blue',size=12,), name="Buy"), row=1, col=1)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell].index, y=df.iloc[sell]['Close'], marker=dict(color='yellow',size=12,), name="Sell"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['sam-28']), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['sam-28']), row=1, col=1)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)

st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(orders.tail(5))
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")