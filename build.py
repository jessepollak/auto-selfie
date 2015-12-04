import os
import urllib
import subprocess
import cStringIO
import concurrent.futures
from itertools import izip_longest
import time

from PIL import Image, ImageDraw, ImageFont

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def get_coords(basepath):
    out = subprocess.check_output(
        "exiftool -n -GPSLatitude -GPSLongitude {0}/*.jpg | cut -d ':' -f 2 | tr -d ' '".format(basepath),
        shell=True
    )
    items = {}
    for item in out.split("========")[:-1]:
        lines = item.split()
        if len(lines) > 1:
            coords = [str(round(float(f), 4)) for f in lines[1:]]
            items[lines[0]] = ','.join(coords)
    return items


def get_gmaps(coords):
    url = "https://maps.googleapis.com/maps/api/staticmap"
    gmaps = {}
    for jpg, coord in coords.iteritems():
        payload = {
            'center': coord,
            'zoom': 12,
            'markers': coord,
            'key': "AIzaSyCpbbt20uA1MqAqikMvYeqRAsNMOOx0Ey0",
            'size': "300x300"
        }
        gmaps[jpg] = url + '?' + urllib.urlencode(payload)
    return gmaps

basepath = "/Users/jhunt3/Dropbox/Apps/whereapp/auto-selfie"
coords = get_coords(basepath)
gmaps = get_gmaps(coords)


def build_new_img(grp):
    for img, gmap in grp:
        base_img = Image.open(img)
        img_name = os.path.basename(img).strip(".jpg")
        img_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(img_name)))
        f = cStringIO.StringIO(urllib.urlopen(gmap).read())
        im = Image.open(f)
        base_img.paste(im, (0, 0))
        d = ImageDraw.Draw(base_img)
        fnt = ImageFont.truetype("/Users/jhunt3/dev/fonts/LiberationMono/Literation Mono Powerline Bold Italic.ttf", 40)
        d.text((820, 680), img_time, font=fnt, fill=(255, 255, 255))
        base_img.save(os.path.join(basepath, "gmap-img/", os.path.basename(img)))

executor = concurrent.futures.ProcessPoolExecutor(10)
futures = [executor.submit(build_new_img, group) for group in grouper(gmaps.iteritems(), 20)]
concurrent.futures.wait(futures)
