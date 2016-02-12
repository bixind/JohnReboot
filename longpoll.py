# -*- coding: utf-8 -*-

from urllib.request import *
from urllib.parse import *
from urllib.error import *
import json
import logging


class Handler:
    def __init__(self, commands = {}):
        self.commands = commands

    def handle(self, upd):
        if upd[0] in self.commands:
            self.commands[upd[0]](upd)


def longpoll(vk, handler):
    while True:
        try:
            l = []
            v = vk.method('messages.getLongPollServer')
            ts = v['ts']
            key = v['key']
            wait = 25
            mode = 2 + 8
            try:
                while True:
                    data = urlencode({'act':'a_check', 'key' : key, 'ts' : ts, 'wait' : wait, 'mode' : mode})
                    s = urlopen('http://' + v['server'] + '?' + data)
                    l = json.loads(s.read().decode('utf-8'))
                    if 'failed' in l:
                        logging.warning(l)
                        break
                    ts = l['ts']
                    for upd in l['updates']:
                        handler.handle(upd)
                    vk.method('account.setOnline', {'void' : 0})
            except HTTPError as e:
                logging.error(e)
            except Exception as e:
                logging.exception(l)
        except Exception as e:
            logging.exception(e)