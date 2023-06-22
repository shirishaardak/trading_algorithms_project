import sys
sys.path.insert(0, 'D:/trading_algorithms_project/backtesting_strategy')
import pandas as pd
import numpy as np
import plotly.graph_objects as go 
import streamlit as st  
import yfinance as yf
from plotly.subplots import make_subplots
import pandas_ta as ta
from utility.backtesting import Backtest
from utility.technical_indicators import heikin_ashi

#----- Data

#df = yf.download(tickers='^NSEBANK', period='30d' , interval='15m')

df = pd.read_csv(r'D:/trading_algorithms_project/backtesting_strategy/report_data/Backtest_report_SAM-9-High-Low.CSV', index_col='Date')


#-----Ploting Data
fig = make_subplots(rows=3, cols=1,)
fig.add_trace(go.Candlestick(x=df.index,
                open=df['HA_open'],
                high=df['HA_high'],
                low=df['HA_low'],
                close=df['HA_close']), row=1, col=1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1500, width=1750)
fig.add_trace(go.Scatter(x=df.index, y=df['returns']), row=2, col=1)
fig.update_xaxes(type='category', rangeslider_visible=False)
fig.update_yaxes(fixedrange=False)
st. set_page_config(layout="wide")
st.write(fig)