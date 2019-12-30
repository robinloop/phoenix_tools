# -*- coding: UTF-8 -*-

import requests
import pandas as pd
import util.sqlite as sqlite
import util.constants as constants
import util.date_utils as date_utils


table_name = 'guozhai'


def get_guozhai_data(conn, date):
    """
    获取10年国债收益率（从中国债券信息网获取）
    :param date:
    :return:
    """
    # params = {
    #     'xyzSelect': 'txy',
    #     'workTimes': date,
    #     'dxbj': 0,
    #     'qxll': 0,
    #     'yqqxN': 'N',
    #     'yqqxK': 'K',
    #     'ycDefIds': '2c9081e50a2f9606010a3068cae70001,',
    #     'wrjxCBFlag': 0,
    #     'locale': 'zh_CN'
    # }
    url = 'http://yield.chinabond.com.cn/cbweb-mn/yc/searchYc' \
          '?xyzSelect=txy' \
          '&&dxbj=0' \
          '&&qxll=0,' \
          '&&yqqxN=N' \
          '&&yqqxK=K' \
          '&&ycDefIds=2c9081e50a2f9606010a3068cae70001,' \
          '&&wrjxCBFlag=0' \
          '&&locale=zh_CN' \
          '&&workTimes=' + date

    result = requests.post(url)
    if result.status_code == 200:
        if result.text is '':
            print('This date has no data, please check date!',  date)
        else:
            r = result.json()[0]
            for data in r['seriesData']:
                if data[0] == 10:
                    # 获取十年收益率，将数据插入到数据库中
                    save_to_db(conn, date, data[1])
                    break
    else:
        print('获取十年国债收益率失败，')


def save_to_db(conn, date, value):
    sql = 'INSERT INTO ' + table_name + ' (date, roe) VALUES (?, ?)'
    print(sql, date, value)
    result_data = [(date, value)]
    sqlite.save(conn, sql=sql, data=result_data)


conn = sqlite.get_conn('data/' + constants.DATABASE)

df = pd.read_csv('data/guozhai.csv')
df.to_sql(table_name, con=conn, if_exists='replace', index=False)

sql = 'SELECT MAX(DATE) FROM ' + table_name + ' ORDER BY DATE DESC'
max_date = sqlite.fetchone(conn, sql)[0]
print('指数基本面最新日期:', max_date)

# sql = 'SELECT date FROM indice_fundamental_a ' \
#       'where code = 399975 and date > (select max(date) from guozhai) ' \
#       'order by date desc'
# results = sqlite.fetchall(conn, sql)
# print(results)
# 跟随股票。股票有新日期则获取新日期的国债收益数据
# for result in results:
date = max_date
if date_utils.check_today(date):
    print('已经是最新数据，不需要处理')
else:
    while True:
        date = date_utils.tomorrow(date)
        print('获取国债收益数据, 日期：', date)
        get_guozhai_data(conn, date)
        if date_utils.check_today(date):
            break

sql = 'select * from guozhai order by date desc'
df = pd.read_sql_query(sql, conn)
df.to_csv('data/guozhai.csv', index=False, encoding='utf-8', decimal='.')
