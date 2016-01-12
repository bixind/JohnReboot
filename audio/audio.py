import random

def getAudio(com, vk):
    offset = random.randint(1, 200)
    resp = vk.method('audio.getPopular', {'offset' : offset, 'count' : 1})
    print(resp)
    track = resp[0]
    attachment = 'audio{}_{}'.format(track['owner_id'], track['id'])
    return {'attachment' : attachment}