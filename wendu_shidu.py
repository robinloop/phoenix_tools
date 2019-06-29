# -*- coding: UTF-8 -*-
from pyecharts import Gauge
import util.constants as constants

TEMP_NAME = ["券商温度", "券商湿度"]


def value_formatter(value):
    value = (value + '').split('.')
    value.length < 2 and (value.push('0'))
    return value[0] + '.' + value[1] + '°C'


def generate_chart(date, data, show_temp):
    gauge = Gauge("券商温湿度", width=800, height=600)
    option = gauge._option

    value = data['399975']
    wendu = round(value[constants.PB_PERCENTILE])
    shidu = round(value[constants.PE_PERCENTILE])
    name = TEMP_NAME[0]
    if show_temp:
        name = name + '\n ' + value[constants.FIFTY_SIGNAL] + ' ' + value[constants.HUNDRED_SIGNAL]

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
            'show': False
        },
        "data": [{
            "value": wendu,
            "name": name
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
            "fontSize": 20,
            "formatter": value_formatter
        },
        "data": [{
            "value": shidu,
            "name": TEMP_NAME[1]
        }]
    })
    # gauge.change_option(options)
    # gauge.render(path=file, template_name='template/six_gauge_template.html', object_name='gauge')
    return gauge
