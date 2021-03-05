import os
import pandas as pd
import numpy as np

# csvファイルからのダウンロード
# 絶対パスを通すといい。ダメなら実行構成を見直すこと
X = os.path.abspath("data/reserve.csv")
reserve_tb = pd.read_csv(X, encoding="utf-8")
