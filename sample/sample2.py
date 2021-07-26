import pandas as pd
import sys
sys.path.append('../')
from utils import * # libディレクトリ以下に設定した定数やutilクラスのインポート # 株価分析用に自作した関数をまとめたもの

list_stock_name = get.topix500() # TOPIX500銘柄リスト

df = pd.DataFrame()
for stock_name in list_stock_name.code:
    stock_name = change_stock_code(stock_name)
    df_new = get.price(stock_name)['Close']
    df_new.name = stock_name
    df = pd.concat([df, df_new], axis=1)
print(df)


