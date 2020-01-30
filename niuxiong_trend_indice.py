# -*- coding: UTF-8 -*-
import util.constants as constants
import util.sqlite as sqlite
import pandas as pd
import abs_trend_chart
import indice_niuxiong_chart


conn = sqlite.get_conn('data/' + constants.DATABASE)


def generate(stockCode, stockName):
    """
    绝对温度计算
    :param stockCode: 指数代码
    :param temp_year_cnt: 相对温度计算年数
    :param roe_year_cnt: roe计算年数
    :return:
    """
    flg = 'indice_A'
    if str(stockCode).startswith('H'):
        flg = 'indice_H'
        # stockCode = str(stockCode).replace('H', '')

    print('生成牛熊周期图开始')
    # 获取数据
    df_nx = get_niuxiong_data(stockCode)
    indice_niuxiong_chart.generate(df_nx, flg, stockCode, stockName)
    print('生成牛熊周期图结束')


def get_niuxiong_data(code):
    sql = """
        SELECT i.date, round(100/pe, 2) as shouyi, round((1/pe - g.roe * 0.01)*10000) as bp, round(g.roe, 2) * 2 as g_roe
        FROM indice_fundamental_a i  
        left join guozhai g 
        on i.date = g.date 
        where i.code =:code
        order by i.date
    """
    df = pd.read_sql(sql, conn, params={'code': code})
    return df


generate('000300', '沪深300')