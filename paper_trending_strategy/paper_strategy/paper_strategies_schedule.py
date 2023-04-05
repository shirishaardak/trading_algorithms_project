import sys
sys.path.insert(0, 'D:/trading_algorithms_project/paper_trending_strategy')
import pandas as pd
import numpy as np
from paper_strategy.correlation_close_ema_11 import correlation_close_ema_11
from paper_strategy.correlation_close_close_11day import correlation_close_11
from utility.historical_data import historical_data
from datetime import datetime, date
import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from scipy.signal import argrelextrema
import pandas_ta as ta
from utility.technical_indicators import heikin_ashi
import os
os.chdir(r'D:\\trading_algorithms_project\\paper_trending_strategy')



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
start_date = date(2023,3,1)   #yyyy-mm-dd format
end_date =  date(2023,4,3)     #yyyy-mm-dd format

# End date need today 

auth_token = 'enctoken 05bXfsZRMu7xBzcUGsUSp93PaxgvGflav4KVGzmygYRHXZxOYP3uTEq7JDxY+6yDGFSTp2ZvY1kfz5tuGkljEJFGVDhF903W3aG74aQo5CmYgvim0d8M4Q=='

def strategies():    
    historical_data(start_date, end_date, auth_token)
    correlation_close_ema_11()
    correlation_close_11()


strategies()

df = pd.read_csv(r'D:/trading_algorithms_project/paper_trending_strategy/stock_data/historical_data_nifty_bank_15minute.CSV',)


fig = make_subplots(rows=2, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800, width=1750)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.title(current_time)
st.write(fig)
st.table(df)
st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")

