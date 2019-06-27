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


def check_today(start_date):
    """
    判断csv文件的最新日期是否是今天
    :param start_date:
    :return:
    """
    d = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.datetime.now()
    dd = d2 - d
    if dd.days == 0:
        return True
    return False
