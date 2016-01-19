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
        now = round(time.time())
        with open('history.txt', 'a') as f:
            print(*(upd + [now]), file = f)
        curdname = time.strftime('%Y-%m-%d', time.localtime(now))
        id = upd[3]
        fp.ensure_dir('days/' + curdname)
        with open('days/' + curdname + '/' + str(id) + '.txt', 'a') as f:
            print(*(upd + [now]), file = f)
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
            with open('history.txt', 'w') as f:
                for id in l:
                    for el in l[id]:
                        if int(el[-1]) >= now - day:
                            print(*el, file = f)
            with open('days/lastupdate.txt', 'w') as f:
                print(now, file = f)
