import pandas as pd
import os
from fyers_api import fyersModel , accessToken
from fyers_api.Websocket import ws
from datetime import datetime



class Fyers:

    def __init__(self, app_id, app_secret, redirect_url,):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_url = redirect_url 
        
    def get_access_token(self):
        if not os.path.exists('access_token.txt'):
            session=accessToken.SessionModel(client_id=self.app_id, secret_key=self.app_secret, redirect_uri=self.redirect_url, response_type='code', grant_type='authorization_code')
            response = session.generate_authcode() 
            print('url:', response)
            auth_code = input('Enter Code:')
            session.set_token(auth_code)
            response = session.generate_token()

            access_token = response["access_token"]
            with open('access_token.txt', 'w') as f:
                f.write(access_token)
        else:
            with open('access_token.txt', 'r') as f:
                access_token = f.read()  
        
        return access_token
        

    def set_token(self):
        access_token = self.get_access_token()
        fyers = fyersModel.FyersModel(client_id=self.app_id, token=access_token, log_path="")
        return fyers
    
    def get_data(self, data):
        fyers_data = self.set_token()
        data = fyers_data.history(data)
        def timestamptodate(timestamp):
            return datetime.fromtimestamp(timestamp)
        data = pd.DataFrame(data['candles'])
        data.to_csv(r'D:/trading_algorithms_project/strategy_analysis/stock_data/downloaded_data/live.csv', index=True, header=True)

        columns = ['Date', 'open', 'high', 'low', 'close', 'v']
        data = pd.read_csv('D:/trading_algorithms_project/strategy_analysis/stock_data/downloaded_data/live.csv', header = None, names = columns)
        df = pd.DataFrame(data)
        date_df = []
        for i in df['Date']:
         date_df.append({"Date" : timestamptodate(i)})
        date_df = pd.DataFrame(date_df)
        realtime_data = pd.concat([date_df, df['open'], df['high'], df['low'], df['close'], df['v']], axis=1)
        return realtime_data

    def get_live_feed(self, data):
        fyers_data = self.set_token()
        df = fyers_data.quotes(data)['d'][0]['v']['cmd']
        return df