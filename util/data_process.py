# -*- coding: UTF-8 -*-

import util.constants as constants
import util.date_utils as dateutils
import pandas as pd
import requests
import numpy as np
from scipy import stats


def data_download(stock, url):
    # 请求数据
    request_data = {
        "token": constants.TOKEN,
        "stockCodes": [stock],
        "metrics": ["pb.median", "pe_ttm.median", "cp"],
        "startDate": "2000-01-01"
    }
    result = requests.post(url, json=request_data)
    pbs = []
    pes = []
    cps = []
    date = []
    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            if 'cp' in data.keys():
                cp = data['cp']
                cps.append(cp)
            else:
                continue

            split_date = data['date'].split('T')
            date.append(dateutils.lxrDate2csvDate(split_date[0]))

            pb = ''
            if 'pb' in data.keys() and 'median' in data['pb'].keys():
                pb = data['pb']['median']
            pbs.append(pb)

            pe = ''
            if 'pe_ttm' in data.keys() and 'median' in data['pe_ttm'].keys():
                pe = data['pe_ttm']['median']
            pes.append(pe)
    df = pd.DataFrame()
    df.insert(0, constants.DATE, date)
    df.insert(1, constants.CP, cps)
    df.insert(2, constants.PB, pbs)
    df.insert(3, constants.PE, pes)
    return df


def data_download_stock(stock, url):
    # 请求数据
    request_data = {
        "token": constants.TOKEN,
        "stockCodes": [stock],
        "metrics": ["pb", "pe_ttm", "sp"],
        "startDate": "2000-01-01"
    }
    result = requests.post(url, json=request_data)
    pbs = []
    pes = []
    cps = []
    date = []
    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            if 'sp' in data.keys():
                cp = data['sp']
                cps.append(cp)
            else:
                continue

            split_date = data['date'].split('T')
            date.append(dateutils.lxrDate2csvDate(split_date[0]))

            pb = ''
            if 'pb' in data.keys():
                pb = data['pb']
            pbs.append(pb)

            pe = ''
            if 'pe_ttm' in data.keys():
                pe = data['pe_ttm']
            pes.append(pe)
    df = pd.DataFrame()
    df.insert(0, constants.DATE, date)
    df.insert(1, constants.CP, cps)
    df.insert(2, constants.PB, pbs)
    df.insert(3, constants.PE, pes)
    return df


def data_calc(data):
    fifty_days = []
    hundred_days = []
    pb_perentile = []
    pe_perentile = []
    data_len = len(data[constants.CP])
    # 处理50日均线
    for index in range(data_len):
        end = index + 50
        avg = np.average(data[constants.CP][index: end])
        fifty_days.append(avg)

        end2 = index + 100
        avg2 = np.average(data[constants.CP][index: end2])
        hundred_days.append(avg2)

        a = data[constants.PB][index: constants.TEMPERATURE_DAY_LEN + index]
        if a[index] == '':
            p = ''
        else:
            p = stats.percentileofscore(a, a[index])
        pb_perentile.append(p)

        a = data[constants.PE][index: constants.TEMPERATURE_DAY_LEN + index]
        if a[index] == '':
            p = ''
        else:
            p = stats.percentileofscore(a, a[index])
        pe_perentile.append(p)
    data.insert(4, constants.PB_PERCENTILE, pb_perentile)
    data.insert(5, constants.PE_PERCENTILE, pe_perentile)
    data.insert(6, constants.FIFTY_MEDIAN, fifty_days)
    data.insert(7, constants.HUNDRED_MEDIAN, hundred_days)


def check_signal(data_before, data, median_type, number):
    data_before_median_diff = data_before[constants.CP] - data_before[median_type]
    median_diff = data[constants.CP] - data[median_type]
    # 判断当天收盘价是否突破均线
    # 连续突破情况，首日突破表示买入
    # 买入信号，0位持平，1位买入，-1卖出
    signal = '--'
    if median_diff > 0:
        signal = '+'
        if data_before_median_diff <= 0:
            signal = 'B' + str(number)
    elif median_diff < 0:
        signal = '-'
        if data_before_median_diff >= 0:
            signal = 'S' + str(number)
    return signal


def data_down2file(stock):
    # 默认使用A股指数接口，H股指数使用不同接口
    url = constants.URL_INDICE_FUNDAMENTAL
    stock_code = stock
    if str(stock).startswith('H'):
        url = constants.URL_H_INDICE_FUNDAMENTAL
        stock_code = str(stock).replace('H', '')

    df = data_download(stock_code, url)
    df.to_csv('../data/back/' + stock + '.csv', index=False, encoding='utf-8', decimal='.')


def data_process(stock):
    csv = pd.read_csv('../data/back/' + stock + '.csv')
    print(stock, csv[constants.DATE][0])

    data_calc(csv)
    csv.to_csv('../data/' + stock + '.csv', index=False)

# for stockCode in constants.STOCK_CODES:
#     # 下载数据
#     # download(stockCode)
#     # 计算数据pb、pe百分位数，50、100日均线数据
#     data_process(stockCode)
# download("H10001")
# data_process("H10001")
