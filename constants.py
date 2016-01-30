# -*- coding: utf-8 -*-
from collections import namedtuple

Command = namedtuple('Command', ['id', 'args', 'misc'])

def getAttachments(misc, type):
    i = 1
    res = []
    while 'attach' + str(i) in misc:
        if misc['attach' + str(i) + '_type'] == type:
            res.append(tuple(map(int, misc['attach' + str(i)].split('_'))))
        i+=1
    return res