from preprocess.load_data.data_loader import load_production

production_tb = load_production()
from preprocess.load_data.data_loader import load_monthly_index

monthly_index_tb = load_monthly_index()

# 5-1 レコードデータにおけるモデル検証用のデータ分割
# 精度が落ちない程度の学習データ量を確保できる中で、なるべく小さな交差数を設定する(8とか)
# データ量に余裕があるときはミスを確認するためにホールドアウト検証(交差検証用のデータとは別のデータでモデルの精度を検証すること)を実施すること
# データ分割機能→sklearn
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import KFold
#
#
# train_test_split関数で学習データと検証データに分割
# train_data, test_data, train_target, test_target = \
#     train_test_split(production_tb.drop("fault_flg", axis=1),
#                      production_tb[["fault_flg"]],
#                      test_size=0.2)
#
# train_data.reset_index(inplace=True, drop=True)
# test_data.reset_index(inplace=True, drop=True)
# train_target.reset_index(inplace=True, drop=True)
# test_target.reset_index(inplace=True, drop=True)
#
# row_no_list = list(range(len(train_target)))
#
# KFold関数は交差検証の学習データと検証データに分割するための関数
# k_fold = KFold(n_splits=4, shuffle=True)
#
# for train_cv_no, test_cv_no in k_fold.split(row_no_list):
#     train_cv = train_data.iloc[train_cv_no, :]
#     test_cv = train_data.iloc[test_cv_no, :]
# print(train_cv)
# print(test_cv)

# 5-2 時系列データにおけるモデル検証用のデータ分割
# 時系列データの分割をかんたんに実現できるライブラリがないので、自分で実装する
# train_window_start = 0
# train_window_end = 23
# horizon = 12
# skip = 12
#
# monthly_index_tb.sort_values(by="year_month")
#
# while True:
#     test_window_end = train_window_end + horizon
#     train = monthly_index_tb[train_window_start:(train_window_end + 1)]
#     test = monthly_index_tb[(train_window_end + 1):(test_window_end + 1)]
#     if test_window_end >= len(monthly_index_tb.index):
#         break
#     train_window_start += skip
#     train_window_end += skip
