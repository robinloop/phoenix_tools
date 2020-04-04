# -*- coding: UTF-8 -*-

import abs_code_const as const
import abs_temp_indice as indice
import abs_temp_stock as stock
import guozhai_data

# 首先更新10年国债收益数据
guozhai_data.generate()

# 指数
# 第一个参数是指数代码，
# 第二个参数代表指数名称
# 第三个参数9代表温度计算时间段9年，
# 第四个参数5代表收益率T年（计算S）

# indice.generate('HSI', '恒生指数', 5, 5)
# indice.generate('000300', '沪深300', 5, 5)

# 股票
# indice.generate('HSCEI', '国企指数', 9, 5)
# 是否生成每一个指数的html，默认生成

# indice.generate_list(const.INDICE_LIST, 5, 5, '指数合并输出', const.IS_GEN_SINGLE)

# stock.generate_list(const.HOLD_STOCK_LIST, 5, 5, '持仓合并输出', const.IS_GEN_SINGLE)

CHECK_STOCK_LIST = [
    ('600019', 'xxxx'),
    ]
stock.generate_list(CHECK_STOCK_LIST, 5, 5, '观察个股合并输出', const.IS_GEN_SINGLE)

# stock.generate_list(const.JJBK_STOCK_LIST, 5, 5, '基建板块合并输出', const.IS_GEN_SINGLE)

