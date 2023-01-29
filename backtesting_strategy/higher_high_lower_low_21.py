import sys
sys.path.insert(0, 'D:/trading_algorithms_project')
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from utility.backtesting import Backtest



df = pd.read_csv(r'D:/trading_algorithms_project/stock_data/historical_data_nifty_bank_15minute.CSV', index_col='Date')

# ------ Create indicator ------ #

max_idx = argrelextrema(df['Close'].values, np.greater, order=21)[0]
min_idx = argrelextrema(df['Close'].values, np.less, order=21)[0]

#----- ------- match High and low with Current data-------------# 

df['max_high'] = df.iloc[max_idx]['Close']
df['max_low'] = df.iloc[min_idx]['Close']

max_high = 18052.15
max_low = 18052.15
df['trand-line'] = 18052.15
trand = 18052.15


for i in range(len(df)):
    if df['Close'][i-1] == df['max_high'][i-1]:
        trand = df['High'][i]
        df['trand-line'][i] = df['High'][i]
    elif df['Close'][i-1] == df['max_low'][i-1]:
        trand = df['Low'][i]
        df['trand-line'][i] = df['Low'][i]
    else:
        df['trand-line'][i] = trand


investment = 500000
lot_size= 25   
position = 0
bt = Backtest()

for i in range(len(df)):
        if (df['Close'][i] > df['trand-line'][i])  & (position == 0):
            position = 1
            bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy',  entry_price=df['Close'][i], exit_price=0)
        elif (df['Close'][i] < df['trand-line'][i]) & (position == 1):
            position = 0
            bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
        elif (df['Close'][i] < df['trand-line'][i])  & (position == 0) :        
            position = -1
            bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
        elif (df['Close'][i] > df['trand-line'][i]) & (position == -1) :          
            position = 0
            bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])


bt.trade_transaction('higher_high_lower_low_21')
bt.Backtest_report(df, 500000, "higher_high_lower_low_21", 15)
