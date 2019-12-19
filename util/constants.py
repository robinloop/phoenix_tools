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
    "中证消费",
    "恒生指数",
    "恒生国企"
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
    "000932",
    "H10001",
    "H10002"
]

# 理杏仁API及TOKEN
BASE_URL = 'https://open.lixinger.com'
# A股指数基本面
URL_INDICE_FUNDAMENTAL = BASE_URL + "/api/a/indice/fundamental"
# H股指数基本面
URL_H_INDICE_FUNDAMENTAL = BASE_URL + "/api/h/indice/fundamental"
# A股个股
URL_A = BASE_URL + "/api/a/stock"
URL_A_FUNDAMENTAL = BASE_URL + "/api/a/stock/fundamental"

# H股个股
URL_H = BASE_URL + "/api/h/stock"
URL_H_FUNDAMENTAL = BASE_URL + "/api/h/stock/fundamental"

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
# 100日线信号HUNDRED_SIGNAL = 'hundred_signal'

# 数据起始日期，获取2002年以后的数据
START_DATE = '2002-01-04'

# 数据库表名
# A股指数
TABLE_INDICE_FUNDAMENTAL_A = 'indice_fundamental_a'
# A股个股
TABLE_STOCK_A = 'stock_a'
# 数据库地址
DATABASE = 'phoenix.db'
# 绝对温度参数
# 计算相对温度时的数据数量（默认9年）
RELATIVE_TEMP_YEAR = 9
# 每年的股票交易日
STOCK_EXCHANGE_DAY_OF_YEAR = 250


