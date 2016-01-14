# -*- coding: utf-8 -*-

from urllib.request import *
import json

def getUser(name):
    v = urlopen('https://www.instagram.com/' + name)
    s = str(v.read(), 'utf-8')
    p = s.find('window._sharedData = ')
    l = s.find('{', p)
    r = s.find(';', l)
    j = json.loads(s[l:r])
    return j['entry_data']['ProfilePage'][0]['user']

def getRating(com, vk):
    name = com.args[1]
    user = getUser(name)
    if user['followed_by']['count'] == 0 or user['follows']['count'] == 0 or user['media']['count'] == 0:
            rt =  0
    else:
        rt = user['followed_by']['count']**2/(user['media']['count']*user['follows']['count'])
    return {'message': name + ' : ' + str(rt)}
