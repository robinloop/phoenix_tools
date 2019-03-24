# -*- coding: UTF-8 -*-
from pyecharts import Gauge

TEMP_NAME = ["券商温度", "券商湿度"]


def value_formatter(value):
    value = (value + '').split('.')
    value.length < 2 and (value.push('0'))
    return value[0] + '.' + value[1] + '°C'


def generate_chart(date, data):
    gauge = Gauge("券商温湿度", width=800, height=600)
    option = gauge._option

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
            "fontSize": 20,
            "formatter": value_formatter
        },
        "title": {
            "fontSize": 20
        },
        "data": [{
            "value": data[0],
            "name": TEMP_NAME[0] + " " + date
        }]
    })
    option['series'].append({
        "name": "业务指标",
        "type": "gauge",
        "center": ['50%', '85%'],
        "radius": "35%",
        "title": {
            "fontSize": 20,
            "offsetCenter": [0, '-30%']
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
            "value": data[1],
            "name": TEMP_NAME[1]
            }]
        })
    # gauge.change_option(options)
    # gauge.render(path=file, template_name='template/six_gauge_template.html', object_name='gauge')
    return gauge
