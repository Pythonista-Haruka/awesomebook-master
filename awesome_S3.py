import os
import pandas as pd

# csvファイルからのダウンロード
# 絶対パスを通すといい。ダメなら実行構成を見直すこと
X = os.path.abspath("reserve.csv")
reserve_tb = pd.read_csv(X, encoding="utf-8")

# 3-1 データ数、種類数の算出
# agg関数を用い、引数にdictionaryオブジェクトを取ることで集約処理をまとめて指定
# result = reserve_tb\
#     .groupby("hotel_id")\
#     .agg({"reserve_id": "count", "customer_id": "nunique"})
# reset_index関数で、列番号を振り直す
# result.reset_index(inplace=True)
# result.columns = ["hotel_id", "rsv_cnt", "cus_cnt"]

# 3-2 合計値の算出
# 集約処理が一つのみのときはagg関数よりも良い関数がある
# sum関数で合計を集約する
# result = reserve_tb\
#     .groupby(["hotel_id", "people_num"])["total_price"]\
#     .sum().reset_index()
# 列名を"price_sum"に変更
# result.rename(columns={"total_price": "price_sum"}, inplace=True)

# 3-3 極値、代表値の算出
# 最大、最小、平均、中央はそれぞれmax,min,mean,median関数を利用
# パーセンタイルはnp.percentileを使用し、そのラムダ式をaggの集約処理に指定する
# result = reserve_tb\
#     .groupby("hotel_id")\
#     .agg({"total_price": ["max", "min", "mean", "median", lambda x: np.percentile(x, q=20)]})\
#     .reset_index()
# result.columns = ["hotel_id", "price_max", "price_min", "price_mean", "price_median", "price_20%"]

# 3-4 ばらつき具合の算出
# 分散、標準偏差はそれぞれvar,std関数を使用
# n=1の場合はNAになってしまうので、fillna関数で0に置き換え
# result = reserve_tb\
#     .groupby("hotel_id")\
#     .agg({"total_price": ["var", "std"]}).reset_index()
# result.columns = ["hotel_id", "price_var", "price_std"]
# result.fillna(0, inplace=True)

# 3-5 最頻値の算出
# round関数で四捨五入した後に、mode関数で最頻値を算出
# reserve_tb["total_price"].round(-3).mode()

# 3-6 順位の算出
# rank関数により順位付け
# strでは順位付けできないため、先にdatetime型に変換
# reserve_tb["reserve_datetime"] = pd.to_datetime(reserve_tb["reserve_datetime"],
#                                                 format="%Y-%m-%d %H:%M:%S")
# log_noを新たな列として追加
# groupby関数で集約単位を指定
# reserve_tb["log_no"] = reserve_tb \
#     .groupby("customer_id")["reserve_datetime"] \
#     .rank(ascending=True, method="first")
# print(reserve_tb)

# 予約回数を計算
# rsv_cnt_tb = reserve_tb.groupby("hotel_id").size().reset_index()
# rsv_cnt_tb.columns = ["hotel_id", "rsv_cnt"]
# 予約回数をもとに順位を計算
# rsv_cnt_tb["rsv_cnt_rank"] = rsv_cnt_tb["rsv_cnt"] \
#     .rank(ascending=False, method="min")
# 必要のない列を削除
# rsv_cnt_tb.drop("rsv_cnt", axis=1, inplace=True)
