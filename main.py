import pandas as pd
import numpy as np
import requests

import apimoex

def dual_sma(df):
    buy_signal_price = []
    sell_signal_price = []
    date = []
    flag = 0

    for i in range(len(df)):
        if df['SMA30'][i] > df['SMA100'][i]:
            if flag != 1:
                buy_signal_price.append(df['CLOSE'][i])
                sell_signal_price.append(np.nan)
                flag = 1
            else:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)
            date = df['TRADEDATE'][i]
        elif df['SMA30'][i] < df['SMA100'][i]:
            if flag != 1:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(df['CLOSE'][i])
                flag = 1
            else:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)
            date = df['TRADEDATE'][i]
    return (buy_signal_price,sell_signal_price,date)

#https://ru.tradingview.com/chart/?symbol=MOEX%3AMTSS
with requests.Session() as session:
    data = apimoex.get_board_history(session, 'MTSS')
    df = pd.DataFrame(data)
    df.set_index('TRADEDATE', inplace=True)
    # print(df.head(), '\n')
    # print(df.tail(), '\n')
    # df.info()
    SMA30 = pd.DataFrame()
    df['SMA30'] = df['CLOSE'].rolling(window=30).mean()
    SMA100 = pd.DataFrame()
    df['SMA100'] = df['CLOSE'].rolling(window=100).mean()
    # df['SMA30'] = SMA30['CLOSE']
    # df['SMA100'] = SMA100['CLOSE']
    df['BUY'] = df['SMA30'] > df['SMA100']
    df['SELL'] = df['SMA30'] < df['SMA100']
    res = df.query("""BUY == True or SELL == True""")
    print(res.to_string())
