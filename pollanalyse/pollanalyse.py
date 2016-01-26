# -*- coding: utf-8 -*-

def pollResults(vk, attch):
    summary = []
    summary.append('Опрос: ' + str(attch['question']))
    summary.append('Проголосовало: ' + str(attch['votes']))
    summary.append('Варианты:')
    for ans in attch['answers']:
        summary.append(str(ans['text']) + ': ' + str(ans['votes']) + ', ' + str(ans['rate']) + '%')
    return "\n".join(summary)

def pollsParse(vk, walls):
    res = []
    r = vk.method('wall.getById', {'posts' : ",".join(walls)})
    for post in r:
        if 'attachments' in post:
            for attch in post['attachments']:
                if attch['type'] == 'poll':
                    res.append(pollResults(vk, attch['poll']))
    return "\n".join(res)

def getPollInfo(com, vk):
    attch = com.misc
    i = 1
    resmssg = ''
    walls = []
    while 'attach' + str(i) in attch:
        if attch['attach' + str(i) + '_type'] == 'wall':
            walls.append(attch['attach' + str(i)])
        i += 1
    resmssg = pollsParse(vk, walls)
    if resmssg == '':
        resmssg = 'Beatae plane aures, quae non vocem foris sonantem, sed intus auscultant veritatem docentem'
    return {'message' : resmssg}