import sys
sys.path.insert(0, 'D:/trading_algorithms_project')
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import plotly.graph_objects as go 
import yfinance as yf
from utility.backtesting import Backtest





df = pd.read_csv(r'D:/trading_algorithms_project/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')


# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater_equal, order=21)[0]
min_idx = argrelextrema(df['Close'].values, np.less_equal, order=21)[0]

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

print(df)


investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
            if (df['Close'][i] > df['trand-line'][i-1]) & (position == 0):
                position = 1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] < df['trand-line'][i-1]) & (position == 1):
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
            elif (df['Close'][i] < df['trand-line'][i-1])  & (position == 0) :        
                position = -1
                bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
            elif (df['Close'][i] > df['trand-line'][i-1]) & (position == -1) :          
                position = 0
                bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])


bt.trade_transaction('paper_higher_high_lower_low_21')
bt.Backtest_report(df, investment, "paper_higher_high_lower_low_21", 15)

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
#fig.add_trace(go.Scatter(x=df.iloc[max_idx].index, y=df.iloc[max_idx]['Close']),)
#fig.add_trace(go.Scatter(x=df.iloc[min_idx].index, y=df.iloc[min_idx]['Close']),)
fig.add_trace(go.Scatter(x=df.index, y=df['max_high']),)
fig.add_trace(go.Scatter(x=df.index, y=df['max_low']),)
fig.add_trace(go.Scatter(x=df.index, y=df['trand-line']),)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)

fig.show()