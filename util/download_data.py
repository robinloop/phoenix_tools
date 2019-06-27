# -*- coding: UTF-8 -*-

import util.constants as constants
import util.date_utils as dateutils
import pandas as pd
import requests
import numpy as np
from scipy import stats

# 测试代码
DEFAULT_CSV = 'data/temp_pb.csv'


def download(stock):
    # 获取中证全指收盘点位
    request_data = {
        "token": constants.TOKEN,
        "stockCodes": [stock],
        "metrics": ["pb.median", "pe_ttm.median", "cp"],
        "startDate": "1996-01-01"
    }
    result = requests.post(constants.URL_INDICE_FUNDAMENTAL, json=request_data)
    pbs = []
    pes = []
    cps = []
    date = []
    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            split_date = data['date'].split('T')
            date.append(dateutils.lxrDate2csvDate(split_date[0]))
            cp = ''
            if 'cp' in data.keys():
                cp = data['cp']
            cps.append(cp)
            pbs.append(data['pb']['median'])
            pes.append(data['pe_ttm']['median'])

    df = pd.DataFrame()
    df.insert(0, constants.DATE, date)
    df.insert(1, constants.CP, cps)
    df.insert(2, constants.PB, pbs)
    df.insert(3, constants.PE, pes)
    df.to_csv('../data/back/' + stock + '.csv', index=False, encoding='utf-8', decimal='.')


def data_process(stock):
    csv = pd.read_csv('../data/back/' + stock + '.csv')
    print(stock, csv[constants.DATE][0])

    fifty_days = []
    hundred_days = []
    pb_perentile = []
    pe_perentile = []
    data_len = len(csv[constants.CP])
    # 处理50日均线
    for index in range(data_len):
        end = index + 50
        avg = np.average(csv[constants.CP][index: end])
        fifty_days.append(avg)

        end2 = index + 100
        avg2 = np.average(csv[constants.CP][index: end2])
        hundred_days.append(avg2)

        a = csv[constants.PB][index: constants.TEMPERATURE_DAY_LEN + index]
        p = stats.percentileofscore(a, a[index])
        pb_perentile.append(p)

        a = csv[constants.PE][index: constants.TEMPERATURE_DAY_LEN + index]
        p = stats.percentileofscore(a, a[index])
        pe_perentile.append(p)

    csv.insert(4, constants.PB_PERCENTILE, pb_perentile)
    csv.insert(5, constants.PE_PERCENTILE, pe_perentile)
    csv.insert(6, constants.FIFTY_MEDIAN, fifty_days)
    csv.insert(7, constants.HUNDRED_MEDIAN, hundred_days)
    csv.to_csv('../data/' + stock + '.csv', index=False)


for stockCode in constants.STOCK_CODES:
    # 下载数据
    # download(stockCode)
    # 计算数据pb、pe百分位数，50、100日均线数据
    data_process(stockCode)
# data_process("1000004")
