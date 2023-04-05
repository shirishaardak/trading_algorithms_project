import pandas as pd
import numpy as np

# Calculate Total Profit Amount 
def Total_returns(df):
    FirstValue = df['returns'].iloc[0]
    LastValue = df['returns'].iloc[-1]
    total =  LastValue - FirstValue
    return "{0:.2f}".format(total)

# Calculate Total Profit %
def cumulative_returns(df):
    FirstValue = df['returns'].iloc[0]
    LastValue = df['returns'].iloc[-1]
    total =  ((LastValue - FirstValue) / FirstValue )*100
    return "{0:.2f}%".format(total)

# Calculate compounded annual growth rate
def get_CAGR(df, candleTimeFrame):
    FirstValue = df['returns'].iloc[0]
    LastValue = df['returns'].iloc[-1]
    trading_hours = 7
    timeframe = (60/candleTimeFrame) * trading_hours
    n = len(df) / (252*timeframe) 
    CAGR = (LastValue / FirstValue) ** (1/n) -1
    return '{:.2%} '.format(CAGR)

# Calculate annualised volatility
def get_annualised_volatility(df):       
    return "{0:.2f}%".format(df['returns'].std()*np.sqrt(252) * 100)

# Calculate Sharpe ratio
def get_sharpe_ratio(df):
    returns = df['returns'].pct_change()
    volatility = returns.std() * np.sqrt(252)      
    return "{0:.2f}%".format((returns.mean() - 0.02) / volatility, 2)

# Calculate the maximum drawdown
def get_max_drawdown(df):
    drawdown = 1 - df['returns'].div(df['returns'].cummax())
    return "{0:.2f}%".format(max(drawdown.expanding().max() * 100), 2)

def print_strategy_summary(name, df, timeframe):
    print("strategy summary:", name)
    print("Total Profit:", Total_returns(df))    
    print("Cumulative Returns:", cumulative_returns(df))
    print("CAGR Returns:", get_CAGR(df, timeframe))
    print("maximum drawdown:", get_max_drawdown(df)) 
    print("Sharpe ratio:", get_sharpe_ratio(df))      
    print("annualised volatility:", get_annualised_volatility(df))