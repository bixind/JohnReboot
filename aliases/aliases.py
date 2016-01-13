# -*- coding: utf-8 -*-

from fileparse import *
import os.path

prpath = 'aliases/preferences/'

def getAlias(id, command):
    if os.path.exists(prpath + str(id) + '.txt'):
        userAliases = jsonRead(prpath + str(id) + '.txt')
    else:
        return None
    if command in userAliases:
        return userAliases[command]
    else:
        return None

def setAlias(com, vk):
    if len(com.args) < 3:
        return {'message' : 'Consequentia non valet'}
    userAliases = {}
    if os.path.exists(prpath + str(com.id) + '.txt'):
        userAliases = jsonRead(prpath + str(com.id) + '.txt')
    userAliases[com.args[1]] = com.args[2:]
    jsonSave(prpath + str(com.id) + '.txt', userAliases)
    return {'message' : 'Ad futarum memoriam'}
