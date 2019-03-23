# -*- coding: UTF-8 -*-

import pandas as pd
from scipy import stats


# 六种指数PBt统计
STOCK_NAME = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE"]
DAY_LEN = 2434


def get_percentile_data(csv_file):
    temp_pb = pd.read_csv(csv_file, encoding='utf-8')
    result = []
    for name in STOCK_NAME[1:]:
        a = temp_pb[name]
        a = a[a.notnull()]
        a = a[0: DAY_LEN]
        p = stats.percentileofscore(a, a[0])
        result.append(round(p, 1))
    return temp_pb[STOCK_NAME[0]][0], result

# insertRow = pd.DataFrame([t],columns=stockNames)
# new = insertRow.append(temp_pb.loc[:], ignore_index=True)
# temp_pb.to_csv('add.csv', index=False, encoding='utf-8', decimal='.')


