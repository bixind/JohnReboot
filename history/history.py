import vk_api.vk_upload as upl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fonts
import matplotlib as mpl
import time
import datetime as date
import random
from historycontrol import historyLock
import os.path

day = 60 * 60 * 24
empty_timeout = 5*60
timeout = 14 * 60

mpl.rcdefaults()
font = {'family': 'stixgeneral',
        'weight': 'normal'}
mpl.rc('font', **font)

def makeChart(vk):
    d = date.datetime.now(date.timezone(date.timedelta(hours=4)))
    now = int(time.time())
    tp = time.localtime(now)
    dh = day - (tp.tm_min * 60 + tp.tm_sec)
    ch = d.hour
    offx = 100

    l = dict()

    with historyLock, open('history.txt') as f:
        for s in f:
            s = s.split()
            id = -int(s[1])
            if id not in l:
                l[id] = []
            if now - day < int(s[3]):
                l[id].append([int(s[0]) - 8, int(s[3]), int(s[2])])

    fxl = dict()

    for id in l:
        pos = -1
        fxl[id] = []
        for el in l[id]:
            if el[0] == 0 and pos == -1:
                fxl[id].append(el)
                pos = el[1]
            elif el[0] == 0 and pos != -1:
                fxl[id].append([1, pos + empty_timeout, 0])
                fxl[id].append(el)
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                if el[2] == 1:
                    el[1] -= timeout
                fxl[id].append(el)
                pos = -1
    l = fxl

    tmid = []
    for id in l:
        st = 0
        pos = -1
        for el in l[id]:
            if el[0] == 0 and pos == -1:
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                st += el[1] - pos
                pos = -1
        if pos != -1:
            st += now - pos
        tmid.append([st, id])
    tmid.sort(key = lambda x : x[0])

    r = vk.method('users.get', {'user_ids' : ','.join(str(u) for u in l)})
    usernames = dict()
    for user in r:
        usernames[user['id']] = user['first_name'] + ' ' + user['last_name']

    plt.figure(1, figsize=(20, len(l) * 3 + 1))
    plt.subplot(2, 1, 1)
    while dh > 0:
        plt.axvline(dh // 60, ls = 'dashed', color = '#B0B0B0')
        plt.annotate(str(ch) + ':00', xy = (dh // 60 + 5, 0), fontproperties = fonts.FontProperties(size = 10))
        dh -= 60*60
        ch -= 1
        if ch < 0:
            ch += 24
    dx = 0
    for st, id in tmid:
        dx += 1
        pos = -1
        usrclr = [random.random() / 2, random.random() / 2, random.random() / 2]
        usrclrfd = list(min(1, clr + 0.5) for clr in usrclr)
        plt.axhline(dx, lw = 1, color = usrclrfd)
        for el in l[id]:
            if el[0] == 0 and pos == -1:
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                plt.plot([(pos - now + day) // 60, (el[1] - now + day) // 60], [dx, dx], color = usrclr, linewidth=2.0)
                pos = -1
        if pos != -1:
            plt.plot([(pos - now + day) // 60, day // 60], [dx, dx], color = usrclr, linewidth=2.0)
        plt.annotate(usernames[id], xy = (-offx, dx + 0.2), fontproperties = fonts.FontProperties(size = 10))
    # plt.plot([0],[0], 'b', linewidth=2.0)
    # plt.plot([day // 60],[dx + 1], 'b', linewidth=2.0)
    # plt.annotate('KEK', xy = (2, 2.2))
    plt.axis([-offx, day // 60, 0, dx + 1])
    plt.axis('off')
    plt.savefig('hist.png', bbox_inches = 'tight')

def makePersonalChart(id):
    d = date.datetime.now(date.timezone(date.timedelta(hours=4)))
    now = int(d.timestamp())
    last_update = now - d.hour * 60*60 - d.minute * 60 - d.second
    print(last_update)
    dg = list()
    cnt = 10
    while cnt > 0:
        cnt-=1
        curdname = time.strftime('%Y-%m-%d', time.localtime(last_update))
        l = []
        if os.path.exists('days/' + curdname + '/' + str(id) + '.txt'):
            with historyLock, open('days/' + curdname + '/' + str(id) + '.txt') as f:
                for s in f:
                    s = s.split()
                    l.append([int(s[0]) - 8, int(s[3]) - last_update, int(s[2])])
        dg.append([curdname, l])
        last_update -= day


    fxdg = []
    for dayname, lt in dg:
        pos = -1
        nlt = []
        for el in lt:
            if el[0] == 0 and pos == -1:
                nlt.append(el)
                pos = el[1]
            elif el[0] == 0 and pos != -1:
                nlt.append([1, pos + empty_timeout, 0])
                nlt.append(el)
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                if el[2] == 1:
                    el[1] -= timeout
                nlt.append(el)
                pos = -1
        fxdg.append([dayname, lt])
    dg = fxdg

    plt.figure(1, figsize=(20, len(dg) * 3 + 1))
    plt.subplot(2, 1, 1)
    dh = day
    ch = 0
    while dh > 0:
        plt.axvline(dh // 60, ls = 'dashed', color = '#B0B0B0')
        plt.annotate(str(ch) + ':00', xy = (dh // 60 + 5, 0), fontproperties = fonts.FontProperties(size = 10))
        dh -= 60*60
        ch -= 1
        if ch < 0:
            ch += 24
    dx = 0
    offx = 100
    for dayname, lt in dg:
        dx += 1
        pos = -1
        usrclr = [random.random() / 2, random.random() / 2, random.random() / 2]
        usrclrfd = list(min(1, clr + 0.5) for clr in usrclr)
        plt.axhline(dx, lw = 1, color = usrclrfd)
        # print(dayname, lt)
        for el in lt:
            if el[0] == 0 and pos == -1:
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                plt.plot([pos // 60, (el[1]) // 60], [dx, dx], color = usrclr, linewidth=2.0)
                pos = -1
        if pos != -1:
            plt.plot([pos // 60, day // 60], [dx, dx], color = usrclr, linewidth=2.0)
        plt.annotate(dayname, xy = (-offx, dx + 0.2), fontproperties = fonts.FontProperties(size = 10))
    # plt.plot([0],[0], 'b', linewidth=2.0)
    # plt.plot([day // 60],[dx + 1], 'b', linewidth=2.0)
    # plt.annotate('KEK', xy = (2, 2.2))
    plt.axis([-offx, day // 60, 0, dx + 1])
    plt.axis('off')
    plt.savefig('pershist.png', bbox_inches = 'tight')

def getHistory(com, vk):
    if len(com.args) == 1:
        makeChart(vk)
        vu = upl.VkUpload(vk)
        r = vu.photo_messages(photos=['hist.png'])
    elif len(com.args) == 2:
        r = vk.method('users.get', {'user_ids' : 'com.args[1]'})
        id = r[0]['id']
        if id in vk.users:
            makePersonalChart(id)
            vu = upl.VkUpload(vk)
            r = vu.photo_messages(photos=['pershist.png'])
        else:
            return {'attachment': 'photo325483887_400964540'}
    elif len(com.args) == 3:
        lname = com.args[1]
        fname = com.args[2]
        id = -1
        for user in vk.users:
            if lname == user['last_name'].lower() and fname == user['first_name'].lower():
                id = user['id']
                break
        if id in vk.users:
            makePersonalChart(id)
            vu = upl.VkUpload(vk)
            r = vu.photo_messages(photos=['pershist.png'])
        else:
            return {'attachment': 'photo325483887_400964540'}
    else:
        return {'attachment': 'photo325483887_400964540'}
    return {'attachment': 'photo' + str(r[0]['owner_id']) + '_' + str(r[0]['id'])}
