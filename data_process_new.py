# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
from scipy import stats
import requests
import datetime
import util.constants as constants
import util.date_utils as date_utils
import util.data_process as dp

URL_INDICE_FUNDAMENTAL = "https://open.lixinger.com/api/a/indice/fundamental"
TOKEN = "8ec3e830-0fe7-4734-844c-e23d6ea119e2"

# 六种指数PBt统计
STOCK_NAMES = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE", "中证全指指数"]
stockCodes = ["1000004", "399006", "1000002", "000016", "000300", "000905", "399975"]
DAY_LEN = 2434
STOCK_NAMES_LEN = len(STOCK_NAMES)
HISTORY_FILE = 'data/temp_history.csv'


def get_result(date):
    result = {}
    # 遍历指数集合，计算每一个指数的温度及50日均线信号（指定日期50均值与收盘价比较）
    for index, stock in enumerate(constants.STOCK_CODES):
        # 读取数据目录下的指数csv文件，获取当前指数数据
        df = read_data(stock)

        # 取得指定日期行的数据
        if date is None:
            date = date_utils.csvDate2lxrDate(df[constants.DATE][0])
        # 取得指定日期之前最新一天的数据
        data_result = df.loc[df[constants.DATE].map(lambda x: date_utils.csvDate2lxrDate(x)) <= date_utils.lxrDate2csvDate(date)]
        if len(data_result.values) == 0:
            print("指定日期不存在", stock, date)
            return date, None

        # 买点1：判断50日均线突破，当天收盘价是否突破50日均线
        # 买点2：判断100日均线突破，当天收盘价是否突破100日均线
        # 卖点1，卖点2，同上述相反
        # 连续突破情况，首日突破表示买入，后续情况多仓、持仓

        # 上一交易日50日均线信号
        data_index = data_result.index.values[0]
        data = data_result.loc[data_index]
        data_before = data_result.loc[data_index + 1]

        fifty_signal = dp.check_signal(data_before, data, constants.FIFTY_MEDIAN, 1)
        hundred_signal = dp.check_signal(data_before, data, constants.HUNDRED_MEDIAN, 2)
        result_stock = {
                        'name': constants.STOCK_NAMES[index],
                        constants.DATE: data[constants.DATE],
                        constants.PB_PERCENTILE: data[constants.PB_PERCENTILE],
                        constants.PE_PERCENTILE: data[constants.PE_PERCENTILE],
                        constants.FIFTY_SIGNAL: fifty_signal,
                        constants.HUNDRED_SIGNAL: hundred_signal}
        print('指数数据:', date, result_stock)
        result[stock] = result_stock
    return date, result


def read_data(stock):
    csv_file = 'data/' + stock + '.csv'
    df = pd.read_csv(csv_file)
    # check 日期
    start_date = df[constants.DATE][0]
    start_date_fix = date_utils.csvDate2lxrDate(start_date)
    if not date_utils.check_today(start_date_fix):
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
                avg = np.average(pd.to_numeric(full_data[constants.CP][index: end]))
                fifty_days.append(avg)

                end2 = index + 100
                avg2 = np.average(pd.to_numeric(full_data[constants.CP][index: end2]))
                hundred_days.append(avg2)

                a = pd.to_numeric(full_data[constants.PB][index: constants.TEMPERATURE_DAY_LEN + index])
                p = stats.percentileofscore(a, a[index])
                pb_perentile.append(p)

                a = pd.to_numeric(full_data[constants.PE][index: constants.TEMPERATURE_DAY_LEN + index])
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


def get_new_data(stock, start_date_fix):
    new_data = pd.DataFrame()
    result_data = download_data(stock, start_date_fix)

    dates = []
    pbs = []
    pes = []
    cps = []
    for data in result_data:
        if start_date_fix == data[constants.DATE]:
            # 开始日期的数据在csv中已存在，不需要再放入新的data frame
            continue
        pes.append(data[constants.PE])
        pbs.append(data[constants.PB])
        cps.append(data[constants.CP])
        dates.append(date_utils.lxrDate2csvDate(data[constants.DATE]))

    # 将新的数据插入到data frame，然后返回
    new_data.insert(0, constants.DATE, dates)
    new_data.insert(1, constants.CP, cps)
    new_data.insert(2, constants.PB, pbs)
    new_data.insert(3, constants.PE, pes)
    return new_data


def download_data(stockCode, startDate):
    url = constants.URL_INDICE_FUNDAMENTAL
    if str(stockCode).startswith('H'):
        url = constants.URL_H_INDICE_FUNDAMENTAL
        stockCode = str(stockCode).replace('H', '')

    request_data = {
        "token": TOKEN,
        "stockCodes": [stockCode],
        "metrics": ["pb.median", "pe_ttm.median", "cp"],
        "startDate": startDate
    }
    result = requests.post(url, json=request_data)
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


# result = get_result('2019-10-08')
# print(result)
