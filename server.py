# -*- coding: utf-8 -*-

from vk_api.vk_api_ext import *
from longpoll import *
from threading import *
from tasks import *
import logging as log

log.basicConfig(filename='log.txt', format='%(asctime)s\n%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')

with open('session.token') as f:
    at = f.readline()

vk = VkApiExt(token=at)
disp = Dispenser()

def processMessage(vk, disp, upd):
    try:
        if upd[3] > 2000000000 or (upd[2] & 2) != 0:
            return
        mssg = upd[6]
        args = mssg.split()
        if len(args) > 0 and len(args[0]) > 0 and args[0][0] is '!':
            args[0] = args[0][1:]
            mssg = disp.dispense(args[0], [upd[3], args])
        vk.method('messages.send', {'user_id' : upd[3], 'message' : mssg})
    except Exception as e:
        logging.exception(e)


h = Handler({4 : lambda upd : processMessage(vk, disp, upd)})

t = Thread(daemon=True, target=longpoll, args=[vk, h])

t.start()

input()
