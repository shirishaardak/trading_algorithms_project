import requests, time
import pandas as pd
from datetime import datetime

def realtime_data(symbol,timeframe): 
    
    def datetotime(date):
        time_tuple = date.timetuple()
        timestamp = round(time.mktime(time_tuple))
        return timestamp

    def timestamptodate(timestamp):
        return datetime.fromtimestamp(timestamp)

    date = datetime.today()

    start = datetotime(datetime(2023,1,1))
    end = datetotime(datetime.today())

    url = 'https://priceapi.moneycontrol.com/techCharts/history?symbol='+symbol+'&resolution='+str(timeframe)+'&from='+str(start)+'&to='+str(end)+''
    print(url)
    resp = requests.get(url).json()

    df = pd.DataFrame(resp)
    date_df = []
    for i in df['t']:
        date_df.append({"Date" : timestamptodate(i)})

    date_df = pd.DataFrame(date_df)

    realtime_data = pd.concat([date_df, df['o'], df['h'], df['l'], df['c']], axis=1)
    realtime_data.to_csv('./stock_data/'+symbol+'_realtime_data.CSV')
    return realtime_data

realtime_data('23', 15)