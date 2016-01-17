import vk_api.vk_upload as upl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fonts
import matplotlib as mpl
import time
import random

def makeChart(vk):
    day = 60 * 60 * 24
    now = int(time.time())
    tp = time.localtime(now)
    dh = day - (tp.tm_min * 60 + tp.tm_sec)
    ch = tp.tm_hour
    offx = 100

    l = dict()
    with open('history.txt') as f:
        for s in f:
            s = s.split()
            id = -int(s[1])
            if id not in l:
                l[id] = []
            if now - day < int(s[3]):
                l[id].append([int(s[0]) - 8, int(s[3])])

    mpl.rcdefaults()
    font = {'family': 'Courier New',
            'weight': 'normal'}
    mpl.rc('font', **font)

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
    for id in l:
        dx += 1
        pos = -1
        usrclr = [random.random(), random.random(), random.random()]
        usrclrfd = list(min(1, clr + 0.5) for clr in usrclr)
        plt.axhline(dx, lw = 1, color = usrclrfd)
        for el in l[id]:
            if el[0] == 0 and pos == -1:
                pos = el[1]
            elif el[0] == 1 and pos != -1:
                plt.plot([(pos - now + day) // 60, (el[1] - now + day) // 60], [dx, dx], color = usrclr, linewidth=2.0)
                pos = -1
        plt.annotate(usernames[id], xy = (-offx, dx + 0.2), fontproperties = fonts.FontProperties(size = 10))
    # plt.plot([0],[0], 'b', linewidth=2.0)
    # plt.plot([day // 60],[dx + 1], 'b', linewidth=2.0)
    # plt.annotate('KEK', xy = (2, 2.2))
    plt.axis([-offx, day // 60, 0, dx + 1])
    plt.axis('off')
    plt.savefig('hist.png', bbox_inches = 'tight')

def getHistory(args, vk):
    makeChart(vk)
    vu = upl.VkUpload(vk)
    r = vu.photo_messages(photos = ['hist.png'])
    return {'attachment' : 'photo' + str(r[0]['owner_id']) + '_' + str(r[0]['id'])}