# -*- coding: utf-8 -*-

import weather.weather as weather
import audio.audio as audio
import aliases.aliases as aliases
from time import *
import logging

def defaultModule(com, vk):
    return {'message' : 'Nemo omnia potest scire'}

class Dispenser:
    def __init__(self, vk):
        self.modules = {'погода' : weather.makeWeatherReport,
                        'аудио' : audio.getAudio,
                        'иначе' : aliases.setAlias}
        self.vk = vk

    def dispense(self, com):
        try:
            command = com.args[0]
            if command in self.modules:
                return self.modules[com.args[0]](com, self.vk)
            newargs = aliases.getAlias(com.id, command)
            com._replace(args = com.args[1:] + newargs)
            command = com.args[0]
            if command in self.modules:
                return self.modules[com.args[0]](com, self.vk)
            return defaultModule(com, self.vk)
        except Exception as e:
            logging.exception(e)
            return 'Error'
