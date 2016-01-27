# -*- coding: utf-8 -*-

import vk_api.vk_api_ext
import vk_api.vk_api
from longpoll import *
from threading import *
from tasks import *
import logging as log
from constants import *
import time
from urllib.request import *
from urllib.parse import *
import json
import requests
import vk_api.vk_upload as upl
from history.history import *

log.basicConfig(filename='log.txt', format='%(asctime)s\n%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')

with open('session.token') as f:
    at = f.readline()

vk = vk_api.vk_api_ext.VkApiExt(token=at)

friends = set(vk.method('friends.get')['items'])
possible_friends = dict()
for user in friends:
    try:
        friends_of_friend = vk.method('friends.get', {'user_id': user})['items']
        print(friends_of_friend)
        for pf in friends_of_friend:
            possible_friends[pf] = possible_friends.get(pf, 0) + 1
    except Exception as e:
        print(e)
        print(user)
subscr = vk.method('users.getSubscriptions')['users']['items']
for user in subscr:
    if user in possible_friends:
        del possible_friends[user]
for user in friends:
    if user in possible_friends:
        del possible_friends[user]
print(len(possible_friends))
sl = list(zip(possible_friends.keys(), possible_friends.values()))
sl.sort(key=lambda x : -x[1])
sf = ','.join(str(e[0]) for e in sl[:990])
# print(sf)
names_of_friends = vk.method('users.get', {'user_ids' : sf})
names_of_friends.sort(key=lambda x:-possible_friends[x['id']])
with open('output.txt', 'w', encoding='utf-8') as f:
    for user in names_of_friends:
        print(possible_friends[user['id']], user, file = f)