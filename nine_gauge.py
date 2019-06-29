# -*- coding: UTF-8 -*-
from pyecharts import Gauge
import util.constants as constants

LOCATION = [
    ["20%", "30%"], ["45%", "30%"], ["70%", "30%"],
    ["20%", "60%"], ["45%", "60%"], ["70%", "60%"],
    ["20%", "90%"], ["45%", "90%"], ["70%", "90%"]
]


def value_formatter(value):
    value = (str(value) + '').split('.')
    value.length < 2 and (value.push('0'))
    print(value)
    return value[0] + '.' + value[1] + '°C'


def generate_chart(stock_temp, date, data, show_temp):
    gauge = Gauge("指数温度", width=900, height=600)
    option = gauge._option
    option['title'] = {
        "text": "公众号：金凤钱潮策略 " + date,
        "left": "15%",
        "top": "5%"
    }
    option['tooltip'] = {
        "formatter": "{b} : {c}°C"
    }
    option['toolbox'] = {
        "show": False
    }
    option["graphic"] = [
        {
            "type": "image",
            "id": "logo",
            "right": 205,
            "top": 20,
            "z": 10,
            "bounding": "raw",
            "draggable": True,
            "origin": [75, 75],
            "style": {
                "image": "image/logo.jpg",
                "width": 90,
                "height": 90,
                "opacity": 1
            }
        },
        {
            "type": "image",
            "id": "barcode",
            "right": 320,
            "top": 15,
            "z": 10,
            "bounding": "raw",
            "draggable": True,
            "origin": [75, 75],
            "style": {
                "image": "image/barcode.jpg",
                "width": 100,
                "height": 100,
                "opacity": 1
            }
        }]

    for index, value in enumerate(stock_temp):
        code, name = value
        if show_temp:
            name = name + '\n ' + data[code][constants.FIFTY_SIGNAL] + ' ' + data[code][constants.HUNDRED_SIGNAL]

        val = round(data[code][constants.PB_PERCENTILE], 1)
        option['series'].append({
            "name": "业务指标",
            "type": "gauge",
            "center": LOCATION[index],
            "radius": "35%",
            "title": {
                "fontSize": 16,
            },
            "axisLine": {
                "lineStyle": {
                    "width": 8
                }
            },
            "axisTick": {
                "length": 8,
                "lineStyle": {
                    "color": "auto"
                }
            },
            'axisLabel': {
                'show': False
            },
            "splitLine": {
                "length": 15,
                "lineStyle": {
                    "color": "auto"
                }
            },
            "pointer": {
                "width": 5
            },
            "detail": {
                "show": show_temp,
                "fontSize": 16,
                "formatter": value_formatter
            },
            "data": [{
                "value": val,
                "name": name
                # "name": name + "\n B 1"
            }]
        })
    return gauge
