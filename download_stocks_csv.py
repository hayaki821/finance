import yfinance as yf
import time
import pandas as pd

stocks=[ "7203.T", "9984.T", "6861.T" ]

# [date,open, hight, low, close, volume, dividends,stock splits, 5day,25day, 75day ]
def download_stock_scv(stock):
    tickerTag = yf.Ticker(stock)
    df = pd.DataFrame(tickerTag.history(period="max"))
    ### Calc Average Moving
    df["5day"] = df["Close"].rolling(5).mean()
    df["25day"] = df["Close"].rolling(25).mean()
    df["75day"] = df["Close"].rolling(75).mean()
    df.to_csv("data/tickertag{}.csv".format(stock))

for stock in stocks:
    download_stock_scv(stock)

