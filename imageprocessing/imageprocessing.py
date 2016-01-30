from PIL import Image
from constants import getAttachments
from urllib.request import *
from vk_api.vk_upload import *

imgbuf = "imageprocessing/"

def shakalize(imgpath, deg):
    im = Image.open(imgpath)
    x, y = im.size
    im.resize((x // 3, y // 3)).save(imgbuf + "shakalized.jpg", quality = 10 - deg)
    return imgbuf + "shakalized.jpg"

def getShakalized(com, vk):
    photos = getAttachments(com.misc, 'photo')
    if len(photos) == 0:
        return {'attachment' : 'photo325483887_402170372'}
    if len(com.args) == 1:
        deg = 5
    elif len(com.args) == 2:
        try:
            deg = int(com.args[1])
            if deg <= 0 or deg > 9:
                raise Exception('deg out of range')
        except:
            return {'attachment' : 'photo325483887_402170372'}
    else:
        return {'attachment' : 'photo325483887_402170372'}
    r = vk.method('photos.getById', {'photos': str(photos[0][0]) + '_' + str(photos[0][1]), 'photo_sizes': 1})
    for sz in r[0]['sizes']:
        if sz['type'] == 'x':
            src = sz['src']
    img = urlopen(src)
    with open(imgbuf + 'buf.jpg', 'wb') as f:
        f.write(img.read())
    pth = shakalize(imgbuf + 'buf.jpg', 10 - deg)
    vu = VkUpload(vk)
    r = vu.photo_messages(pth)
    return {'attachment' : 'photo' + str(r[0]['owner_id']) + '_' + str(r[0]['id'])}