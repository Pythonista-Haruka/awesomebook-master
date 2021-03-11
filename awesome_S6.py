# 6-1 アンダーサンプリングによる不均衡データの調整
# §4, 5と同様の方法で実現可能
# 偏りのないランダムサンプリングを実現するためには、
# 事前にデータをクラスタリングし、作成されたクラスタごとにサンプリングする
# 貴重なサンプル数を減らすことになるので、なるべく使わないようにする

# 6-2 オーバーサンプリングによる不均衡データの調整
# True/False間で極端なデータ量の差がある場合、それを調整する必要がある
# SMOTEの実装→imblearnライブラリを使うのがシンプルで使いやすい
from preprocess.load_data.data_loader import load_production
from imblearn.over_sampling import SMOTE
production_tb = load_production()

# ratio="auto"部分が動作しない…
sm = SMOTE(ratio="auto", k_neighbors=5, random_state=71)

balance_data, balance_target = \
    sm.fit_sample(production_tb[["length", "thickness"]],
                  production_tb["fault_fig"])
