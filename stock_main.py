# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import stock_process
import temperature_generator as tg
import sys
import getopt


if __name__ == '__main__':
    # args = sys.argv[1:]
    opts, args = getopt.getopt(sys.argv[1:], "th:d:i:s")

    input_date = None
    display_date = None
    print('处理开始，请稍后......')
    # 返回的参数opts是对应的选项和参数，args暂时不用管
    is_history = False
    show_temp = False
    stocks = None
    if len(opts) > 0:
        for op, value in opts:
            if op == '-h':
                is_history = True
                input_date = value
            elif op == '-d':
                display_date = value
            elif op == '-i':
                stocks = str(value).split(',')
            elif op == '-s':
                show_temp = True

    for stock in stocks:
        stock_process.generate(stock, input_date, show_temp)
    print("处理结束")
    sys.exit(0)

