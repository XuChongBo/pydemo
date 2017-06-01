# -*- coding: utf-8 -*-
# First you need to import the libraries in question.
# borrow from blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
import numpy as np
import cv2
import sys
from PIL import Image, ImageDraw
from pylab import imshow,show,axis

im = Image.new("P", (400, 400), 0)

im.putpalette([
0, 0, 0, # black background
255, 0, 0, # index 1 is red
255, 255, 0, # index 2 is yellow
255, 153, 0, # index 3 is orange
])

im.paste(1, box=[100,100,200,200])
im.paste(1, box=[100,100,200,200])

im.save('/3T/images/tt.png');

d = ImageDraw.ImageDraw(im)
d.setfill(1)

d.setink(1)
d.polygon((0, 0, 0, 400, 400, 400))

d.setink(3)
d.rectangle((100, 100, 300, 300))

d.setink(2)
d.ellipse((120, 120, 280, 280))

# For gray image
img = Image.open(sys.argv[1])
imgcv = np.asarray(img.convert('L'))
imshow(img)
show()


cv2.imshow('Demo gray Image',imgcv)
cv2.waitKey(0)
