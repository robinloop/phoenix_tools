# -*- coding: UTF-8 -*-

from pyecharts import Line
import pandas as pd

CHART_NAMES = ["指数收益率%", "10年国债收益率% * 2", "BP差"]
Y_AXIS_NAMES = ['收益率%', 'BP差']
LINE_COLOR = ['#c23531', '#006400', '#000000']


def generate(df, flg, stockCode, stockName):
    dates = df['date']
    y_axises = []
    y_axises.append(df['shouyi'])
    y_axises.append(df['g_roe'])
    y_axises2 = df["bp"]

    line = Line(width=1200)
    option = option_process(stockCode, stockName, CHART_NAMES, dates, y_axises, y_axises2)

    # line.render('output/temp_line.html')
    # line._option = getOption()
    file = 'output/niuxiong_line_' + flg + '_' + stockCode + '.html'
    line._option = option
    line.render(path=file, template_name='template/temp_history2.html', object_name='line')


def option_process(stockCode, stockName, names, x_axis, y_axises, y_axises2):
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
                # "minInterval": 100,
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
                # 'max': 100,
                # 'interval': 10
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
        'series': []
    }

    for index, name in enumerate(names):
        line_width = 1.5
        if 2 == index:
            yAxisIndex = 1
            data = y_axises2
            line_width = 1
        else:
            yAxisIndex = 0
            data = y_axises[index]

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
            "color": LINE_COLOR[index]
        }
        option['series'].append(series)
    return option


# generate()