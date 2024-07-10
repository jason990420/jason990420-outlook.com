from os import listdir, stat
from os.path import isfile, isdir, join
from PIL import Image

p = 'PNG_before\\'
n = 'PNG_After\\'

all = listdir(p)

for file in all:
    if file[-4:] == '.png':
        im = Image.open(p+file)
        im = im.resize((600, 300), resample=Image.LANCZOS)
        im.save(n+file)
