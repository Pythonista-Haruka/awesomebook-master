import pandas as pd
from preprocess.load_data.data_loader import load_hotel_reserve

customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

# 7-1 横持ちへの変換
# pivot_table関数を使用、集約処理も同時にできる
print(pd.pivot_table(reserve_tb, index="customer_id", columns="people_num",
                     values="reserve_id",
                     aggfunc=lambda x: len(x), fill_value=0))

# 7-2 スパースマトリックスへの変換
# スパースマトリックスのライブラリを読み込み
from scipy.sparse import csc_matrix

cnt_tb = reserve_tb \
    .groupby(["customer_id", "people_num"])["reserve_id"].size() \
    .reset_index()
cnt_tb.columns = ["customer_id", "people_num", "rsv_cnt"]

customer_id = pd.Categorical(cnt_tb["customer_id"])
people_num = pd.Categorical(cnt_tb["people_num"])

print(csc_matrix((cnt_tb["rsv_cnt"], (customer_id.codes, people_num.codes)),
                 shape=(len(customer_id.categories), len(people_num.categories))))
