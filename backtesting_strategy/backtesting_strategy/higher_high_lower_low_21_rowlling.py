import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import plotly.graph_objects as go 
import yfinance as yf
from utility.backtesting import Backtest
import pandas_ta as ta





df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/stock_data/historical_data_nifty_bank_15minute.csv', index_col='Date')

# ------ Create indicator ------ #
df['EMA-21'] = ta.ema(close=df['Close'], length=21)
df['max_high'] = np.where(df['Close'] == df['Close'].rolling(21, center=True).max(), df['Close'], None)
df['max_low'] = np.where(df['Close'] == df['Close'].rolling(21, center=True).min(), df['Close'], None)
df['max_high'].fillna(method='pad', inplace=True)
df['max_low'].fillna(method='pad', inplace=True)


df['trand-line'] = df['Close'].iloc[0]
trand = df['Close'].iloc[0]


for i in range(len(df)):
        if df['Close'][i] == df['max_high'][i]:
            trand = df['High'][i]
            df['trand-line'][i] = df['High'][i]
        elif df['Close'][i] == df['max_low'][i]:
            trand = df['Low'][i]
            df['trand-line'][i] = df['Low'][i]
        else:
            df['trand-line'][i] = trand


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


bt.trade_transaction('rolling_higher_high_lower_low_21')
bt.Backtest_report(df, investment, "rolling_higher_high_lower_low_21", 15)

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