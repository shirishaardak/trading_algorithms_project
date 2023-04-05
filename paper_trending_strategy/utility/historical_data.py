import requests
import pandas as pd
from datetime import  timedelta
import os
os.chdir(r'D:\\trading_algorithms_project\\paper_trending_strategy')



def historical_data(start_date, end_date, auth_token, timeframe='15minute'):
    userid = 'NY4565'
    timeframe= timeframe
    ciqrandom = '161746886774'
    headers = {'Authorization': auth_token}

    token_df = pd.read_excel('token_symbol.xlsx')
    for i in range(0,len(token_df)):
        token = token_df.loc[i]['TOKEN']
        columns = ['Date','Open','High','Low','Close','V','OI']
        final_df = pd.DataFrame(columns=columns)
        from_date = start_date
        while from_date < end_date :
    
            to_date =  from_date + timedelta(days=30)
            url = f'https://kite.zerodha.com/oms/instruments/historical/{token}/{timeframe}?user_id={userid}&oi=1&from={from_date}&to={to_date}'
            resJson = requests.get(url, headers=headers).json()
            print(resJson)
            candelinfo = resJson['data']['candles']
            df= pd.DataFrame(candelinfo, columns=columns)
        
            final_df = final_df.append(df,ignore_index=True)
            from_date = from_date + timedelta(days=31)        
    
  
    filename = str(token_df.loc[i]['SYMBOL']) + '_' + timeframe +'.csv'
    final_df.to_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/'+ 'historical_data_' + filename, index=True, header=True)
    
    
