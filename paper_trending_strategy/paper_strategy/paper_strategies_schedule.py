import sys
sys.path.insert(0, 'D:/trading_algorithms_project/paper_trending_strategy')
import pandas as pd
import numpy as np
from paper_strategy.correlation_close_ema_11 import correlation_close_ema_11
from paper_strategy.correlation_close_close_11day import correlation_close_11
from utility.historical_data import historical_data
from datetime import datetime, date
import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from scipy.signal import argrelextrema
import pandas_ta as ta
from utility.technical_indicators import heikin_ashi
import os
os.chdir(r'D:\\trading_algorithms_project\\paper_trending_strategy')
from utility.backtesting import Backtest



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
start_date = date(2023,4,1)   #yyyy-mm-dd format
end_date =  date(2023,4,16)     #yyyy-mm-dd format

# End date need today 

auth_token = 'enctoken y5NaHvi93j5Mw551fNVkjAFPK2wGH0Vt1N3zqKPs1DMFS6cfYb5s5kF0wi11KPQel579vNT73MSn2/OZKJU4Jyi30Mf0Mb423iVR9xs9TIUIdF4khVRLSg=='

def strategies():    
    historical_data(start_date, end_date, auth_token)
    correlation_close_ema_11()
    correlation_close_11()


strategies()

df = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/historical_data_nifty_bank_15minute.CSV', index_col='Date')
report_data = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/report_data/Backtest_report_SAM-9_and_SAM-18.CSV',)

df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

df['SAM-9'] = ta.ema(close=df['Close'], length=9)
df['SAM-18'] = ta.ema(close=df['Close'], length=18)

#--------- Buy and Sell 
buy=[]
sell=[]

investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['Close'][i] > df['Close'][i-1]) &  (df['SAM-9'][i] > df['SAM-18'][i]) & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
                buy.append(i)
            elif (df['Close'][i] < df['SAM-18'][i])  & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
                buy.append(i)
            elif (df['Close'][i] < df['Close'][i-1]) &  (df['SAM-9'][i] < df['SAM-18'][i])  & (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
                sell.append(i)
            elif (df['Close'][i] > df['SAM-18'][i])  & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])
                sell.append(i)


bt.trade_transaction('SAM-9_and_SAM-18')
bt.Backtest_report(df, investment, "SAM-9_and_SAM-18", 60)

fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
fig.add_trace(go.Scatter(x=df.iloc[buy].index, y=df.iloc[buy]['Close'], mode="markers", marker_size=10, marker_color='green'),)
fig.add_trace(go.Scatter(x=df.iloc[sell].index, y=df.iloc[sell]['Close'], mode="markers", marker_size=10, marker_color='red'),)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-9']),)
fig.add_trace(go.Scatter(x=df.index, y=df['SAM-18']),)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(df)
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")

