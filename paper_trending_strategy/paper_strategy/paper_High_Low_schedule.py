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
start_date = date(2023,6,1)   #yyyy-mm-dd format
end_date =  date(2023,6,13)     #yyyy-mm-dd format

# End date need today 

auth_token = 'enctoken 1YdLmsSlYhnQRBXi+wWij315Y7sftWHyBwYvmGgNpefv6Rvhcq6WmaabC3hcid4Q6c3z5SbWOtvCsB/jH5AMd0WdMWZUdDC8cl49/u9MOK0avfysMKn3yQ=='

def strategies():    
    historical_data(start_date, end_date, auth_token)  

strategies()

df = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/historical_data_nifty_bank_15minute.CSV', index_col='Date')
df = ta.ha(open_=df.Open, high=df.High, low=df.Low, close=df.Close,)

df['max_high'] = np.where(df['HA_close'] == df['HA_close'].rolling(21).max(), df['HA_close'], None)
df['max_low'] = np.where(df['HA_close'] == df['HA_close'].rolling(21).min(), df['HA_close'], None)
df['max_high'].fillna(method='pad', inplace=True)
df['max_low'].fillna(method='pad', inplace=True)


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

#--------- Buy and Sell 
buy=[]
sell=[]
Order_book= []
print(Order_book)
investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['HA_close'][i] > df['trand-line'][i-1]) & (position == 0):
                position = 1
                Order_book.append([df.index[i], 'Bank', lot_size, position,  'Buy',  df['HA_close'][i],  0])
                buy.append(i)
            elif (df['HA_close'][i] < df['trand-line'][i]) & (position == 1):
                position = 0
                Order_book.append([df.index[i], 'Bank', lot_size, position,  'Buy_exit',  df['HA_close'][i],  0])                
                buy.append(i)
            elif (df['HA_close'][i] < df['trand-line'][i-1]) & (position == 0) :        
                position = -1
                Order_book.append([df.index[i], 'Bank', lot_size, position,  'Sell',  df['HA_close'][i],  0])
                sell.append(i)
            elif (df['HA_close'][i] > df['trand-line'][i]) & (position == -1) :          
                position = 0
                Order_book.append([df.index[i], 'Bank', lot_size, position,  'Sell_exit',  df['HA_close'][i],  0])
                sell.append(i)


#Order_book = bt.trade_transaction('SAM-9_and_SAM-18')
# bt.Backtest_report(df, investment, "SAM-9_and_SAM-18", 60)

#final_df.to_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/'+ 'historical_data_' + filename, index=True, header=True)

pd.DataFrame(Order_book).to_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/test.csv', mode='a', index=False, header=False)
order = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/test.csv', index_col='Date')

fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
fig.add_trace(go.Scatter(x=df.iloc[buy].index, y=df.iloc[buy]['HA_close'], mode="markers", marker_size=10, marker_color='green'),)
fig.add_trace(go.Scatter(x=df.iloc[sell].index, y=df.iloc[sell]['HA_close'], mode="markers", marker_size=10, marker_color='red'),)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
# fig.add_trace(go.Scatter(x=df.index, y=df['SAM-18']),)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(order)
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")

