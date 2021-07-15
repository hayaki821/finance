import yfinance as yf
import time
start = time.time()

ticker = yf.Ticker("7203.T")
hist = ticker.history(period="max")
# 価格ヒストリカルデータを取得
print('価格ヒストリカルデータ')
print(hist)

# 損益計算書 直近3~4年分？
# 特に重要なのは、Total Revenue(売上高)、Operating Income(営業利益)、Net Income(当期純利益)あたり
financials = ticker.financials
print('損益計算書')
print(financials)

# 貸借対照表（バランスシート）直近3~4年分？
# Total Assets(総資産)、Total Liab(総負債)、Total Stockholder Equity(自己資本)あたり
balance_sheet = ticker.balance_sheet
print('貸借対照表（バランスシート）')
print(balance_sheet)

# キャッシュフロー計算書 直近3~4年分？
# Total Cashflows From Operating Activities(営業キャッシュフロー)、
# Total Cashflows From Financing Activities(財務キャッシュフロー)、
# Total Cashflows From Investing Activities(投資キャッシュフロー)あたり
cashflow = ticker.cashflow
print('キャッシュフロー計算書')
print(cashflow)


# 銘柄のサマリー
# marketCap(時価総額)、sharesOutstanding(発行株数)、forwardPE(予測PER)、
# dividendYield(配当利回り)、profitMargins(純利益比率)など
info = ticker.info
print('銘柄のサマリー')
print(info)


# 複数銘柄を同時に取得する場合はTickersクラスを使い、引数はスペースで区切ります
tickers = yf.Tickers("7203.T 9984.T 6861.T")
hists = []
for key in tickers.tickers.keys():
    #print(tickers.tickers)
    hists.append(tickers.tickers[key].history())
print(hists[0])

# 株価以外のデータ取得（為替）
import pandas as pd
# 株海外に取れる為替データの一部
#indices = ["^N225", "^DJI", "^GSPC", "^IXIC", "^GDAXI", "^FTSE", "^FCHI", "^HSI", 
# "^SSEC", "^BVSP", "^KOSPI"]
fxs = ["JPY=X", "EURUSD=X", "GBPUSD=X"]
tickers = yf.Tickers(" ".join(fxs))

closes = []
for key in tickers.tickers.keys():
    closes.append(tickers.tickers[key].history(period="max").Close)

df = pd.DataFrame(closes).T
df.columns = fxs
print('株価以外のデータ取得（為替）')
print(df)


elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
