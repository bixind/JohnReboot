import random

def getAudio(com, vk):
    offset = random.randint(1, 100)
    resp = vk.method('audio.getPopular', {'offset' : offset, 'count' : 3})
    track = resp[0]
    print(resp[0])
    attachment = 'audio{}_{}'.format(track['owner_id'], track['id'])
    return {'attachment' : attachment}
