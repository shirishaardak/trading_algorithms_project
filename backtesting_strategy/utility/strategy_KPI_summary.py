import numpy as np

 
def total_trade(df):
    df['Profit Trade'] = np.where((df['strategy_returns'] > 0), 1, 0)
    df['Loss Trade'] = np.where((df['strategy_returns'] < 0), 1, 0)
    total = df['Profit Trade'] + df['Loss Trade']
    return total.sum()

def Win_Trade(df):
    df['Profit Trade'] = np.where((df['strategy_returns'] > 0.0), 1, 0)
    return sum(df['Profit Trade'])

def Loss_Trade(df):  
    df['Loss Trade'] = np.where((df['strategy_returns'] < 0.0), 1, 0)
    return sum(df['Loss Trade'])

def Average_Profit(df):  
    df = df[df['strategy_returns'] > 0.0]
    return round((df['strategy_returns'].mean()))

def Average_Loss(df):  
    df = df[df['strategy_returns'] < 0.0]
    return round((df['strategy_returns'].mean()))

def max_Profit(df):  
    df = df[df['strategy_returns'] > 0.0]
    return round((max(df['strategy_returns'])))

def max_loss(df):  
    df = df[df['strategy_returns'] < 0.0]
    return round(min(df['strategy_returns']))

def risk_reward(df):
    aveProfit = Average_Profit(df)
    aveLoss = Average_Loss(df)
    return round((aveProfit-aveLoss)/100)

def winning_probability(df):
    get_Win_Trade = Win_Trade(df)
    get_Total_Trade = total_trade(df)
    return "{0:.2f}%".format((get_Win_Trade/get_Total_Trade)*100)   
    

def print_trade_strategy_summary(df):
    print("winning probability:", winning_probability(df))
    print("Risk Reward", risk_reward(df))
    print("Total Trade:", total_trade(df))
    print("Win Trade:", Win_Trade(df))
    print("Loss Trade:", Loss_Trade(df))
    print("Max loss:", max_loss(df))
    print("Max Profit", max_Profit(df)) 
    print("Average Loss:", Average_Loss(df))      
    print("Average Profit:", Average_Profit(df))
    
    
    