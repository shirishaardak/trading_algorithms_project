import requests
import pandas as pd




def get_option_strikePrice(currentPrice, optionType=''):
    # get url
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
    # set headers
    header= {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.7',
    'Content-Type':'application/json; charset=utf-8'
    }
    session = requests.Session()
    data = session.get(url, headers=header)
    cookies = dict(data.cookies)
    response = session.get(url, headers=header).json()    
    rowdf = pd.DataFrame(response)   
    strikePrice = round(currentPrice/100)*100
    df = pd.DataFrame(rowdf['filtered']['data']).fillna(0)
    option_lastPrice = 0
    for i in range(len(df)):
        if df[optionType][i]['strikePrice'] == strikePrice:
            option_lastPrice = df[optionType][i]['lastPrice']
    return option_lastPrice

