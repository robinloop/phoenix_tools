# -*- coding: UTF-8 -*-
from pyecharts import Gauge

LOCATION = [["20%", "35%"], ["45%", "35%"], ["70%", "35%"],
            ["20%", "65%"], ["45%", "65%"], ["70%", "65%"]]
TEMP_NAME = ["上证指数", "创业板指", "中证全指", "上证50", "沪深300", "中证500"]


def value_formatter(value):
    value = (value + '').split('.')
    value.length < 2 and (value.push('0'))
    return value[0] + '.' + value[1] + '°C'


def generate_chart(date, data, show_temp):
    gauge = Gauge("指数温度", width=900, height=600)
    option = gauge._option
    option['title'] = {
        "text": "公众号：金凤钱潮策略 " + date,
        "left": "15%",
        "top": "7%"
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

    for index, name in enumerate(TEMP_NAME):
        option['series'].append({
            "name": "业务指标",
            "type": "gauge",
            "center": LOCATION[index],
            "radius": "35%",
            "title": {
                    "fontSize": 20,
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
                "fontSize": 20,
                "formatter": value_formatter
                },
            "data": [{
                "value": data[index],
                "name": name
                # "name": name + "\n B 1"
                }]
            })
    # gauge.change_option(options)
    # gauge.render(path=file, template_name='template/six_gauge_template.html', object_name='gauge')
    return gauge
