import sys
sys.path.append('../')
from utils import * # libディレクトリ以下に設定した定数やutilクラスのインポート # 株価分析用に自作した関数をまとめたもの
import pandas as pd
# メモリリーク問題を防ぐ
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import ceil 
import os
from datetime import datetime    # "datetime" オブジェクトによる時刻計算
# 1なら個別の株のRSIのグラフを生成
plt_stock_rsi = 1

# タイミングを取得　RSIがこのpointを基準にする
point = 25
save_dir = "./RSI_up_toukei_p"+ str(point) 
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
# 銘柄コードの読み込み
# stocks = ["7203"]
stocks = get.topix500()
# resultデータフレーム作成
day = [1,3,5,10]  # 株価を確認する日（〇日後の株価）
stock_rsi_save_dir = "./RSI_stocks_graph"
col=["buy_sign_count"]
period = [14]   # RSIの設定期間
for d in day:
    col.append("roc_d"+str(d)+"_plus")
    col.append("rocUp_d"+str(d)+"_plus")
result = pd.DataFrame(data=0,index=range(len(period)),columns=col)
# rocマップのデータフレーム
col=[]
for p in period:
    for d in day:
        col.append("rocUp_p"+str(p)+"_d"+str(d))
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


if not os.path.isdir(stock_rsi_save_dir):
    os.makedirs(stock_rsi_save_dir)
for code in stocks.code:
    # 用意した株価データの読み込み
    code = change_stock_code(code)
    # コードのprice情報を読み取る
    #  date     High      Low     Open    Close    Volume     Adj Close
    read_data = get.price(code)

    # period=14固定
    for p in range(len(period)):
        data = read_data.copy()

        # RSIを計算
        tech.rsi(data, period=period[p])
        data["buy_sign"] = False
        data["buy_sign_up"] = False
        # ここまででカラムに rsi  buy_sign追加

        for i in range(len(data.index)-1):
            # 下回ったとき
            # if(data.rsi[i]>point and data.rsi[i+1]<=point):
            #     data["buy_sign"].iat[i+1] = True            
            # 下から上へ突破したとき
            if(data.rsi[i]<point and data.rsi[i+1]>=point):
                # iat = 行番号
                data["buy_sign"].iat[i+1] = True
            # rsiがpointより下で当日より、次の日が上がっていて、前の日よりも下がっているとき
            if(data.rsi[i]<point and data.rsi[i+1]>data.rsi[i] and data.rsi[i-1]>=data.rsi[i]):
                # iat = 行番号
                data["buy_sign_up"].iat[i+1] = True


        # 〇日後に上昇しているか確認
        # ex) data.index[data.buy_sign] = DatetimeIndex(['2019-04-12', '2020-03-17'], dtype='datetime64[ns]', name='Date', freq=None)
        for bs in data.index[data.buy_sign]:
            for d in day:
                # len(data.Close) = 値がある数（日数）、len(data.Close[:bs]　= 今何日目かみたいな
                # 何%あがったか下がったかをroc_d +dにいれる
                if(len(data.Close[:bs])+d<=len(data.Close)):
                    data.at[bs,"roc_d"+str(d)] = (data.Close[len(data.Close[:bs])+d-1]-data.Close[bs])/data.Close[bs]*100
                else:
                    # 〇日後の株価がない場合は最新の株価
                    data.at[bs,"roc_d"+str(d)] = (data.Close[-1]-data.Close[bs])/data.Close[bs]*100
                # 分布に振り分け
                # 20が原点位置になる
                roc_index = 20+ceil(data.at[bs,"roc_d"+str(d)]/2)
                if(roc_index<0):
                    roc_index=0
                elif(roc_index>41):
                    roc_index=41   
                roc_map.at[index[roc_index],"rocUp_p"+str(period[p])+"_d"+str(d)] += 1
        for bs in data.index[data.buy_sign_up]:
            for d in day:
                # len(data.Close) = 値がある数（日数）、len(data.Close[:bs]　= 今何日目かみたいな
                # 何%あがったか下がったかをroc_d +dにいれる
                if(len(data.Close[:bs])+d<=len(data.Close)):
                    data.at[bs,"rocUp_p"+str(d)] = (data.Close[len(data.Close[:bs])+d-1]-data.Close[bs])/data.Close[bs]*100
                else:
                    # 〇日後の株価がない場合は最新の株価
                    data.at[bs,"rocUp_p"+str(d)] = (data.Close[-1]-data.Close[bs])/data.Close[bs]*100
                # 分布に振り分け
                # 20が原点位置になる
                roc_index = 20+ceil(data.at[bs,"rocUp_p"+str(d)]/2)
                if(roc_index<0):
                    roc_index=0
                elif(roc_index>41):
                    roc_index=41   
                roc_map.at[index[roc_index],"rocUp_p"+str(period[p])+"_d"+str(d)] += 1
        xlim=["20150101","20220101"]
        high = max(data["High"])
        low = min(data["Low"])
        plot_starting_dtobject = datetime.strptime(xlim[0], "%Y%m%d")  # datetime object of datetime module = dtobject
        plot_ending_dtobject   = datetime.strptime(xlim[1],   "%Y%m%d") 
        plot_starting_time = datetime.timestamp(plot_starting_dtobject)
        plot_ending_time = datetime.timestamp(plot_starting_dtobject)
        if plt_stock_rsi == 1:
            ymin, ymax = 0,100
            fig = plt.figure(figsize=[32, 4])
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
            #plt.subplots(figsize=(8.0, 6.0))
            #data.plot.line(style=['b.-'])
            #data.plot(subplots=True,figsize=[40, 4],y=['rsi','Close'],style=['b.-'],grid=True,xlim=xlim)
            ax1.plot(data["Close"])
            ax1.set_ylabel('Close')
            ax1.vlines(data.index[data.buy_sign], low, high, colors='red', linestyle='dashed')
            ax1.set_xlim(plot_starting_dtobject, plot_ending_dtobject) 
            ax2.plot(data["rsi"])
            ax2.set_ylabel('RSI')
            ax2.vlines(data.index[data.buy_sign], 0, 100, colors='red', linestyle='dashed')
            ax2.set_xlim(plot_starting_dtobject, plot_ending_dtobject)
            fig.savefig( stock_rsi_save_dir + "/" + code+'.png')
            plt.cla()   # clear axis ################################################################################################################################# Python3 
            plt.clf() 
            plt.close('all')



# 上昇した数をカウント/roc分布を画像出力
for p in range(len(period)):
    result["buy_sign_count"].iat[p] = sum(roc_map.iloc[:,p*len(day)])
    for d in range(len(day)):
        result["rocUp_d"+str(day[d])+"_plus"].iat[p]=sum(roc_map.iloc[21:,p*len(day)+d])

        # roc分布を画像出力
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        bar_list = ax.bar(roc_map.index,roc_map["rocUp_p"+str(period[p])+"_d"+str(day[d])], width=1, color="#8ac6d1")
        [bar_list[i].set_color("#ffb6b9") for i in range(21)]
        ax.set_xticklabels(roc_map.index,rotation=90)
        ax.tick_params(labelsize=20)
        ax.grid(axis="y",c="lightgray")
        # TODO stock code name
        title = " RSI (period="+str(period[p])+", x day later="+str(day[d])+")"
        ax.set_title(title,fontsize=24)
        ax.set_xlabel("Rate of Change [%]", fontsize=24)
        ax.set_ylabel("counts", fontsize=24)
        win = round(result.at[p,"rocUp_d"+str(day[d])+"_plus"]/result.at[p,"buy_sign_count"]*100,1)
        fig.text(0.75,0.5,"{:}%".format(win),size=40,color="#7dc4d1")
        fig.text(0.17,0.5,"{:}%".format(100-win),size=40,color="#ffa8ac")
        fig.savefig( save_dir + "/" + title+".png", bbox_inches='tight')

print(result)
