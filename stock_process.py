# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import util.constants as constants
import requests
import util.date_utils as date_utils
import util.data_process as dp
import chart.guage as guage
from pyecharts import Page


def generate(stock, input_date, show_signal):
    stock_name, df = download(stock)
    if stock_name is None or df is None:
        print("没有获取到数据，请确认代码输入是否正确")
        return

    print('生成股票温度图：', stock_name)
    date = input_date
    # 取得指定日期行的数据
    if date is None:
        date = date_utils.csvDate2lxrDate(df[constants.DATE][0])
    data = df.loc[df[constants.DATE] == date_utils.lxrDate2csvDate(date)]
    if len(data.values) == 0:
        print("指定日期不存在", stock, date)
        return

    # 买点1：判断50日均线突破，当天收盘价是否突破50日均线
    # 买点2：判断100日均线突破，当天收盘价是否突破100日均线
    # 卖点1，卖点2，同上述相反
    # 连续突破情况，首日突破表示买入，后续情况多仓、持仓

    # 上一交易日50日均线信号
    data_index = data.index.values[0]
    data = df.loc[data_index]
    data_before = df.loc[data_index + 1]

    fifty_signal = dp.check_signal(data_before, data, constants.FIFTY_MEDIAN, 1)
    hundred_signal = dp.check_signal(data_before, data, constants.HUNDRED_MEDIAN, 2)
    result_stock = {constants.PB_PERCENTILE: data[constants.PB_PERCENTILE],
                    constants.PE_PERCENTILE: data[constants.PE_PERCENTILE],
                    constants.FIFTY_SIGNAL: fifty_signal,
                    constants.HUNDRED_SIGNAL: hundred_signal}

    generate_chart(stock, stock_name, date, result_stock, show_signal)


def generate_chart(stock, name, date, result_stock, show_signal):
    value = round(result_stock[constants.PB_PERCENTILE], 1)

    if show_signal:
        name = name + '\n ' + result_stock[constants.FIFTY_SIGNAL] + ' ' + result_stock[constants.HUNDRED_SIGNAL]

    chart = guage.generate_chart(date, value, name, show_signal)
    page = Page()
    page.add(chart)
    file = 'output/temperature_' + str(stock) + '.html'
    page.render(path=file)
    print("查看股票温度图：", file)


def download(stock):
    # 首先判断股票代码是否存在
    stock_code, url_info, url_fun = get_url(stock)

    # 获取股票信息
    request_data = {
        "token": constants.TOKEN,
        "stockCodes": [stock_code]
    }

    stock_name = None
    result = requests.post(url_info, json=request_data)
    if result.status_code == 200 and result.json()['msg'] == 'success':
        for data in result.json()['data']:
            if 'name' in data.keys():
                stock_name = data['name']
                # 请求数据
                df = dp.data_download_stock(stock_code, url_fun)
                dp.data_calc(df)
                return stock_name, df
    return stock_name, None


def get_url(stock):
    url_info = constants.URL_A
    url_fun = constants.URL_A_FUNDAMENTAL
    stock_code = stock
    if str(stock).startswith('H'):
        url_info = constants.URL_H
        url_fun = constants.URL_H_FUNDAMENTAL
        stock_code = str(stock).replace('H', '')
    return stock_code, url_info, url_fun

# generate('000001', None, True)
