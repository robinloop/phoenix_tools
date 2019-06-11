# -*- coding: UTF-8 -*-
import data_process as dp
import temperature_generator as tg
import sys
import getopt
import temp_history, wendu_trend_chart

DEFAULT_CSV = 'data/temp_pb.csv'
DEFAULT_HTML_TEMPERATURE = 'output/temperature.html'
DEFAULT_TREND_TEMPERATURE = 'output/temp_line.html'

if __name__ == '__main__':
    # args = sys.argv[1:]
    opts, args = getopt.getopt(sys.argv[1:], "th:s", ["trend", ])

    input_date = None
    print('处理开始，请稍后......')
    # 返回的参数opts是对应的选项和参数，args暂时不用管
    is_history = False
    show_temp = False

    if len(opts) > 0:
        for op, value in opts:
            if op == '-h':
                is_history = True
                input_date = value
            elif op == '-s':
                show_temp = True

    print(input_date)
    if is_history:
        print('获取历史数据，请稍后......')
        data = temp_history.get_history_data(input_date)
        if data is None or len(data) == 0:
            print("没有获取到指定日期的指数温度，请输入正确的日期")
        else:
            tg.generate(input_date, [round(i, 1) for i in data[1:9]], DEFAULT_HTML_TEMPERATURE, show_temp)
            print('chart生成完毕,请查看:', DEFAULT_HTML_TEMPERATURE)
    else:
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
        tg.generate(input_date, data, DEFAULT_HTML_TEMPERATURE, show_temp)
        print('chart生成完毕,请查看:', DEFAULT_HTML_TEMPERATURE)

        print('生成历史温度趋势，请稍后......')
        wendu_trend_chart.generate()
        print('chart生成完毕,请查看:', DEFAULT_TREND_TEMPERATURE)
    sys.exit(0)
