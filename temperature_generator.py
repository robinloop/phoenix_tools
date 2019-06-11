# -*- coding: UTF-8 -*-
from pyecharts import Page
from pyecharts.engine import create_default_environment

import six_gauge
import wendu_shidu


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

