# -*- coding: UTF-8 -*-

import datetime


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
    if len(date_arr) != 3:
        raise Exception("日期格式不正确，请输入正确的日期格式，例如：2019-02-24")
    year = date_arr[0]
    month = str(int(date_arr[1]))
    day = str(int(date_arr[2]))
    return '/'.join([year, month, day])


def check_today(date):
    """
    判断csv文件的最新日期是否是今天
    :param date:
    :return:
    """
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    d2 = datetime.datetime.now()
    dd = d2 - d
    if dd.days == 0:
        return True
    return False


def tomorrow(date):
    """
    取得指定日期第二天的日期
    :param date:
    :return:
    """
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    d1 = d + datetime.timedelta(days=1)
    return d1.strftime('%Y-%m-%d')


def years_ago(date, n):
    """
    获取指定日期的n年前日期
    :param date:
    :param n:
    :return:
    """
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    # year = d.year - n
    # month = d.month
    # day = d.day
    # d1 = datetime.date(year, month, day)
    d1 = d + datetime.timedelta(days=-365 * n)
    return d1.strftime('%Y-%m-%d')
