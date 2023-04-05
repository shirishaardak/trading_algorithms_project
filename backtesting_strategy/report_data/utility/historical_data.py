import requests
import pandas as pd
import time 
from datetime import datetime, timedelta
from datetime import date

start_date = date(2017,1,1)   #yyyy-mm-dd format
end_date =  date(2023,1,30)     #yyyy-mm-dd format

# End date need today 

auth_token = 'enctoken 7dGR0wtBDlBj0jl2jtSsNLXksp0LWzMrxoVKMe8S7QvTo4+urXqy6N0CcZKKmCr+hW+VoaqmS7EKR5CK1wLXLkRLpYfKYwEEsJauyvsOVYUGclyvK6PJPQ=='

def historical_data(start_date, end_date, auth_token, timeframe='5minute'):
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
    final_df.to_csv(r'D:/trading_algorithms_project/stock_data/'+ 'historical_data_' + filename, index=True, header=True)
    
    
historical_data(start_date, end_date, auth_token)