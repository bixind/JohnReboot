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

    def dispense(self, command, args):
        try:
            return self.modules.get(command, defaultModule)(args)
        except Exception as e:
            logging.exception(e)
            return 'Error'
