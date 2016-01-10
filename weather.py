# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from urllib.request import *

def makeWeatherReport(args):
    wpb = urlopen('http://export.yandex.ru/weather-ng/forecasts/28411.xml')
    wp = str(wpb.read(), 'utf-8')
    root = et.fromstring(wp)
    pref = '{http://weather.yandex.ru/forecast}'
    fact = root.find(pref + 'fact')
    weather_report = ['Сейчас в Ижевске:']
    weather_report.append('Предположительное время: ' + fact.find(pref + 'uptime').text.split('T')[1])
    weather_report.append('Температура: ' + fact.find(pref + 'temperature').text)
    weather_report.append(fact.find(pref + 'weather_type').text.title())
    weather_report.append('Влажность: ' + fact.find(pref + 'humidity').text + '%')
    weather_report.append('Давление: ' + fact.find(pref + 'pressure').text + ' мм рт. ст.')
    weather_report.append('Скорость ветра: ' + fact.find(pref + 'wind_speed').text + ' м/с')
    return '\n'.join(weather_report)
