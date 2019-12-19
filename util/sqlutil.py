# -*- coding: UTF-8 -*-

import util.sqlite as sqlite
import util.constants as constants


def get_connect():
    conn = sqlite.get_conn(constants.DATABASE_PATH)
    print(conn)
    return conn


def save(table_name, data):
    """
    批量插入数据
    :param table_name:
    :param data:
    :return:
    """
    conn = get_connect()
    sql = 'INSERT INTO ' + table_name + ' VALUES (?, ?, ?, ?)'
    sqlite.save(conn, sql=sql, data=data)


def get_max_date(table_name, code):
    """
    获取指数或个股在数据库中的最大日期，如果数据库中不存在则取默认起始日期
    :param table_name:表名
    :param code: 代码
    :return:最大日期
    """
    conn = get_connect()
    r = sqlite.fetchone(conn, 'SELECT MAX(DATE) FROM ' + table_name + ' WHERE code = ?', data=code)
    max_date = r[0][0]
    if max_date is None:
        max_date = constants.START_DATE
    return max_date

