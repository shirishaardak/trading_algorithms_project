import pandas as pd
from utility.performance_metrics import print_strategy_summary
from utility.strategy_KPI_summary import print_trade_strategy_summary


class Backtest:
     def __init__(self):
        self.columns = ['Date', 'Symbol', 'Qty','position','Buy/Sell','Entry Price','Exit Price']
        self.backtesting = pd.DataFrame(columns=self.columns)
        print(self.backtesting)
        
     def orders(self, date, symbol, qty, position, buy_sell='', entry_price=0, exit_price=0):
         self.trade_book = dict(zip(self.columns, [None] * len(self.columns)))
         self.trade_book['Date'] = date
         self.trade_book['Symbol'] = symbol
         self.trade_book['Qty'] = qty
         self.trade_book['position'] = position
         self.trade_book['Buy/Sell'] = buy_sell
         self.trade_book['Entry Price'] = entry_price
         self.trade_book['Exit Price'] = exit_price 
         trade_book_df = pd.DataFrame.from_dict([self.trade_book])  
         self.backtesting = pd.concat([trade_book_df, self.backtesting])
         self.backtesting.set_index(self.backtesting["Date"], inplace = True)
         self.backtesting = self.backtesting.sort_index(ascending=True)
         

     def trade_transaction(self, strategiesName):
         transaction = self.backtesting.copy()         
         buy_transaction = transaction[(transaction['Buy/Sell'] == 'Buy') | (transaction['Buy/Sell'] == 'Buy_Exit')]        
         sell_transaction = transaction[(transaction['Buy/Sell'] == 'Sell') | (transaction['Buy/Sell'] == 'Sell_exit')]               
         buy_transaction['strategy_returns'] = (buy_transaction['Exit Price'] - buy_transaction['Entry Price'].shift(1)) * buy_transaction['Qty']
         sell_transaction['strategy_returns'] = (sell_transaction['Entry Price'].shift(1) - sell_transaction['Exit Price']) * sell_transaction['Qty']                        
         self.backtesting = pd.concat([buy_transaction, sell_transaction])
         self.backtesting = self.backtesting.drop("Date",axis=1)        
         self.backtesting = self.backtesting.sort_values(by='Date', ascending=True)
         self.backtesting.to_csv(r'D:/trading_algorithms_project/report_data/trade_transaction_' + strategiesName + '.CSV')

     def Backtest_report(self, df, investment, strategiesName, timeframe):
         transaction_book = self.backtesting.copy()
         backtest_returns = df.join(transaction_book)
         backtest_returns['strategy_returns'] = backtest_returns['strategy_returns'].fillna(0) 
         backtest_returns['returns'] = backtest_returns['strategy_returns'].cumsum()+ investment
         returns = backtest_returns['returns']
         returns.index = pd.to_datetime(returns.index)
         backtest_returns.to_csv(r'D:/trading_algorithms_project/report_data/Backtest_report_' + strategiesName + '.CSV')
         print_strategy_summary(strategiesName, backtest_returns, timeframe)
         print_trade_strategy_summary(backtest_returns)
     
       
               

