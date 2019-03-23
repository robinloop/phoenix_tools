# -*- coding: UTF-8 -*-
from pyecharts import Gauge

LOCATION = [["20%", "30%"], ["45%", "30%"], ["70%", "30%"],
                       ["20%", "60%"], ["45%", "60%"], ["70%", "60%"]]
TEMP_NAME = ["上证指数", "创业板指", "中证全指", "上证50", "沪深300", "中证500"]


def value_formatter(value):
    value = (value + '').split('.')
    value.length < 2 and (value.push('0'))
    return value[0] + '.' + value[1] + '°C'


def generate_chart(date, data, file):
    gauge = Gauge(width=900, height=600)
    option = gauge._option
    option['title'] = {
        "text": date,
        "left": "39%",
        "top": "5%"
        }
    option['tooltip'] = {
        "formatter": "{b} : {c}°C"
        }
    option['toolbox'] = {
      "show": False
    }
    option["graphic"] = [{
        "type": "image",
        "id": "logo",
        "right": 675,
        "top": 20,
        "z": 10,
        "bounding": "raw",
        "draggable": True,
        "origin": [75, 75],
        "style": {
                "image": "image/logo.png",
                "width": 50,
                "height": 50,
                "opacity": 1
            }
        },
        {
        "type": "image",
        "id": "barcode",
        "right": 275,
        "top": 20,
            "z": 10,
            "bounding": "raw",
            "draggable": True,
            "origin": [75, 75],
            "style": {
                "image": "image/barcode.jpg",
                "width": 50,
                "height": 50,
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
                    "fontSize": 20
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
                "fontSize": 20,
                "formatter": value_formatter
                },
            "data": [{
                "value": data[index],
                "name": name
                }]
            })
    # gauge.change_option(options)
    gauge.render(path=file, template_name='template/six_gauge_template.html', object_name='gauge')
