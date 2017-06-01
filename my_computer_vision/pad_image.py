#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image, ImageEnhance
from pylab import imshow,show,axis,array,zeros
import sys
im = Image.open(sys.argv[1])
a4im = Image.new('RGB',
                      (im.width+20, im.height+30),   # A4 at 72dpi
                      (255, 255, 255))  # White

a4im.paste(im,(20,30))  # Not centered, top-left corner

#(595, 842),   # A4 at 72dpi
#a4im.paste(im, im.getbbox())  # Not centered, top-left corner
a4im.show()
