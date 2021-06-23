# -*- coding: UTF-8 -*-

import abs_code_const as const
import abs_temp_indice as indice
import abs_temp_stock as stock
import guozhai_data

# 首先更新10年国债收益数据
guozhai_data.generate()


# 第一个参数是指数代码，
# 第二个参数代表指数名称
# 第三个参数9代表温度计算时间段9年，
# 第四个参数5代表收益率T年（计算V_PB）

indice.generate('000300', '沪深300', 5, 5)
#indice.generate('000688', '科创50', 5, 5)
indice.generate('399975', '证券公司', 5, 5)
#stock.generate('600019', '宝钢股份',5,5)
#stock.generate('000825', '太钢不锈',5,5)
#stock.generate('601186', '中国铁建',5,5)
#stock.generate('H03898', '中车时代电气',5,5)
#stock.generate('H00005', '汇丰控股',5,5)
#indice.generate('HSI', '恒生指数', 5, 5)
#indice.generate('HSCEI', '国企指数', 9, 5)

indice.generate_list(const.INDICE_LIST, 5, 5, '宽基指数合并输出', const.IS_GEN_SINGLE)
indice.generate_list(const.INDICE_INDUSTRY_LIST, 5, 5, '行业指数合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.HOLD_STOCK_LIST, 5, 5, '持仓合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.LEADING_STOCK_LIST, 5, 5, '龙头企业合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.GZDMBK_STOCK_LIST, 5, 5, '跟踪待买合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.CHECK_STOCK_LIST, 5, 5, '观察个股合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.JJBK_STOCK_LIST, 5, 5, '基建板块合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.QNBK_STOCK_LIST, 5, 5, '氢能板块合并输出', const.IS_GEN_SINGLE)

stock.generate_list(const.ZJBK_STOCK_LIST, 5, 5, '猪鸡板块合并输出', const.IS_GEN_SINGLE)


