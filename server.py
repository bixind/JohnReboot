# -*- coding: utf-8 -*-

from vk_api.vk_api_ext import *
from longpoll import *
from threading import *
from tasks import *

# with open("session.token", "wb") as f:
# 	vk = VkApi(token=f.readline())

with open('session.token') as f:
    at = f.readline()

vk = VkApiExt(token=at)
disp = Dispenser()

def processMessage(vk, disp, upd):
    if upd[3] > 2000000000 or (upd[2] & 2) != 0:
        return
    mssg = upd[6]
    args = list(s[1:] for s in filter(lambda s : len(s) > 1 and s[0] is '!', mssg.split()))
    if len(args) > 0:
        disp.dispense(args)
    else:
        vk.method('messages.send', {'user_id' : upd[3], 'message' : upd[6]})

h = Handler({4 : lambda upd : processMessage(vk, disp, upd)})

t = Thread(daemon=True, target=longpoll, args=[vk, h])

t.start()

input()
