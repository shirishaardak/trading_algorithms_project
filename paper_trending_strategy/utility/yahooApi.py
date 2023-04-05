import yfinance as yf
import pandas as pd



def get_data(tickers, period, interval,strategiesName):
    df = yf.download(tickers=tickers, period=period, interval=interval, auto_adjust=True)

    df.to_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/' + strategiesName + '.CSV',  mode='a', index=True, header=False, )

    data = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/NSEBANK_15_MIN.CSV',)

    data = data.drop_duplicates(subset=['Date',])

    data.to_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/duplicates_NSEBANK_15_MIN.CSV',)
