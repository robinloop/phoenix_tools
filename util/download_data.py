# -*- coding: UTF-8 -*-

import util.constants as constants
import util.date_utils as dateutils
import pandas as pd
import requests

# 测试代码
DEFAULT_CSV = 'data/temp_pb.csv'


def test(stock):
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
    df.insert(0, "日期", date)
    df.insert(1, "cp", cps)
    df.insert(2, "pb", pbs)
    df.insert(3, "pe", pes)
    df.to_csv('../data/' + stock + '.csv', index=False, encoding='utf-8', decimal='.')


for stockCode in constants.STOCK_CODES:
    test(stockCode)
