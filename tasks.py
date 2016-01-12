# -*- coding: utf-8 -*-

import weather.weather as weather
import audio.audio as audio
from time import *
import logging

def defaultModule(com, vk):
    return {'message' : 'Команда ' + str(com.args[0]) + ' не найдена'}

class Dispenser:
    def __init__(self, vk):
        self.modules = {'погода' : weather.makeWeatherReport,
                        'аудио' : audio.getAudio}
        self.vk = vk

    def dispense(self, command, com):
        try:
            return self.modules.get(command, defaultModule)(com, self.vk)
        except Exception as e:
            logging.exception(e)
            return 'Error'
