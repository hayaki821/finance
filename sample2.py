import datetime
import numpy as np
import codecs
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import time
start = time.time()

# 銘柄リストの読み込み topix500
# 取得サイト https://www.jpx.co.jp/markets/statistics-equities/misc/01.html
data = pd.read_csv("topix500_20210531.csv")
print('銘柄リストの読み込み(topix500)')
print(data)

stocks = [str(s)+".T" for s in data.code]
stocks.append("^N225")
tickers = yf.Tickers(" ".join(stocks))
# print(stocks)

# 終値データフレームの作成
# yfinanceで価格系列のヒストリカルデータを入手し、
# その中から終値のデータをデータフレームにまとめ
closes   = [] # 終値

for key in tickers.tickers.keys():
    closes.append(tickers.tickers[key].history(period="max").Close)

closes = pd.DataFrame(closes).T   # DataFrame化
closes.columns = stocks           # カラム名の設定
closes = closes.ffill()           # 欠損データの補完

#print(closes)

# 当期純利益データフレームの作成
# PERとROEを算出するための当期純利益
earnings = [] # 当期純利益

dummy = tickers.tickers["1332.T"].financials.T["Net Income"]
dummy[:] = np.nan
print(dummy)
for key in tickers.tickers.keys():
    try:
        earnings.append(tickers.tickers[key].financials.T["Net Income"])
    except:
        earnings.append(dummy)       # エラー発生時はダミーを入れる

earnings = pd.DataFrame(earnings).T  # DataFrame化
earnings.columns = stocks            # カラム名の設定

print(earnings)

# 自己資本データフレームの作成
# ROEを算出するための自己資本です。
equity   = [] # 自己資本

dummy = tickers.tickers["1332.T"].balance_sheet.T["Total Stockholder Equity"]
dummy[:] = np.nan

for key in tickers.tickers.keys():
    try:
        equity.append(tickers.tickers[key].balance_sheet.T["Total Stockholder Equity"])
    except:
        equity.append(dummy)         # エラー発生時はダミーを入れる

equity = pd.DataFrame(equity).T      # DataFrame化
equity.columns = stocks              # カラム名の設定

print(equity)

# 発行株数データフレームの作成
# PERを算出するためにはEPS（一株益）が必要です。EPSを算出するために発行株数データフレームを作ります。
shares   = [] # 発行株数

for key in tickers.tickers.keys():
    try:
        shares.append(tickers.tickers[key].info["sharesOutstanding"])
    except:
        shares.append(np.nan)        # エラー発生時はNAN値を入れる

shares = pd.Series(shares)           # Series化 一次元のデータを収納するために使われる
shares.index = stocks                # インデックス名の設定

print(shares)

# EPS、ROEデータフレームの作成
# 当期純利益、自己資本、発行株数のデータからEPS、ROEデータフレームを作る
eps = earnings/shares.values      # EPS （1株当たりの利益）＝当期純利益÷発行済株式総数
roe = earnings/equity             # ROE （自己資本利益率(％）＝当期純利益 ÷ 自己資本（期中平均） × 100

eps = eps.ffill()                 # 欠損データの補完
roe = roe.ffill()

eps = eps.drop(["^N225"], axis=1) # ^N225カラムは削除しておく
roe = roe.drop(["^N225"], axis=1)

print(eps)
print(roe)

# 終値データフレームの整形、および月次リターンデータフレームの作成
# 月次データ用にデータ整形し、それから
# 月次リターンデータフレーム（マーケットリターンを差し引いたもの）を作る
closes["month"] = closes.index.month                                      # 月カラムの作成
closes["end_of_month"] = closes.month.diff().shift(-1)                    # 月末フラグカラムの作成
closes = closes[closes.end_of_month != 0]                                 # 月末のみ抽出

monthly_rt = closes.pct_change().shift(-1)                                # 月次リターンの作成(ラグあり)
monthly_rt = monthly_rt.sub(monthly_rt["^N225"], axis=0)                  # マーケットリターン控除

closes = closes[closes.index > datetime.datetime(2017, 4, 1)]             # 2017年4月以降
monthly_rt = monthly_rt[monthly_rt.index > datetime.datetime(2017, 4, 1)]

closes = closes.drop(["^N225", "month", "end_of_month"], axis=1)          # 不要なカラムを削除
monthly_rt = monthly_rt.drop(["^N225", "month", "end_of_month"], axis=1)

print(closes)
print(monthly_rt)

# PER、ROEデータフレームの作成（月次リターンと同次元）
# 最後に月次リターンど同次元になるようにPER、ROEデータフレームを作成
eps_df = pd.DataFrame(index=monthly_rt.index, columns=monthly_rt.columns) # 月次リターンと同次元のDF作成
roe_df = pd.DataFrame(index=monthly_rt.index, columns=monthly_rt.columns)

for i in range(len(eps_df)):                                              # 各行への代入
    eps_df.iloc[i] = eps[eps.index < eps_df.index[i]].iloc[-1]

for i in range(len(roe_df)):
    roe_df.iloc[i] = roe[roe.index < roe_df.index[i]].iloc[-1]

per_df = closes/eps_df       # error 0で割った場合                                             # PERデータフレームの作成

print(per_df)
print(roe_df)

# データの結合
# これらのデータフレームを1つにまとめます。
stack_monthly_rt = monthly_rt.stack()                                  # 1次元にスタック
stack_per_df = per_df.stack()
stack_roe_df = roe_df.stack()

df = pd.concat([stack_monthly_rt, stack_per_df, stack_roe_df], axis=1) # 結合
df.columns = ["rt", "per", "roe"]                                      # カラム名の設定

df["rt"][df.rt > 1.0] = np.nan                                         # 異常値の除去

print(df)

# 対象銘柄の抽出とプロット
value_df = df[(df.per < 10) & (df.roe > 0.1)]       # 割安でクオリティが高い銘柄を抽出

plt.hist(value_df["rt"])                            # ヒストグラムの描画
plt.show()

balance = value_df.groupby(level=0).mean().cumsum() # 累積リターンを作成

plt.clf()
plt.plot(balance["rt"])                             # バランスカーブの描画
plt.show()

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")