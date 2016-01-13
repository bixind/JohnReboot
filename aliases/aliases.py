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
    userAliases = {}
    if os.path.exists(prpath + str(id) + '.txt'):
        userAliases = jsonRead(prpath + str(id) + '.txt')
    userAliases[com.args[1]] = com.args[2:]
    jsonSave(prpath + str(id) + '.txt', userAliases)
