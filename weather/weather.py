# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from urllib.request import *
import os.path
from fileparse import *

pref = '{http://weather.yandex.ru/forecast}'
prpath = 'preferences/'

defaultargs = {'сейчас'}

clockDict = {'1' : 'Утро', '2' : 'День', '3' : 'Вечер', '4' : 'Ночь'}

def getNow(fact):
    weather_report = ['Сейчас в Ижевске:']
    weather_report.append('Предположительное время: ' + fact.find(pref + 'uptime').text.split('T')[1])
    weather_report.append('Температура: ' + fact.find(pref + 'temperature').text)
    weather_report.append(fact.find(pref + 'weather_type').text.title())
    weather_report.append('Влажность: ' + fact.find(pref + 'humidity').text + '%')
    weather_report.append('Давление: ' + fact.find(pref + 'pressure').text + ' мм рт. ст.')
    weather_report.append('Скорость ветра: ' + fact.find(pref + 'wind_speed').text + ' м/с')
    return weather_report

def getDay(day):
    day_report = ['Прогноз на ' + day.get('date') + ':']
    for part in day.findall(pref + 'day_part'):
        if part.get('typeid') in clockDict:
            if part.find(pref + 'temperature') is not None:
                temp = part.find(pref + 'temperature').text
            else:
                temp = part.find(pref + 'temperature_from').text + '...' + part.find(pref + 'temperature_to').text
            wt = part.find(pref + 'weather_type').text.title()
            day_report.append('{:<7}{:<11}{}'.format(clockDict[part.get('typeid')], temp, wt))
    return day_report

def makeWeatherReport(args):
    id = args[0]
    args = args[1]
    wpb = urlopen('http://export.yandex.ru/weather-ng/forecasts/28411.xml')
    wp = str(wpb.read(), 'utf-8')
    root = et.fromstring(wp)
    if len(args) <= 1:
        if os.path.exists(prpath + str(id) + '.txt'):
            args = jsonRead(prpath + str(id) + '.txt')
        else:
            args = defaultargs()
    else:
        if 'предпочитаю' in args:
            jsonSave(prpath + str(id) + '.txt', args)
    report = ['Сводка погоды']
    predictions = root.findall(pref + 'day')
    if 'сейчас' in args:
        fact = root.find(pref + 'fact')
        report.extend(getNow(fact))
    if 'прогноз' in args:
        for el in predictions:
            report.extend(getDay(el))
    if 'сегодня' in args and len(predictions) > 0:
        report.extend(getDay(predictions[0]))
    if 'завтра' in args and len(predictions) > 1:
        report.extend(getDay(predictions[1]))
    if 'послезавтра' in args and len(predictions) > 2:
        report.extend(getDay(predictions[2]))
    return '\n'.join(report)