# -*- coding: utf-8 -*-

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import vk_api.vk_api_ext
import vk_api.vk_api
from longpoll import *
from threading import *
from tasks import *
import logging as log
from collections import namedtuple
import time

log.basicConfig(filename='log.txt', format='%(asctime)s\n%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')

with open('session.token') as f:
    at = f.readline()

vk = vk_api.vk_api_ext.VkApiExt(token=at)
disp = Dispenser(vk)

Command = namedtuple('Command', ['id', 'args'])

def processMessage(vk, disp, upd):
    try:
        if upd[3] > 2000000000 or (upd[2] & 2) != 0:
            return
        mssg = upd[6]
        args = list(s.lower() for s in mssg.split())
        values = {'message' : mssg}
        values['user_id'] = upd[3]
        if len(args) > 0 and len(args[0]) > 0 and args[0][0] is '!':
            args[0] = args[0][1:]
            newvals = disp.dispense(Command(upd[3], args))
            del values['message']
            values.update(newvals)
        # values = dict(filter(lambda x : x[1] is not None, values.items()))
        try:
            vk.sendMessage(values)
        except vk_api.vk_api.ApiError as e:
            logging.warning(e)
            vk.sendMessage({'user_id' : upd[3], 'message' : 'Nihil verum est licet omnia'})
    except Exception as e:
        logging.exception(e)


def statusChange(upd):
    with open('history.txt', 'a') as f:
        print(*(upd + [round(time.time())]), file = f)

h = Handler({4: lambda upd : processMessage(vk, disp, upd),
             8: statusChange,
             9: statusChange})

t = Thread(daemon=True, target=longpoll, args=[vk, h])

t.start()

input()
