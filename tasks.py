# -*- coding: utf-8 -*-

import weather
from time import *
import logging

def defaultModule(args):
    return 'Команда ' + str(args[0]) + ' не найдена'

class Dispenser:
    def __init__(self):
        self.modules = {}
        self.modules['погода'] = weather.makeWeatherReport

    def dispense(self, args):
        try:
            return self.modules.get(args[0], defaultModule)(args)
        except Exception as e:
            logging.exception(e)
            return 'Error'
