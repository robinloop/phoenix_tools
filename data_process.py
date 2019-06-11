# -*- coding: UTF-8 -*-

import pandas as pd
from scipy import stats
import requests
import datetime

URL_INDICE_FUNDAMENTAL = "https://open.lixinger.com/api/a/indice/fundamental"
TOKEN = "8ec3e830-0fe7-4734-844c-e23d6ea119e2"

# 六种指数PBt统计
STOCK_NAMES = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE", "中证全指指数"]
stockCodes = ["1000004", "399006", "1000002", "000016", "000300", "000905", "399975"]
DAY_LEN = 2434
STOCK_NAMES_LEN = len(STOCK_NAMES)
HISTORY_FILE = 'data/temp_history.csv'


def get_percentile_data(csv_file):
    result = data_process(csv_file)
    return csvDate2lxrDate(result[0]), [round(i, 1) for i in result[1:9]]


def data_process(csv_file):
    temp_pb = pd.read_csv(csv_file, encoding='utf-8')
    temp_history = pd.read_csv(HISTORY_FILE, encoding='utf-8')

    start_date = temp_pb[STOCK_NAMES[0]][0]
    start_date_fix = csvDate2lxrDate(start_date)
    if check_today(start_date_fix):
        # CSV文件数据已经是最新的，无需再下载
        return temp_history.loc[0]

    new_data = get_new_data(start_date_fix)
    if new_data.index.values.size == 0:
        print('CSV数据已是最新 ', start_date_fix)
        return temp_history.loc[0]
    full_data = new_data.append(temp_pb, ignore_index=True)

    new_history_result = temp_history_process(temp_history, full_data, new_data)

    # 处理成功再保存数据
    full_data.to_csv(csv_file, index=False, encoding='utf-8', decimal='.')

    return new_history_result.loc[0]


def temp_history_process(temp_history, full_data, new_data):
    new_history_result = pd.DataFrame()
    new_history_result.insert(0, STOCK_NAMES[0], new_data[STOCK_NAMES[0]])
    # 计算新增数据的温度数据
    for loc, name in enumerate(STOCK_NAMES[1:]):
        stock_data = full_data[name]
        result = []
        if STOCK_NAMES[-1] == name:
            result = new_data[name]
        else:
            for index, per_day in enumerate(new_data[name]):
                # 去除空值
                stock_data = stock_data[stock_data.notnull()]
                a = stock_data[index: DAY_LEN + index]
                p = stats.percentileofscore(a, a[index])
                result.append(p)

        new_history_result.insert(loc + 1, name, result)

    history_full_data = new_history_result.append(temp_history, ignore_index=True)
    history_full_data.to_csv(HISTORY_FILE, index=False, encoding='utf-8', decimal='.')
    return new_history_result


def get_new_data(start_date_fix):
    new_data = pd.DataFrame()
    zzqz = []
    for index, stock_code in enumerate(stockCodes):
        result_data = download_data(stock_code, start_date_fix)

        dates = []
        pbs = []
        pes = []
        cps = []
        for data in result_data:
            if start_date_fix == data['date']:
                # 开始日期的数据在csv中已存在，不需要再放入新的data frame
                continue
            pes.append(data['pe'])
            pbs.append(data['pb'])
            cps.append(data['cp'])
            dates.append(lxrDate2csvDate(data['date']))
        if index == 0:
            # 日期只需要插入一次即可
            new_data.insert(0, STOCK_NAMES[0], dates)
        new_data.insert(index + 1, STOCK_NAMES[index + 1], pbs)

        if stock_code == stockCodes[-1]:
            new_data.insert(index + 2, STOCK_NAMES[index + 2], pes)
        elif stock_code == stockCodes[2]:
            zzqz = cps
    new_data.insert(index + 3, STOCK_NAMES[index + 3], zzqz)
    return new_data


def csvDate2lxrDate(start_date):
    date_arr = start_date.split('/')
    year = date_arr[0]
    month = date_arr[1]
    if len(month) == 1:
        month = "0" + month
    day = date_arr[2]
    if len(day) == 1:
        day = "0" + day
    return '-'.join([year, month, day])


def lxrDate2csvDate(start_date):
    date_arr = start_date.split('-')
    year = date_arr[0]
    month = str(int(date_arr[1]))
    day = str(int(date_arr[2]))
    return '/'.join([year, month, day])


def check_today(start_date):
    """
    判断csv文件的最新日期是否是今天
    :param start_date:
    :return:
    """
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.datetime.now()
    dd = d2 - d
    if dd.days == 0:
        return True
    return False


def download_data(stockCode, startDate):
    request_data = {
        "token": TOKEN,
        "stockCodes": [stockCode],
        "metrics": ["pb.median", "pe_ttm.median", "cp"],
        "startDate": startDate
    }
    result = requests.post(URL_INDICE_FUNDAMENTAL, json=request_data)
    result_data = []

    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            split_date = data['date'].split('T')
            pb_data = {
                'date': split_date[0],
                'pb': data['pb']['median'],
                'pe': data['pe_ttm']['median'],
                'cp': data['cp']
            }
            result_data.append(pb_data)
        return result_data
    else:
        error = '从理性人下载数据失败 : ' + result.json()
        print(error)
        raise Exception(error)





































