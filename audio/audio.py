import random

def getAudio(com, vk):
    offset = random.randint(1, 200)
    track = vk.method('audio.getPopular', {'offset' : offset, 'count' : 1})[0]
    attachment = 'audio{}_{}'.format(track['owner_id'], track['id'])
    return {'attachment' : attachment}