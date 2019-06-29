# -*- coding: UTF-8 -*-
from pyecharts import Page

import six_gauge
import wendu_shidu
import nine_gauge


def generate(date, data, file, show_temp):
    """
    生成温度HTML页面
    :param date: 显示日期
    :param data: 温度数据
    :param file: HTML文件路径
    :return:
    """
    page = Page()
    gauge = six_gauge.generate_chart(date, data, show_temp)
    page.add(gauge)
    gauge = wendu_shidu.generate_chart(date, data[-2:], show_temp)
    page.add(gauge)
    page.render(path=file)


def generate_signal(date, data, file, show_temp):
    """
    生成温度HTML页面
    :param date: 显示日期
    :param data: 温度数据
    :param file: HTML文件路径
    :return:
    """
    page = Page()
    # 宽基指数
    stock_temp = [
        ("1000004", "上证指数"),
        ("000300", "沪深300"),
        ("H10001", "恒生指数"),
        ("1000002", "中证全指"),
        ("399006", "创业板指"),
        ("399005", "中小板指"),
        ("H10002", " 恒生国企"),
        ("000016", "上证50"),
        ("000905", "中证500"),
    ]
    gauge = nine_gauge.generate_chart(stock_temp, date, data, show_temp)
    page.add(gauge)
    # 行业指数
    stock_temp = [
        ("000932", "中证消费"),
        ("000018", "180金融"),
        ("000991", "全指医药"),
        ("399967", "中证军工"),
        ("000827", "中证环保"),
        ("399986", "中证银行"),
        ("399971", "中证传媒"),
        ("000993", "全指信息"),
        ("000015", "红利指数")
    ]
    gauge = nine_gauge.generate_chart(stock_temp, date, data, show_temp)
    page.add(gauge)

    gauge = wendu_shidu.generate_chart(date, data, show_temp)
    page.add(gauge)
    page.render(path=file)

