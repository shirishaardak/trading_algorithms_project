import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
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
import time



now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def data_feed():

    #old_df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/Data_testing_gold.csv', index_col='Datetime')
    df = yf.download(tickers='CL=F', period='1d' , interval='5m')
    
    

    #df = pd.concat([old_df, new_df])
    #df = df.drop_duplicates(subset=['Open','High','Low','Close','Adj Close'], keep=False)
    
    print(df)
    df = ta.ha(open_=df.Open, high=df.High, low=df.Low, close=df.Close,)
    max_idx = argrelextrema(df['HA_high'].values, np.greater_equal, order=11)[0]
    min_idx = argrelextrema(df['HA_low'].values, np.less_equal, order=11)[0]
    df['21_high'] = df['HA_high'].rolling(window=11).max()
    df['21_low'] = df['HA_low'].rolling(window=11).min()

    df['max_high'] = df.iloc[max_idx]['HA_high']
    df['max_low'] = df.iloc[min_idx]['HA_low']

    df['trand-line'] = df['HA_close'].iloc[0]
    trand = df['HA_close'].iloc[0]

    #print(df)

    for i in range(len(df)):
        if df['HA_high'][i] == df['max_high'][i]:
            trand = df['HA_high'][i]
            df['trand-line'][i] = df['HA_high'][i]
        elif df['HA_low'][i] == df['max_low'][i]:
            trand = df['HA_low'][i]
            df['trand-line'][i] = df['HA_low'][i]
        else:
            df['trand-line'][i] = trand

    df = df.iloc[-1:]
    print(df)
    df.to_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/Data_testing_gold.csv', mode='a', index=True, header=False)

 
data_feed()

df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/Data_testing_gold.csv', index_col='Datetime')

orders=[]
list=[]
position=0
for i in range(len(df)):
            if(df['HA_close'][i] > df['trand-line'][i-2]) & (position == 0):
                position = 1               
                orders.append({'date': df.index[i], 'buy_sell':'buy','entry_price':df['HA_close'][i], 'exit_price':0})
                list.append(i)
            elif (df['HA_close'][i] < df['trand-line'][i-1]) & (position == 1):
                position = 0
                orders.append({'date': df.index[i],  'buy_sell':'buy_exit',  'entry_price':0, 'exit_price': df['HA_close'][i]})
                list.append(i)
            elif (df['HA_close'][i] < df['trand-line'][i-2]) & (position == 0):
                position = -1                
                orders.append({'date': df.index[i],  'buy_sell':'sell',  'entry_price':df['HA_close'][i], 'exit_price':0})
                list.append(i)
            elif (df['HA_close'][i] > df['trand-line'][i-1]) & (position == -1) :          
                position = 0
                orders.append({'date': df.index[i],  'buy_sell':'sell_exit',  'entry_price':0, 'exit_price':df['HA_close'][i]})
                list.append(i)

orders.to_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/Data_testing_order.csv',  index=True,)
fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[list].index, y=df.iloc[list]['HA_close'], marker=dict(color='black',size=12,), name="Buy"), row=1, col=1)
fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['max_high'], marker=dict(color='green',size=6,), name="buy"), row=1, col=1)
fig.add_trace(go.Scatter(mode='markers', x=df.index, y=df['max_low'], marker=dict(color='Red',size=6,), name="sell"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']))
fig.add_trace(go.Scatter(x=df.index, y=df['21_high']))
fig.add_trace(go.Scatter(x=df.index, y=df['21_low']))
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st.set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(df)
st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")