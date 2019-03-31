# -*- coding: UTF-8 -*-
import pandas as pd
from scipy import stats
import numpy as np
from util import date_utils

STOCK_NAMES = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE"]
DAY_LEN = 2434
csv_file = 'data/temp_pb.csv'
HISTORY_FILE = 'data/temp_history.csv'


def generate_history_csv():
    temp_pb = pd.read_csv(csv_file, encoding='utf-8')
    size = None
    date_index = []
    history_result = pd.DataFrame()
    for loc, name in enumerate(STOCK_NAMES[1:]):
        stock_data = temp_pb[name]
        result = []
        for index, per_day in enumerate(stock_data):
            # 只计算20006年后的数据
            date = temp_pb[STOCK_NAMES[0]][index]
            if date.startswith('2005'):
                break
            if loc == 0:
                date_index.append(date)

            # 去除空值
            stock_data = stock_data[stock_data.notnull()]
            a = stock_data[index: DAY_LEN + index]
            if len(a) > 0:
                p = stats.percentileofscore(a, a[index])
                result.append(p)
            else:
                result.append(None)
        if size is None:
            size = len(result)
        elif len(result) < size:
            result = np.add([None for i in range(size)], result)
        # y_axises.append(result)
        history_result.insert(loc, name, result)
    history_result.insert(0, STOCK_NAMES[0], date_index)
    history_result.to_csv(HISTORY_FILE, index=False, encoding='utf-8', decimal='.')


def get_history_data(date):
    df = pd.read_csv(HISTORY_FILE)
    data = df.loc[df[STOCK_NAMES[0]] == date_utils.lxrDate2csvDate(date)]
    result = data.values
    if len(result) > 0:
        return result[0]
    else:
        return None


# result = get_history_data('2012')
# print(result)
# y_axises = []
# generate_history_csv()

# import wendu_trend_chart
# wendu_trend_chart.generate(STOCK_NAMES[1:], date_index, y_axises)