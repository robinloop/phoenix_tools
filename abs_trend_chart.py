# -*- coding: UTF-8 -*-

from pyecharts import Line
import pandas as pd

CHART_NAMES = ["收盘点位", "绝对温度", "相对温度"]


def generate(df, stockCode, stockName):
    dates = df['date']
    y_axises2 = []
    y_axises2.append(df['absolute_temp'])
    y_axises2.append(df['relative_temp'])
    y_axises = df["cp"]

    line = Line(width=1200)
    option = option_process(stockCode, stockName, CHART_NAMES, dates, y_axises, y_axises2)

    # line.render('output/temp_line.html')
    # line._option = getOption()
    file = 'output/abs_temp_line_' + stockCode + '.html'
    line._option = option
    line.render(path=file, template_name='template/temp_history.html', object_name='line')


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
                "name": '指数',
                "type": "value",
                "min": "dataMin",
                "max": "dataMax",
                "maxInterval": 1000,
                "minInterval": 100,
                # "nameLocation": 'start',
                # "max": 5,
                # "type": 'value',
            },
            {
                "name": "温度",
                "scale": True,
                "splitArea": {
                    "show": True
                },
                'max': 100,
                'interval': 10
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
    color = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074',
             '#546570', '#c4ccd3']
    length = len(names)
    for index, name in enumerate(names):
        if 0 == index:
            yAxisIndex = 0
            data = y_axises
        else:
            yAxisIndex = 1
            data = y_axises2[index - 1]

        series = {
            'type': 'line',
            'name': name,
            "yAxisIndex": yAxisIndex,
            'data': data,
            'symbol': 'none',
            "smooth": True,
            "lineStyle": {
                "width": 1.5
            },
            "color": color[index]
        }
        option['series'].append(series)
    return option


# generate()