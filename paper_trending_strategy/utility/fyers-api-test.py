from fyersApi import Fyers
import pandas as pd
from csv import DictWriter



data = {"symbols":"MCX:CRUDEOIL23FEBFUT"}

client_id = 'HL3MFKAPRB-100'
secret_key = 'E7818HCS14'
redirect_uri = 'http://localhost:8888/'

fyers = Fyers(client_id, secret_key, redirect_uri)

df = fyers.get_live_feed(data)
df = pd.DataFrame(df, index=['t'])

print(df)
df.to_csv('log.csv', mode='a', index=False, header=False,)