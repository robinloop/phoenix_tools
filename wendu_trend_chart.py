# -*- coding: UTF-8 -*-

from pyecharts import Line
import pandas as pd

STOCK_NAMES = ["日期", "上证指数PB", "创业板指PB", "中证全指PB", "上证50PB", "沪深300PB", "中证500PB", "证券公司PB", "证券公司PE"]
CHART_NAMES = ["上证指数温度", "创业板指温度", "中证全指温度", "上证50温度", "沪深300温度", "中证500温度", "证券公司温度", "证券公司湿度", "全指指数"]


def generate():
    df = pd.read_csv('data/temp_history.csv')
    df = df.sort_index(ascending=False)
    dates = df[STOCK_NAMES[0]]
    names = STOCK_NAMES[1:]
    y_axises = []
    for name in names:
        y_axises.append(df[name])

    y_axises2 = df["中证全指指数"]

    line = Line(width=1200)
    option = option_process(CHART_NAMES, dates, y_axises, y_axises2)

    # line.render('output/temp_line.html')
    # line._option = getOption()
    file = 'output/temp_line.html'
    line._option = option
    line.render(path=file, template_name='template/temp_history.html', object_name='line')


def option_process(names, x_axis, y_axises, y_axises2):
    option = {
        # "title": {
        #     "text": "上证指数",
        #     "textAlign": 'center',
        #     'left': 400,
        #     'top': -10
        #     },
        "graphic": [
            {
                "type": "image",
                "id": "logo",
                "left": 5,
                "top": 60,
                "z": 10,
                "bounding": "raw",
                "draggable": True,
                "origin": [75, 75],
                "style": {
                    "image": "image/logo.jpg",
                    "width": 80,
                    "height": 80,
                    "opacity": 1
                }
            },
            {
                "type": "image",
                "id": "barcode",
                "left": 0,
                "top": 160,
                "z": 10,
                "bounding": "raw",
                "draggable": True,
                "origin": [75, 75],
                "style": {
                    "image": "image/barcode.jpg",
                    "width": 90,
                    "height": 90,
                    "opacity": 1
                }
            }],
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
        "yAxis": [{
            "name": "温度",
            "scale": True,
            "splitArea": {
                "show": True
            },
            'max': 100,
            # 'boundaryGap': [0, '100%'],
        },
            {
                "name": '全指指数',
                "type": "value",
                # "min": "dataMin",
                # "max": "dataMax",
                "maxInterval": 1000,
                "minInterval": 100,
                # "nameLocation": 'start',
                # "max": 5,
                # "type": 'value',
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
        if length - 1 == index:
            yAxisIndex = 1
            data = y_axises2
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
                "width": 1.5
            },
            "color": color[index]
        }
        option['series'].append(series)
    return option


# generate()