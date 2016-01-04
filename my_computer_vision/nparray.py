#!/usr/bin/env python
# -*- coding:utf-8 -*-

#borrow from DIGITS

import sys
import os.path
import time
import argparse
import logging
import operator
from collections import Counter
import cv2
import numpy as np
from pylab import imshow,show,axis
import matplotlib.pyplot as plt
# must call digits.config.load_config() before caffe to set the path
from caffe.proto import caffe_pb2
import lmdb
from PIL import Image

import numpy as np

a = [[10,22,33,7],[1,2,3,7],[454,66,66,8],[454,66,66,7],[4,5,6,8]]
b = np.array(a)
print b
print b.shape
c =b[np.newaxis,:,:]
print c
print c.shape

d =b[:,np.newaxis,:]
print d
print d.shape

e = d.transpose((2,0,1)).copy()  #warning: transpose doesn't change the bytes position, so DO USE the copy()
print e
print e.shape


f = d[[2,1,0],...]
print f
print f.shape

        #     image = image.transpose((2,0,1))
        #     if image.shape[0] == 3:
        #         # channel swap
        #         # XXX see issue #59
        #         image = image[[2,1,0],...]
        # elif image.ndim == 2:
        #     # Add a channels axis
        #     


