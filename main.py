# -*- coding: UTF-8 -*-
import data_process as dp
import temperature_generator as tg
import sys

DEFAULT_CSV = 'data/temp_pb.csv'
DEFAULT_HTML_TEMPERATURE = 'output/temperature.html'

if __name__ == '__main__':
    args = sys.argv[1:]

    print('数据分析中，请稍后......')
    date, data = dp.get_percentile_data(DEFAULT_CSV)

    input_date = None
    if len(args) > 0:
        input_date = args[0]
    else:
        input_date = date
        print('没有输入日期, 使用指数最新日期:', date)

    print('指数最新日期', date)
    print('指数温度信息', data)
    print('数据获取完毕，开始生成chart...')
    tg.generate(input_date, data, DEFAULT_HTML_TEMPERATURE)
    print('chart生成完毕,请查看:', DEFAULT_HTML_TEMPERATURE)
    sys.exit(0)
