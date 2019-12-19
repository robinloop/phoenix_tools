# -*- coding: UTF-8 -*-
import pandas as pd
import util.constants as constants
import util.date_utils as dateutils
import util.sqlite as sqlutil

# 代码
code = '1000004'
DB_PATH = '../data/test.db'
TABLE_NAME = 'STOCK_TEMPRETURE'
# 数据导入
# 取得数据库最大id
conn = sqlutil.get_conn(DB_PATH)
r = sqlutil.fetchone(conn, 'SELECT MAX(ID) FROM ' + TABLE_NAME, None)
max_id = r[0]
if max_id is None:
    max_id = 0
print('max id is ', max_id)
conn.close()

# csv_data = pd.read_csv('data/' + code + '.csv')
# data = []
# len = csv_data.index.size + max_id
# for index, row in csv_data.iterrows():
#     date = dateutils.csvDate2lxrDate(row[constants.DATE])
#     data.append((len - index, code, date, row[constants.CP], row[constants.PB], row[constants.PE]
#                  , row[constants.FIFTY_MEDIAN], row[constants.HUNDRED_MEDIAN], row[constants.PB_PERCENTILE]
#     , row[constants.PE_PERCENTILE]))
# sql = 'INSERT INTO ' + TABLE_NAME + ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
# sqlutil.save(conn, sql=sql, data=data)
