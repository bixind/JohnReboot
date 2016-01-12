# -*- coding: utf-8 -*-

import sys
from vk_api import vk_api

def get_access_token(login, password):
	vk = vk_api.VkApi(login, password)
	try:
		vk.authorization()
	except vk_api.AuthorizationError as error_msg:
		print(error_msg)
		exit()
	print("Authorization: OK")
	return vk.token["access_token"]

f = open('config.txt', 'r')
#login, password = sys.stdin.readline().split()
login, password = f.readline().split()
f.close()

access_token = get_access_token(login, password)
with open("session.token", "wb") as f:
	f.write(access_token.encode())
