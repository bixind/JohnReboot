# -*- coding: utf-8 -*-

import sys
from vk_api import vk_api
from urllib.request import *
from urllib.parse import *
from urllib.error import *
from config import *
import re

def make_auth_url(app_id, scope):
    base = 'https://oauth.vk.com/authorize'
    data = urlencode({'client_id': str(app_id), 'redirect_uri': 'https://oauth.vk.com/blank.html',
                      'scope': scope, 'response_type': 'token', 'v': '5.69'})
    s = base + '?' + data
    return s

def extract_token(url):
    pass

print('Please enter page url after redirect:')
print(make_auth_url(app_id, 2 | 4096 | 65536))
res = input()

p = re.compile(r'access_token=(\w+)')
token = p.search(res).group(1)

with open("session.token", "wb") as f:
	f.write(token.encode())