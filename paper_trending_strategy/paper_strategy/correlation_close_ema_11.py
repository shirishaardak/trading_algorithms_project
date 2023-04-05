import sys
sys.path.insert(0, 'D:/trading_algorithms_project/paper_trending_strategy')
import pandas as pd
import numpy as np
import pandas_ta as ta
from utility.backtesting import Backtest
from utility.technical_indicators import heikin_ashi


def correlation_close_ema_11(): 

    df = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/historical_data_nifty_bank_15minute.CSV',)
    
    df = heikin_ashi(df)
    

    df['EMA-11'] = ta.ema(close=df['Close'], length=11)
    df['correlation_close_ema'] = df['Close'] - df['EMA-11']

    # ------ Create indicator ------ #
    investment = 500000
    lot_size= 25   
    position = 0
    bt = Backtest()

    for i in range(len(df)):
                if (df['correlation_close_ema'][i] > 100) & (position == 0):
                    position = 1
                    bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Buy', entry_price=df['Close'][i], exit_price=0)
                elif (df['correlation_close_ema'][i] < 0) & (position == 1):
                    position = 0
                    bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Buy_Exit', entry_price=0, exit_price=df['Close'][i])
                elif (df['correlation_close_ema'][i] < -100) &  (position == 0) :        
                    position = -1
                    bt.orders(df.index[i], 'Bank', lot_size, position= position, buy_sell='Sell', entry_price=df['Close'][i], exit_price=0)
                elif (df['correlation_close_ema'][i] > 0) & (position == -1) :          
                    position = 0
                    bt.orders(df.index[i], 'Bank', lot_size,  position= position, buy_sell='Sell_exit', entry_price=0, exit_price=df['Close'][i])

    bt.trade_transaction('correlation_close_ema_11')
    bt.Backtest_report(df, investment , 'correlation_close_ema_11', 15)
