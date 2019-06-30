# -*- coding: UTF-8 -*-
from pyecharts import Gauge


def value_formatter(value):
    value = (value + '').split('.')
    value.length < 2 and (value.push('0'))
    return value[0] + '.' + value[1] + '°C'


def generate_chart(date, value, name, show_temp):
    gauge = Gauge("券商温湿度", width=800, height=600)
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
            "id": "barcode",
            "right": 350,
            "top": 230,
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
    option['series'].append({
        "name": "业务指标",
        "type": "gauge",
        "detail": {
            "show": show_temp,
            "fontSize": 20,
            "formatter": value_formatter
        },
        "title": {
            "fontSize": 20
        },
        'axisLabel': {
            'show': True
        },
        "data": [{
            "value": value,
            "name": name
        }]
    })
    return gauge
