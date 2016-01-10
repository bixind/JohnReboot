# -*- coding: utf-8 -*-

import weather
from time import *

def defaultModule(args):
    return 'Команда ' + args[0] + ' не найдена'

class Dispenser:
    def __init__(self):
        self.modules = {}
        self.modules['погода'] = weather.makeWeatherReport

    def dispense(self, args):
        try:
            return self.modules.get(args[0], defaultModule)(args)
        except:
            print('some errors', time())
            return 'Error'
