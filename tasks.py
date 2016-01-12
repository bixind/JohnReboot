# -*- coding: utf-8 -*-

import weather.weather as weather
from time import *
import logging

def defaultModule(com):
    return 'Команда ' + str(com.args[0]) + ' не найдена'

class Dispenser:
    def __init__(self):
        self.modules = {}
        self.modules['погода'] = weather.makeWeatherReport

    def dispense(self, command, com):
        try:
            return self.modules.get(command, defaultModule)(com)
        except Exception as e:
            logging.exception(e)
            return 'Error'
