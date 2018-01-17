# -*- coding: utf-8 -*-

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import vk_api.vk_api_ext
import vk_api.vk_api
from longpoll import *
from threading import *
import logging as log
import time
from historycontrol import statusChange
from history.history import makeChart

log.basicConfig(filename='log.txt', format='%(asctime)s\n%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')

with open('session.token') as f:
    at = f.readline()

vk = vk_api.vk_api_ext.VkApiExt(token=at)

h = Handler({8: statusChange,
             9: statusChange})

t = Thread(daemon=True, target=longpoll, args=[vk, h])

t.start()

while True:
    s = input()
    if s == 'makechart':
        makeChart(vk)
    if len(s) > 0 and s[0] == 'q':
        break
