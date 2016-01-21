# -*- coding: utf-8 -*-

import os

def convertText(text):
    with open('input.txt', 'w', encoding='utf-8') as f:
        print(text, file=f)
    os.system('./mystem -ni input.txt output.txt')
    with open('output.txt', 'r') as f:
        res = f.read()
    return res