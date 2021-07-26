import sys
sys.path.append('../')
from utils import * # libディレクトリ以下に設定した定数やutilクラスのインポート # 株価分析用に自作した関数をまとめたもの
# list_stock_name = get.tokyo() # 東証上場銘柄リスト
list_stock_name = get.topix500() # TOPIX500銘柄リスト
dl.price_update(list_stock_name.code)


