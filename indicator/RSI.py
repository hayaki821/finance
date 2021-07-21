import sys
sys.path.append('../')
from utils import * # libディレクトリ以下に設定した定数やutilクラスのインポート # 株価分析用に自作した関数をまとめたもの
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil 

# 銘柄コードの読み込み
stocks = get.topix1000()
print(stocks)
# resultデータフレーム作成
day = [1,3,5,10]  # 株価を確認する日（〇日後の株価）
col=["buy_sign_count"]
period = [9,14,22,42]   # RSIの設定期間
for d in day:
    col.append("roc_d"+str(d)+"_plus")
result = pd.DataFrame(data=0,index=range(len(period)),columns=col)
# rocマップのデータフレーム
col=[]
for p in period:
    for d in day:
        col.append("roc_p"+str(p)+"_d"+str(d))
index=[]
# 分布図の設定(-40~40%を2%間隔)
for i in range(-42,42,2):
    if(i==40):
        index.append(str(i)+"~")
    elif(i==-42):
        index.append("~"+str(i+2))
    else:
        index.append(str(i)+"~"+str(i+2))
roc_map = pd.DataFrame(data=0,index=index,columns=col)

for code in stocks.code:
    # 用意した株価データの読み込み
    code = str(code) +".T" 
    read_data = get.price(code)
    print(read_data)
    for p in range(len(period)):
        data = read_data.copy()

        # RSIを計算
        tech.rsi(data, period=period[p])
        data["buy_sign"] = False

        # タイミングを取得
        point = 20
        for i in range(len(data.index)-1):
            # 下回ったとき
            # if(data.rsi[i]>point and data.rsi[i+1]<=point):
            #     data["buy_sign"].iat[i+1] = True            
            # 下から上へ突破したとき
            if(data.rsi[i]<point and data.rsi[i+1]>=point):
                data["buy_sign"].iat[i+1] = True

        # 〇日後に上昇しているか確認    
        for bs in data.index[data.buy_sign]:
            for d in day:
                if(len(data.Close[:bs])+d<=len(data.Close)):
                    data.at[bs,"roc_d"+str(d)] = (data.Close[len(data.Close[:bs])+d-1]-data.Close[bs])/data.Close[bs]*100
                else:
                    # 〇日後の株価がない場合は最新の株価
                    data.at[bs,"roc_d"+str(d)] = (data.Close[-1]-data.Close[bs])/data.Close[bs]*100
                # 分布に振り分け
                roc_index = 20+ceil(data.at[bs,"roc_d"+str(d)]/2)
                if(roc_index<0):
                    roc_index=0
                elif(roc_index>41):
                    roc_index=41   
                roc_map.at[index[roc_index],"roc_p"+str(period[p])+"_d"+str(d)] += 1


# 上昇した数をカウント/roc分布を画像出力
for p in range(len(period)):
    result["buy_sign_count"].iat[p] = sum(roc_map.iloc[:,p*len(day)])
    for d in range(len(day)):
            result["roc_d"+str(day[d])+"_plus"].iat[p]=sum(roc_map.iloc[21:,p*len(day)+d])

            # roc分布を画像出力
            fig = plt.figure(figsize=(16, 12))
            ax = fig.add_subplot(111)
            bar_list = ax.bar(roc_map.index,roc_map["roc_p"+str(period[p])+"_d"+str(day[d])], width=1, color="#8ac6d1")
            [bar_list[i].set_color("#ffb6b9") for i in range(21)]
            ax.set_xticklabels(roc_map.index,rotation=90)
            ax.tick_params(labelsize=20)
            ax.grid(axis="y",c="lightgray")
            title = "RSI (period="+str(period[p])+", x day later="+str(day[d])+")"
            ax.set_title(title,fontsize=24)
            ax.set_xlabel("Rate of Change [%]", fontsize=24)
            ax.set_ylabel("counts", fontsize=24)
            fig.savefig(title+".png", bbox_inches='tight')

print(result)
