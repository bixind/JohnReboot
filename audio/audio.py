import random
from audio.genres import *

def getAudio(com, vk):
    offset = random.randint(1, 100)
    values = {'offset' : offset, 'count' : 3}
    genre = None
    for val in com.args:
        ps = val.split('_')
        if len(ps) > 1 and 'жанр' == ps[0]:
            genre = genres.get(ps[1], None)
    if genre is not None:
        values['genre_id'] = genre
    resp = vk.method('audio.getPopular', values)
    track = resp[0]
    attachment = 'audio{}_{}'.format(track['owner_id'], track['id'])
    return {'attachment' : attachment}
