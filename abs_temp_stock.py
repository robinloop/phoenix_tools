# -*- coding: UTF-8 -*-
# 指数处理
# 绝对温度计算及chart生成
# 首先下载数据，然后按天计算相对温度、绝对温度
import requests
import util.constants as constants
import util.sqlite as sqlite
import util.date_utils as dateutil
import pandas as pd
from scipy import stats
import numpy as np
import abs_trend_chart


conn = sqlite.get_conn('data/' + constants.DATABASE)


def generate(stockCode, stockName, temp_year_cnt, roe_year_cnt):
    """
    绝对温度计算
    :param stockCode: 指数代码
    :param temp_year_cnt: 相对温度计算年数
    :param roe_year_cnt: roe计算年数
    :return:
    """
    print('计算绝对温度开始', stockCode)

    table_name = constants.TABLE_STOCK_A
    url = constants.URL_A_FUNDAMENTAL
    flg = 'stock_A'
    if str(stockCode).startswith('H'):
        table_name = constants.TABLE_STOCK_H
        url = constants.URL_H_FUNDAMENTAL
        stockCode = str(stockCode).replace('H', '')
        flg = 'stock_H'

    # 如果表不存在先建表
    create_table(table_name)
    # 取得指数基本面数据
    download_indice_fundamental_data(url, table_name, stockCode)
    # 获取国债收益率
    # TODO
    df_gz = pd.read_csv('data/guozhai.csv')
    # 计算相对温度
    df = calc_relative_tempreture(table_name, stockCode, df_gz, temp_year_cnt, roe_year_cnt)
    # 计算绝对温度
    calc_absolute_tempreture(table_name, df, df_gz, stockCode, temp_year_cnt)
    print('计算绝对温度结束', stockCode)

    abs_trend_chart.generate(df, flg, stockCode, stockName)
    print('生成图')


def create_table(table_name):
    sql_start = 'CREATE TABLE IF NOT EXISTS ' + table_name
    sql_schema = """
         (
           code           TEXT    NOT NULL,
           date           TEXT     NOT NULL,
           cp       REAL,
           pb       REAL, 
           pe       REAL,
           primary key (code, date));
    """
    sql = sql_start + sql_schema
    sqlite.create_table(conn, sql)


def calc_absolute_tempreture(table_name, df, df_gz, stockCode, temp_year_cnt):
    # 查询数据中没有计算相对温度的最大日期
    print('计算绝对温度开始', stockCode)
    absolute_temp = []
    for index in range(df.index.values.size):
        # 相对温度计算
        p = calc_relative_temp(df, index, temp_year_cnt, 'pba')
        absolute_temp.append(p)

    df['absolute_temp'] = absolute_temp
    print('计算绝对温度结束', stockCode)
    df.to_sql(table_name + '_' + stockCode, con=conn, if_exists='replace', index=False)

    # 输出到csv
    csv = 'data/' + table_name + '_' + stockCode + '.csv'
    df.to_csv(csv, index=False, encoding='utf-8', decimal='.')
    print('数据输出到csv文件：',  csv)
    return df


def calc_relative_tempreture(table_name, stockCode, df_gz, temp_year_cnt, roe_year_cnt):
    # 查询数据中没有计算相对温度的最大日期
    print('计算相对温度开始', stockCode)
    sql = 'SELECT date, cp, pb, pe, 1/pb, pb/pe as roe FROM ' + table_name + ' WHERE code = ? order by date'
    # result = sqlite.fetchall(conn, sql, stockCode)
    # df = pd.DataFrame(result, columns=['date', 'cp', 'pb', 'pe', '1/pb', 'roe'])
    df = pd.read_sql_query(sql, conn, params=(stockCode,))
    relative_temp = []
    pba = []
    sa = []
    for index in range(df.index.values.size):
        # 相对温度计算
        p = calc_relative_temp(df, index, temp_year_cnt, '1/pb')
        relative_temp.append(p)
        # 计算roe: S=[(1+ROE)^t-1]/[(1+r)^t-1]
        roe = df['roe'][index]
        pb = df['pb'][index]
        # 获取国债收益率
        df_gz_split = df_gz[df_gz['date'] <= df['date'][index]]
        r = df_gz_split['roe'][df_gz_split.index.values[0]]
        r = r/100
        r1 = np.power(roe + 1, roe_year_cnt) - 1
        r2 = np.power(r + 1, roe_year_cnt) - 1
        s = r1/r2
        sa.append(s)
        # a = abs(s) / (pb - s)
        a = s/pb
        pba.append(a)

    df['relative_temp'] = relative_temp
    df['pba'] = pba
    df['s'] = sa
    print('计算相对温度结束', stockCode)
    df.to_sql(table_name + '_' + stockCode, con=conn, if_exists='replace', index=False)
    return df


def calc_relative_temp(df, index, temp_year_cnt, column):
    date = df['date'][index]
    start_date = dateutil.years_ago(date, temp_year_cnt)
    df_split = df[df['date'] >= start_date]
    df_split = df_split[df_split['date'] <= date]

    # print('日期区间', temp_year_cnt, start_date, date, df_split.size/6)
    a = pd.to_numeric(df_split[column])
    #     # 计算1/pb的百分位
    # 计算100 - (1/pb的百分位)
    p = 100 - stats.percentileofscore(a, a[index])
    p = round(p, ndigits=2)
    return p


def download_indice_fundamental_data(url, table_name, stockCode):
    sql = 'SELECT MAX(DATE) FROM ' + table_name + ' WHERE code = ?'
    max_date = sqlite.fetchone(conn, sql, stockCode)[0]
    print('指数基本面最新日期:', max_date)

    if max_date is None:
        print('已有数据中无该指数数据，下载2000年以后所有数据')
        max_date = constants.START_DATE
    elif dateutil.check_today(max_date):
        # 判断数据是否已是最新，如果是则不需要下载
        print('指数基本面数据已是最新，不需下载')
        return
    else:
        # 如果不是，则下载start_date+1天之后的数据
        max_date = dateutil.tomorrow(max_date)

    print('指数基本面数据下载开始', stockCode)
    request_data = {
        "token": constants.TOKEN,
        "stockCodes": [stockCode],
        "metrics": ["pb", "pe_ttm", "sp"],
        "startDate": max_date
    }
    result = requests.post(url, json=request_data)
    result_data = []

    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            split_date = data['date'].split('T')
            result_data.append(
                (stockCode,
                 split_date[0],
                 data['sp'],
                 data['pb'],
                 data['pe_ttm'])
            )
        sql = 'INSERT INTO ' + table_name + ' (code, date, cp, pb, pe) VALUES (?, ?, ?, ?, ?)'
        sqlite.save(conn, sql=sql, data=result_data)
    else:
        error = '从理性人下载数据失败 : '
        print(error)
        print('result ', result)
        raise Exception(error)
    print('指数基本面数据下载结束', stockCode)


# 只支持A股指数，
# 第一个参数是指数代码，
# 第二个参数代表指数名称
# 第三个参数9代表温度计算时间段9年，
# 第四个参数5代表收益率T年（计算S）
generate('H00700', '港股', 9, 5)
generate('600674', '川投能源', 9, 5)
