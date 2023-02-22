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


df = pd.read_csv(r'D:/trading_algorithms_project/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')

def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close'])
    
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

df['SAM-11'] = ta.ema(close=df["Close"], length=11)
df['Close-diff'] = df['Close'] - df['Close'].shift(42)


print(df)


investment = 500000
lot_size= 25   
position = 0
bt = Backtest()


for i in range(len(df)):
            if (df['Close-diff'][i] > 100) & (df['Close'][i] > df['SAM-11'][i]) & (df['Close'][i] > df['Close'][i-1]) & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] < df['SAM-11'][i]) & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
            elif(df['Close-diff'][i] < -100) & (df['Close'][i] < df['SAM-11'][i]) & (df['Close'][i] < df['Close'][i-1]) &  (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] > df['SAM-11'][i]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])


bt.trade_transaction('close_different_21_days_EMA_21')
bt.Backtest_report(df, investment, "close_different_21_days_EMA_21", 15)


fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(df.tail(20))
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh")