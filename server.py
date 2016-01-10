# -*- coding: utf-8 -*-

from vk_api.vk_api_ext import *
from longpoll import *
from threading import *

# with open("session.token", "wb") as f:
# 	vk = VkApi(token=f.readline())

with open('session.token') as f:
    at = f.readline()

vk = VkApiExt(token=at)

def echo(vk, upd):
    if upd[3] > 2000000000 or (upd[2] & 2) != 0:
        return
    print(upd[3])
    vk.method('messages.send', {'user_id' : upd[3], 'message' : upd[6]})

h = Handler({4 : lambda upd : echo(vk, upd)})

t = Thread(daemon=True, target=longpoll, args=[vk, h])

t.start()

input()
