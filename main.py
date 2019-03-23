# -*- coding: UTF-8 -*-
import data_process as dp
import six_gauge
import sys

DEFAULT_CSV = 'data/temp_pb.csv'
DEFAULT_HTML_SIX_GAUGE = 'output/wendu6.html'

if __name__ == '__main__':
    args = sys.argv[1:]

    print('数据分析中，请稍后......')
    if len(args) == 0:
        args.append(DEFAULT_CSV)
    if len(args) > 0:
        print('没有输入csv文件, 使用文件: ', DEFAULT_CSV)
        date, data = dp.get_percentile_data(args[0])
        print(date, data)
        print('数据获取完毕，开始生成chart...')
        six_gauge.generate_chart(date, data, DEFAULT_HTML_SIX_GAUGE)
        print('chart生成完毕,请查看:', DEFAULT_HTML_SIX_GAUGE)
    sys.exit(0)
