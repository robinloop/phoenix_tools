# -*- coding: UTF-8 -*-

DATE = 'date'

# 指数列表，名称与code一一对应
STOCK_NAMES = [
    "上证指数",
    "沪深300",
    "中证全指",
    "创业板指",
    "中小板指",
    "上证50",
    "中证500",
    "证券公司",
    "180金融",
    "全指医药",
    "中证军工",
    "中证环保",
    "中证银行",
    "中证传媒",
    "全指信息",
    "红利指数",
    "中证消费"
]
STOCK_CODES = [
    "1000004",
    "000300",
    "1000002",
    "399006",
    "399005",
    "000016",
    "000905",
    "399975",
    "000018",
    "000991",
    "399967",
    "000827",
    "399986",
    "399971",
    "000993",
    "000015",
    "000932"
]

# TODO: H股指数接口同A股不同，需要注意！！！！！
# H股指数
# 恒生指数 10001
# 恒生国企 10002

# 理杏仁API及TOKEN
URL_INDICE_FUNDAMENTAL = "https://open.lixinger.com/api/a/indice/fundamental"
TOKEN = "8ec3e830-0fe7-4734-844c-e23d6ea119e2"

# 百分位数计算范围（温度计算范围）
TEMPERATURE_DAY_LEN = 2434
CP = 'cp'
PB = 'pb'
PE = 'pe'

PB_PERCENTILE = 'pb_percentile'  # PB百分位数
PE_PERCENTILE = 'pe_percentile'  # PE百分位数
FIFTY_MEDIAN = 'fifty_median'  # 50日均线
HUNDRED_MEDIAN = 'hundred_median'  # 100日均线
# 50日线信号
FIFTY_SIGNAL = 'fifty_signal'
# 100日线信号
HUNDRED_SIGNAL = 'hundred_signal'

