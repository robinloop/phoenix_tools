# -*- coding: UTF-8 -*-

from pyecharts import Line
import pandas as pd

CHART_NAMES = ["收盘点位", "绝对温度", "相对温度", "平均温度", "PB", "PE", "ROE", "V_PB", "十年国债收益"]
# Y_AXIS_NAMES = ['收盘价', '温度']
LINE_COLOR = ['#000000', '#c23531', '#006400',  '#FFD306', '#FCFCFC', '#FCFCFC', '#FCFCFC', '#FCFCFC', '#FCFCFC']


def option_process(stockCode, stockName, names, x_axis, y_axises, y_axises2, Y_AXIS_NAMES):
    option = {
        "title": {
            "text": stockName + '(' + stockCode + ')',
            "textAlign": 'center',
            'left': 200,
            'top': 10
            },
        # "graphic": [
            # {
            #     "type": "image",
            #     "id": "logo",
            #     "left": 5,
            #     "top": 60,
            #     "z": 10,
            #     "bounding": "raw",
            #     "draggable": True,
            #     "origin": [75, 75],
            #     "style": {
            #         "image": "image/logo.jpg",
            #         "width": 80,
            #         "height": 80,
            #         "opacity": 1
            #     }
            # },
            # {
            #     "type": "image",
            #     "id": "barcode",
            #     "left": 0,
            #     "top": 160,
            #     "z": 10,
            #     "bounding": "raw",
            #     "draggable": True,
            #     "origin": [75, 75],
            #     "style": {
            #         "image": "image/barcode.jpg",
            #         "width": 90,
            #         "height": 90,
            #         "opacity": 1
            #     }
            # }],
        "toolbox": {
            "orient": "vertical",
            'top': 60,
            "right": 50,
            "feature": {
                "dataZoom": {
                    "yAxisIndex": True
                },
                "brush": {
                    "type": ["lineX", "clear"]
                }
            }
        },
        "tooltip": {
            "trigger": "axis",
            # "axisPointer": {
            #     "type": "cross"
            #     }
        },
        "legend": {
            "data": names,
            'top': 10
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "bottom": "15%"
        },
        "xAxis": {
            "type": "category",
            "data": x_axis,
            "scale": True,
            "boundaryGap": False,
            "axisLine": {
                "onZero": False
            },
            "splitLine": {
                "show": False
            },
            "splitNumber": 40,
            "min": "dataMin",
            "max": "dataMax"
        },
        "yAxis": [
            {
                "name": Y_AXIS_NAMES[0],
                "type": "value",
                "min": "dataMin",
                "max": "dataMax",
                # "maxInterval": 1000,
                "minInterval": 100,
                "splitLine": {
                    "show": False
                },
                # "nameLocation": 'start',
                # "max": 5,
                # "type": 'value',
            },
            {
                "name": Y_AXIS_NAMES[1],
                "scale": True,
                "splitArea": {
                    "show": True
                },
                'max': 100,
                'interval': 10,
                'min': 0
                # 'boundaryGap': [0, '100%'],
            }
        ],
        "dataZoom": [{
            "type": "inside",
            "start": 90,
            "end": 100
        }, {
            "show": True,
            "type": "slider",
            "y": "90%",
            "start": 90,
            "end": 100
        }],
        'series': [],
        'legend': {
            'data': []
        }
    }
    for index, name in enumerate(names):
        line_width = 1.5
        if 0 == index:
            yAxisIndex = 0
            data = y_axises
            line_width = 3
        else:
            yAxisIndex = 1
            data = y_axises2[index - 1]

        if index > 3:
            line_width = 0
        show_temp = True
        series = {
            'type': 'line',
            'name': name,
            "yAxisIndex": yAxisIndex,
            'data': data,
            'symbol': 'none',
            "smooth": True,
            "lineStyle": {
                "width": line_width
            },
            "showSymbol ": False,
            "color": LINE_COLOR[index]
        }
        option['series'].append(series)

        if index < 4:
            option['legend']['data'].append(name)
    return option




def generate(df, flg, stockCode, stockName, is_gen_single):
    Y_AXIS_NAMES = ['收盘价', '温度']
    if flg is 'stock_A':
        Y_AXIS_NAMES = ['前复权', '温度']
    dates = df['date']
    y_axises2 = []
    y_axises2.append(df['absolute_temp'])
    y_axises2.append(df['relative_temp'])
    decimal = 3
    y_axises2.append(df['avg_temp'].round(decimals=decimal))
    y_axises2.append(df['pb'].round(decimals=decimal))
    y_axises2.append(df['pe'].round(decimals=decimal))
    y_axises2.append(df['roe'].round(decimals=decimal))
    y_axises2.append(df['s'].round(decimals=decimal))
    y_axises2.append(df['guozhai'].round(decimals=decimal))
    y_axises = df["cp"]

    line = Line(width=1200, title=stockName)
    option = option_process(stockCode, stockName, CHART_NAMES, dates, y_axises, y_axises2, Y_AXIS_NAMES)

    # line.render('output/temp_line.html')
    # line._option = getOption()
    file = 'output/abs_temp_line_' + flg + '_' + stockCode + '.html'
    line._option = option
    if is_gen_single is True:
        line.render(path=file, template_name='template/temp_history.html', object_name='line')
    return line


# generate()