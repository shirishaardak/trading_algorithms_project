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



now = datetime.now()
current_time = now.strftime("%H:%M:%S")


df = yf.download(tickers='^NSEBANK', period='5d' , interval='15m')


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

# investment = 500000
# lot_size= 25  
# position = 0
# bt = Backtest()

# for i in range(len(df)):
#             if(df['HA_close'][i] > df['trand-line'][i])   & (position == 0):
#                 position = 1               
#                 bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['HA_close'][i], exit_price=0)
#             elif (df['HA_close'][i] < df['trand-line'][i]) & (position == 1):
#                 position = 0
#                 bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['HA_close'][i])
#             elif (df['HA_close'][i] < df['trand-line'][i])  &  (position == 0):
#                 position = -1                
#                 bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['HA_close'][i], exit_price=0)
#             elif (df['HA_close'][i] > df['trand-line'][i]) & (position == -1) :          
#                 position = 0
#                 bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['HA_close'][i])


# bt.trade_transaction('trand-line-High-Low-15min')
# bt.Backtest_report(df, investment, "trand-line-High-Low-15min", 15)


investment = 500000
lot_size= 25  
position = 0
order=[]
buy=[]
sell=[]

for i in range(len(df)):
            if(df['HA_close'][i] > df['trand-line'][i]) & (position == 0):
                position = 1
                buy.append(i)               
                order.append({'date' : df.index[i], 'lot_size': lot_size, 'position':position, 'buy_sell':'Buy', 'entry_price' : df['HA_close'][i], 'exit_price':0})              
            elif (df['HA_close'][i] < df['trand-line'][i]) & (position == 1):
                position = 0
                buy.append(i)
                order.append({'date' : df.index[i], 'lot_size': lot_size, 'position':position, 'buy_sell':'Buy_exit', 'entry_price' : df['HA_close'][i], 'exit_price':0})
            elif (df['HA_close'][i] < df['trand-line'][i]) & (position == 0):
                position = -1 
                sell.append(i)    
                order .append({'date' : df.index[i], 'lot_size': lot_size, 'position':position, 'buy_sell':'sell', 'entry_price' : df['HA_close'][i], 'exit_price':0})  
            elif (df['HA_close'][i] > df['trand-line'][i]) & (position == -1) :          
                position = 0
                sell.append(i)
                order.append( {'date' : df.index[i], 'lot_size': lot_size, 'position':position, 'buy_sell':'Sell_exit', 'entry_price' : df['HA_close'][i], 'exit_price':0})


#order = order[-1:]
pd.DataFrame(order).to_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/high_low.csv', mode='a', index=True, header=False)

update_order = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/high_low.csv')

update_order= update_order.drop_duplicates()
update_order = pd.DataFrame(update_order)
print(update_order)

update_order.to_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/high_low_New.csv')

data = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/paper_data/high_low_New.csv')

fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[buy].index, y=df.iloc[buy]['HA_close'], marker=dict(color='Blue',size=12,), name="Buy"), row=1, col=1)
fig.add_trace(go.Scatter(mode='markers', x=df.iloc[sell].index, y=df.iloc[sell]['HA_close'], marker=dict(color='Red',size=12,), name="Sell"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['max_high']))
fig.add_trace(go.Scatter(x=df.index, y=df['max_low']))
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']))
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(data)
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")