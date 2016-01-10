# -*- coding: utf-8 -*-

from vk_api.vk_api import *
from urllib.request import *
from urllib.parse import *
import json
import requests


class Handler:
    def __init__(self, commands = {}):
        self.commands = commands
    def handle(self, upd):
        if upd[0] in self.commands:
            self.commands[upd[0]](upd)

def longpoll(vk, handler):
    v = vk.method('messages.getLongPollServer')
    ts = v['ts']
    key = v['key']
    wait = 25
    mode = 2
    while True:
        data = urlencode({'act':'a_check', 'key' : key, 'ts' : ts, 'wait' : wait, 'mode' : mode})
        s = urlopen('http://' + v['server'] + '?' + data)
        l = json.loads(s.read().decode('utf-8'))
        ts = l['ts']
        for upd in l['updates']:
            handler.handle(upd)