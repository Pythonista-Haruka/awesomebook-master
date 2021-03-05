import os
import pandas as pd
import numpy as np

# csvファイルからのダウンロード
# 絶対パスを通すといい
X = os.path.abspath("reserve.csv")
reserve_tb = pd.read_csv(X, encoding="utf-8")

# 2-1 データ列による抽出
# ①列名指定
# print(reserve_tb[["reserve_id", "hotel_id", "customer_id", "reserve_datetime", "checkin_date",
#                   "checkout_date"]])
# ②列名指定 part2
# print(reserve_tb.loc[:,
#       ["reserve_id", "hotel_id", "customer_id", "reserve_datetime", "checkin_date",
#        "checkout_date"]])
# ③drop関数により不要な列を削除し、書き換え
# reserve_tb.drop(["people_num", "total_price"], axis=1, inplace=True)
# print(X)

# 2-2 条件指定による抽出
# query関数により条件にあったデータ行を抽出
# reserve_tb.query('"2016-10-13" <= checkout_date <= "2016-10-14"')

# 2-3 データ値に基づかないサンプリング
# pandasライブラリのsample関数によりサンプリング
# n=で件数、frac=で割合を指定
# reserve_tb.sample(frac=0.5)

# 2-4 集約IDに基づくサンプリング
# unique関数によりSeriesの値の重複を排除したSeriesを取得
# target = pd.Series(reserve_tb["customer_id"].unique()).sample(frac=0.5)
# isin関数により、サンプリングした顧客IDのいずれかに一致した行を抽出
# print(reserve_tb[reserve_tb["customer_id"].isin(target)])
