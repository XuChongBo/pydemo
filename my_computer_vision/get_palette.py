# -*- coding: utf-8 -*-
# First you need to import the libraries in question.
# borrow from blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
import numpy as np
import cv2
import sys
from PIL import Image, ImageDraw
from pylab import imshow,show,axis

# For gray image
img = Image.open(sys.argv[1])
p = img.getpalette()
#for r, g, b in p:
#    print r, g, b
print img
print len(p)/3
