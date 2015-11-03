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
import ocr

        n+=1
        if n<500:
            continue
        datum = caffe_pb2.Datum()
        datum.ParseFromString(value)

        shape = '%sx%sx%s' % (datum.width, datum.height, datum.channels)
        print shape
        # Read the datum.data
        img_data = np.array(bytearray(datum.data)).reshape(datum.channels, datum.height, datum.width)
        visualize = False
        #NOTE: do copy() to make sure the strides OK for c++ interface
        img_data = img_data.transpose([1,2,0]).copy()


        if visualize:
            plt.imshow(img_data)
            plt.show()

        import ocr
        filename = "/home/xucb/data/ocr_test_set/test_math.png"
        model_dir =  "/home/xucb/projects/OCR/tw_ocr/models"
        #result = ocr.recognize_by_image_path(filename, model_dir)
        #print result


        import cv2
        img = cv2.imread(filename)
        #imshow(img)
        #show()
        print type(img),img.shape, img.size, img.ndim, img.dtype, img.itemsize, img.strides
        #print ocr.recognize_by_cvmat(img, model_dir)


        #cv2.imshow("xx",img_data)
        print type(img_data), img_data.shape, img_data.size, img_data.ndim, img_data.dtype, img_data.itemsize, img_data.strides
        result = ocr.recognize_by_cvmat(img_data, model_dir)
        #cv2.waitKey(-1)

        print key, result


