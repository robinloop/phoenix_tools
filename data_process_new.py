# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
from scipy import stats
import requests
import datetime
import util.constants as constants
import util.date_utils as date_utils

URL_INDICE_FUNDAMENTAL = "https://open.lixinger.com/api/a/indice/fundamental"
TOKEN = "8ec3e830-0fe7-4734-844c-e23d6ea119e2"

# 六种指数PBt统计
STOCK_NAMES = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE", "中证全指指数"]
stockCodes = ["1000004", "399006", "1000002", "000016", "000300", "000905", "399975"]
DAY_LEN = 2434
STOCK_NAMES_LEN = len(STOCK_NAMES)
HISTORY_FILE = 'data/temp_history.csv'


def get_percentile_data(date):
    result = {}
    # 遍历指数集合，计算每一个指数的温度及50日均线信号（指定日期50均值与收盘价比较）
    for index, stock in enumerate(constants.STOCK_CODES):
        # 读取数据目录下的指数csv文件，获取当前指数数据
        df = read_data(stock)

        # 取得指定日期行的数据
        if date is None:
            date = csvDate2lxrDate(df[constants.DATE][0])
        data = df.loc[df[constants.DATE] == date_utils.lxrDate2csvDate(date)]
        if len(data.values) == 0:
            print("指定日期不存在", date)
            pass

        # 买点1：判断50日均线突破，当天收盘价是否突破50日均线
        # 买点2：判断100日均线突破，当天收盘价是否突破100日均线
        # 卖点1，卖点2，同上述相反
        # 连续突破情况，首日突破表示买入，后续情况多仓、持仓

        # 上一交易日50日均线信号
        data_index = data.index.values[0]
        data = df.loc[data_index]
        data_before = df.loc[data_index + 1]

        fifty_signal = check_signal(data_before, data, constants.FIFTY_MEDIAN)
        hundred_signal = check_signal(data_before, data, constants.HUNDRED_MEDIAN)
        result_stock = {constants.PB_PERCENTILE: data[constants.PB_PERCENTILE],
                        constants.PE_PERCENTILE: data[constants.PE_PERCENTILE],
                        constants.FIFTY_SIGNAL: fifty_signal,
                        constants.HUNDRED_SIGNAL: hundred_signal}
        result[stock] = result_stock
    print(result)


def check_signal(data_before, data, median_type):
    data_before_median_diff = data_before[constants.CP] - data_before[median_type]
    median_diff = data[constants.CP] - data[median_type]
    # 判断当天收盘价是否突破均线
    # 连续突破情况，首日突破表示买入
    # 买入信号，0位持平，1位买入，-1卖出
    signal = 0
    if median_diff > 0 and data_before_median_diff<=0:
        signal = 1
    elif median_diff < 0 and data_before_median_diff >= 0:
        signal = -1
    return signal


def read_data(stock):
    csv_file = 'data/' + stock + '.csv'
    df = pd.read_csv(csv_file)
    # check 日期
    start_date = df[constants.DATE][0]
    start_date_fix = csvDate2lxrDate(start_date)
    if not check_today(start_date_fix):
        # CSV文件数据不是最新的，先进行下载
        # 下载数据，csv文件数据补齐到最近一个交易日
        new_data = get_new_data(stock, start_date_fix)
        # 如果获取到新的数据，则加入到df中并计算均线及百分位数
        if new_data.index.values.size > 0:
            full_data = new_data.append(df, ignore_index=True, sort=True)
            # 计算新数据的百分位及均值
            fifty_days = []
            hundred_days = []
            pb_perentile = []
            pe_perentile = []

            for index in range(new_data.index.values.size):
                end = index + 50
                avg = np.average(full_data[constants.CP][index: end])
                fifty_days.append(avg)

                end2 = index + 100
                avg2 = np.average(full_data[constants.CP][index: end2])
                hundred_days.append(avg2)

                a = full_data[constants.PB][index: constants.TEMPERATURE_DAY_LEN + index]
                p = stats.percentileofscore(a, a[index])
                pb_perentile.append(p)

                a = full_data[constants.PE][index: constants.TEMPERATURE_DAY_LEN + index]
                p = stats.percentileofscore(a, a[index])
                pe_perentile.append(p)
            # 保存数据
            new_data.insert(4, 'pb_percentile', pb_perentile)
            new_data.insert(5, 'pe_percentile', pe_perentile)
            new_data.insert(6, 'fifty_median', fifty_days)
            new_data.insert(7, 'hundred_median', hundred_days)

            result_data = new_data.append(df, ignore_index=True, sort=True)
            result_data.to_csv(csv_file, index=False, encoding='utf-8', decimal='.')
            return result_data
    return df


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


def get_new_data(stock, start_date_fix):
    new_data = pd.DataFrame()
    result_data = download_data(stock, start_date_fix)

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

    # 将新的数据插入到dataframe，然后返回
    new_data.insert(0, "日期", dates)
    new_data.insert(1, "cp", cps)
    new_data.insert(2, "pb", pbs)
    new_data.insert(3, "pe", pes)
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



get_percentile_data('2019-06-06')