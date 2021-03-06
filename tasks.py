# -*- coding: utf-8 -*-

import weather.weather as weather
import audio.audio as audio
import aliases.aliases as aliases
import instrate.instrate as instrate
import history.history as history
import pollanalyse.pollanalyse as pollanalyse
import imageprocessing.imageprocessing as images
from time import *
import logging


def defaultModule(com, vk):
    return {'message' : 'Nemo omnia potest scire'}

class Dispenser:
    def __init__(self, vk):
        self.modules = {'погода' : weather.makeWeatherReport,
                        'аудио' : audio.getAudio,
                        'иначе' : aliases.setAlias,
                        'рейтинг' : instrate.getRating,
                        'история' : history.getHistory,
                        'опрос' : pollanalyse.getPollInfo,
                        'шакализировать' : images.getShakalized}
        self.vk = vk

    def dispense(self, com):
        try:
            command = com.args[0]
            if command in self.modules:
                return self.modules[com.args[0]](com, self.vk)
            newargs = aliases.getAlias(com.id, command)
            if newargs is None:
                return defaultModule(com, self.vk)
            args = (newargs + com.args[1:])
            com = com._replace(args=args)
            command = com.args[0]
            if command in self.modules:
                return self.modules[com.args[0]](com, self.vk)
            return defaultModule(com, self.vk)
        except Exception as e:
            logging.exception(e)
            return 'Error'

