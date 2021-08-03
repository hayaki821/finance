"""
ダイバージェンス・・・価格は上昇しているがオシレーター系のウェーブは下降・・下げの前兆
MACD特徴
１　直近の値に重みを付けた平均移動線（実際の動きに近い）＝EMAの差
2　１～３か月の中長期的なスパン？
３　比較的だましの影響を受けにくい

相場の勢いを表す、上がる上昇、傾きなしストップ、下がる下降
・欠点
ボックス相場に弱い
り各ポイントが遅くなりやすい
じり高じり安のそうばは信頼性が低い
急激な変化に弱い
数値的に売られすぎなどを出すのがむずい

MACDのダイバージェンス現象・・・２つのMACDゴールデンクロス間で株価は下落しているがMACDは上昇しているとき、
2回目のゴールデンクロスから大きく動く(逆もあり）

MACD 買いタイミング
１ ゴールデンクロス：MACDがシグナル（MACD(12,26,9)平均線）を下から上に突き抜けた時（0ラインより下）
２ ゼロクロス：MACDが0を突き抜けた時（マイナス⇒プラス）　MACDとそのシグナル両方
3 MACD(12,26)日線がMACD(12,26,9)平均線とクロスしたタイミング
４　ヒストグラムの反転に注目する
注意
MACD載せんが横ばいになってきたら（反転のタイミング？）
#　TODO
MACDがゴールデンクロスしてそれに伴いRSIも上がっていている間は上昇するか
「ストキャスティクス」と併用する
ダイバージェンスを利用
ヒストグラムの反転利用
"""


import sys
sys.path.append('../')
from utils import * # libディレクトリ以下に設定した定数やutilクラスのインポート # 株価分析用に自作した関数をまとめたもの
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil 
import os

# save dir
MACD_dir = "./MACD"
save_dir = MACD_dir + "/MACD_toukei"
if not os.path.isdir(MACD_dir):
    os.makedirs(MACD_dir)
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
# 銘柄コードの読み込み
stocks = get.topix500()

## resultデータフレーム
day = [1,3,5,10]    # 〇日後に上昇しているかの〇を設定
col=["g_p_count"]   # ゴールデンクロスの総数
period = [[6,19,9],[8,17,9],[12,26,9]] # 移動平均の期間
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
    code = change_stock_code(code)
    # コードのprice情報を読み取る
    #  date     High      Low     Open    Close    Volume     Adj Close
    read_data = get.price(code)
    
    for p in range(len(period)): 
        data = read_data.copy()
        # MACDを計算
        tech.macd(data, fastperiod=period[p][0], slowperiod=period[p][1], signalperiod=period[p][2])
        data["g_point"] = False

        # ゴールデンクロスのタイミングを取得
        for i in range(len(data.index)-1):
            if(data.macd[i]<data.signal[i] and data.macd[i+1]>data.signal[i+1]):
                data["g_point"].iat[i+1] = True

        # ゴールデンクロス時の傾き/角度を算出
        data["macd_line"] = np.nan
        data["signal_line"] = np.nan
        data["macd_slop"] = np.nan
        data["signal_slop"] = np.nan
        data["line_deg"] = np.nan
        for g in data.index[data.g_point]:
             # 2点間の直線を算出
             #  data.macd[g] -> 7.7542  
             a1 = data.macd[g] - data.macd[len(data.Close[:g])-1-1]
             b1 = data.macd[g] - a1*len(data.Close[:g])
             data["macd_slop"].at[g]=a1 
             a2 = data.signal[g] - data.signal[len(data.Close[:g])-1-1]
             b2 = data.signal[g] - a2*len(data.Close[:g])
             data["signal_slop"].at[g]=a2
             data["line_deg"].at[g] = np.rad2deg(np.arctan(abs((a1-a2)/(1+a1*a2))))
             #print(data)
             # plot用に直線データ追加
            #  for i in range(7):
            #     x = len(data.Close[:g])-1+i-3
                 
            #     data["macd_line"].iat[x]= a1*x+b1
            #     data["signal_line"].iat[x]= a2*x+b2

        # 除くゴールデンクロスを選択        
        for g in data.index[data.g_point]:
            # 角度の条件設定
            if(data["line_deg"].at[g] < 30):
                data["g_point"].at[g] = False

            # 位置
            # if(data["macd"].at[g] > -data["Close"].at[g]*0.01):
            #     data["g_point"].at[g] = False

        # 〇日後に上昇しているか確認
        for g in data.index[data.g_point]:
            for d in day:
                # len(data.Close) = 値がある数（日数）、len(data.Close[:g]　= 今何日目かみたいな
                # 何%あがったか下がったかをroc_d +dにいれる
                if(len(data.Close[:g])+d<=len(data.Close)):
                    data.at[g,"roc_d"+str(d)] = (data.Close[len(data.Close[:g])+d-1]-data.Close[g])/data.Close[g]*100
                else:
                    data.at[g,"roc_d"+str(d)] = (data.Close[-1]-data.Close[g])/data.Close[g]*100

                if(data.at[g,"roc_d"+str(d)]>0):
                    data.at[g,"roc_d"+str(d)+"_point"] = 1
                else:
                    data.at[g,"roc_d"+str(d)+"_point"] = 0
                # 分布に振り分け
                # 20が原点位置になる
                roc_index = 20+ceil(data.at[g,"roc_d"+str(d)]/2)
                if(roc_index<0):
                    roc_index=0
                elif(roc_index>41):
                    roc_index=41   
                roc_map.at[index[roc_index],"roc_p"+str(period[p])+"_d"+str(d)] += 1
        # 上昇していたらカウンタを加算
        data.dropna(inplace=True)
        if(len(data.index[data.g_point])>0):
            result["g_p_count"].iat[p] += len(data.index)
            for d in day:
                result["roc_d"+str(d)+"_plus"].iat[p]+=sum(data["roc_d"+str(d)+"_point"])
        # print(data) ここまでのデータ構造 [61 rows x 23 columns]
        #  High     Low    Open   Close     Volume    Adj Close        macd      signal      hist  g_point   
        # macd_line  signal_line  macd_slop  signal_slop   line_deg    roc_d1  roc_d1_point     roc_d3  roc_d3_point    
        #  roc_d5  roc_d5_point    roc_d10  roc_d10_point
# 上昇した数をカウント/roc分布を画像出力
for p in range(len(period)):
    result["g_p_count"].iat[p] = sum(roc_map.iloc[:,p*len(day)])
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
        title = "MACD (period="+str(period[p])+", x day later="+str(day[d])+")"
        ax.set_title(title,fontsize=24)
        ax.set_xlabel("Rate of Change [%]", fontsize=24)
        ax.set_ylabel("counts", fontsize=24)
        fig.savefig(save_dir + "/" + title +".png", bbox_inches='tight')

print(result)
