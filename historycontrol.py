import threading
import time
import fileparse as fp

historyLock = threading.Lock()
day = 24 * 60 * 60

with historyLock, open('days/lastupdate.txt') as f:
    last_update = int(f.readline())

def statusChange(upd):
    global last_update
    with historyLock:
        with open('history.txt', 'a') as f:
            print(*(upd + [round(time.time())]), file = f)
        now = round(time.time())
        newhist = []
        if now > last_update + day:
            l = dict()
            with open('history.txt') as f:
                for s in f:
                    s = s.split()
                    id = -int(s[1])
                    if id not in l:
                        l[id] = []
                    l[id].append(s)
            while now > last_update + day:
                curdname = time.strftime('%Y-%m-%d', time.localtime(last_update))
                fp.ensure_dir('days/' + curdname)
                for id in l:
                    with open('days/' + curdname + '/' + str(id) + '.txt', 'w') as f:
                        for el in l[id]:
                            if int(el[-1]) < last_update + day:
                                print(*el, file = f)
                last_update += day
            with open('history.txt', 'w') as f:
                for id in l:
                    for el in l[id]:
                        if int(el[-1]) >= now - day:
                            print(*el, file = f)
            with open('days/lastupdate.txt', 'w') as f:
                print(last_update, file = f)
