import os
import pandas as pd
import numpy as np
import gc
import datetime
from dateutil.relativedelta import relativedelta

# csvファイルからのダウンロード
# 絶対パスを通すといい。ダメなら実行構成を見直すこと
X = os.path.abspath("data/reserve.csv")
Y = os.path.abspath("data/hotel.csv")
Z = os.path.abspath("data/customer.csv")
reserve_tb = pd.read_csv(X, encoding="utf-8")
hotel_tb = pd.read_csv(Y, encoding="utf-8")
customer_tb = pd.read_csv(Z, encoding="utf-8")

# 4-1 マスタテーブルの結合
# 結合前にデータを抽出し、無駄な結合処理を省略すること
# pd.merge(reserve_tb.query("people_num==1"), hotel_tb.query("is_business"), on="hotel_id",
#          how="inner")
# これにより宿泊人数が1人のビジネスホテルの予約レコードが抽出できる

# 4-2 条件に応じた結合テーブルの切り替え
# ガベージコレクションを先に開放しておく
# small_area_nameごとにホテル数をカウント
# small_area_mst = hotel_tb \
#     .groupby(["big_area_name", "small_area_name"], as_index=False) \
#     .size().reset_index()
#
# indexが残る形になっていたので修正
# small_area_mst.drop('index', axis=1, inplace=True)
# small_area_mst.columns = ["big_area_name", "small_area_name", "hotel_cnt"]
#
# np.whereを活用し、条件に応じて返す値を変更する。
# 20件以上であればjoin_area_idをsmall_area_nameとして設定
# 20件未満であればjoin_area_idをbig_area_nameとして設定
# -1は、自ホテルを引いている
# small_area_mst["join_area_id"] = \
#     np.where(small_area_mst["hotel_cnt"] - 1 >= 20,
#              small_area_mst["small_area_name"],
#              small_area_mst["big_area_name"])
#
# 必要なくなった列を削除
# small_area_mst.drop(["hotel_cnt", "big_area_name"], axis=1, inplace=True)
#
# レコメンド元になるホテルにsmall_area_mstを結合することで、join_area_idを設定
# base_hotel_mst = pd.merge(hotel_tb, small_area_mst, on="small_area_name") \
#                      .loc[:, ["hotel_id", "join_area_id"]]
#
# del small_area_mst
# gc.collect()
#
# recommend_hotel_mstはレコメンド候補のためのテーブル
# recommend_hotel_mst = pd.concat([hotel_tb[["small_area_name", "hotel_id"]] \
#                                 .rename(columns={"small_area_name": "join_area_id"}, inplace=False),
#                                  hotel_tb[["big_area_name", "hotel_id"]] \
#                                 .rename(columns={"big_area_name": "join_area_id"}, inplace=False)
#                                  ])
# hotel_idの列名が結合すると重複するので変更
# recommend_hotel_mst.rename(columns={"hotel_id": "rec_hotel_id"}, inplace=True)
# base_hotel_mstとrecommend_hotel_mstを結合し、レコメンド候補の情報を付与
# query関数によってレコメンド候補から自分を除く
# pd.merge(base_hotel_mst, recommend_hotel_mst, on="join_area_id") \
#     .loc[:, ["hotel_id", "rec_hotel_id"]] \
#     .query("hotel_id != rec_hotel_id")
# print(recommend_hotel_mst)
# これにより、レコメンド候補のホテルを紐付けたデータを作成した。

# 4-3 過去データの結合
# lag関数の代わりにshift関数を利用することで、n件前のデータを抽出する
# 2件前の抽出
# result = reserve_tb \
#     .groupby("customer_id") \
#     .apply(lambda group: group.sort_values(by="reserve_datetime", axis=0, inplace=False))
# result["before_price"] = \
#     result["total_price"].groupby("customer_id").shift(periods=2)

# 合計値を計算するWindow関数はないけど、データをWindowに区切るrolling関数を使う。
# 2件前までの3回の合計予約金額情報の付与
# result = reserve_tb.groupby("customer_id") \
#     .apply(lambda x: x.sort_values(by="reserve_datetime", ascending=True)) \
#     .reset_index(drop=True)
#
# result["price_avg"] = pd.Series(
#     result.groupby("customer_id")["total_price"].rolling(center=False, window=3,
#                                                          min_periods=1).mean().reset_index(
#         drop=True))
# print(result)
# rolling関数を使用すると可読性が大きく低下するので、できればSQLを使用したほうが良い

# 4-4 全結合
# 結合するテーブル同士のすべての組み合わせをかけ合わせる全結合では、データ数が膨大になるため、
# 必要最低限の範囲で全結合すること
# 2017年1月~3月の月間合計利用料金を計算
# month_mst = pd.DataFrame({"year_month": [
#     (datetime.date(2017, 1, 1) + relativedelta(months=x)).strftime("%Y%m") for x in range(0, 3)]})
# customer_tb["join_key"] = 0
# month_mst["join_key"] = 0
#
# customer_mst = pd.merge(customer_tb[["customer_id", "join_key"]], month_mst, on="join_key")
#
# reserve_tb["year_month"] = reserve_tb["checkin_date"] \
#     .apply(lambda x: pd.to_datetime(x, format="%Y-%m-%d").strftime("%Y%m"))
#
# summary_result = pd.merge(
#     customer_mst,
#     reserve_tb[["customer_id", "year_month", "total_price"]],
#     on=["customer_id", "year_month"], how="left"
# ).groupby(["customer_id", "year_month"])["total_price"] \
#           .sum().reset_index()
#
# summary_result.fillna(0, inplace=True)
# print(summary_result)
