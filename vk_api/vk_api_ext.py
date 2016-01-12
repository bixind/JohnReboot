# -*- coding: utf-8 -*-

from vk_api.vk_api import *
import threading

class VkApiExt(VkApi):

    users = {}
    logged = ''
    def __init__(self, login=None, password=None, number=None, sec_number=None,
                 token=None, proxies=None, captcha_handler=None,
                 config_filename='vk_config.json',
                 api_version=None, app_id=4953880, scope=33554431,
                 client_secret=None):
        super().__init__(login, password, number, sec_number,
                 token, proxies, captcha_handler,
                 config_filename,
                 api_version, app_id, scope,
                 client_secret)
        self.id = self.method('users.get')[0]['id']
        self.methodLock = threading.Lock()
        self.guid = 0

    def method(self, method, values=None, captcha_sid=None, captcha_key=None):
        self.methodLock.acquire()
        val = super().method(method, values, captcha_sid, captcha_key)
        self.methodLock.release()
        return val

    def sendMessage(self, values, captcha_sid=None, captcha_key=None):
        values['guid'] = self.guid
        self.guid+=1
        return self.method('messages.send', values=values, captcha_sid=captcha_sid, captcha_key=captcha_key)

    def init_users(self):
        r = self.method('friends.get')
        ids = r['items']
        names = self.method('users.get', {'user_ids' : ",".join(map(str, ids))})
        for user in names:
            self.users[int(user['id'])] = user
        self.logged = self.method('users.get')[0]

    def get_user(self, id):
        id = int(id)
        if id in self.users:
            return self.users[id]
        else:
            user = self.method('users.get', {'user_ids' : id})
            if user:
                self.users[id] = user[0]
                return user[0]
