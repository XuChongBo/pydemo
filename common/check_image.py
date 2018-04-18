#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import string
import PIL
from PIL import Image
import traceback
import time

def boundRect(coordinates):
    n = len(coordinates)
    left = min(coordinates[0:n:2]) 
    right = max(coordinates[0:n:2]) 

    top = min(coordinates[1:n:2]) 
    bottom = max(coordinates[1:n:2]) 
    return max(0,left),max(0,top),right,bottom

def readFileListFromDescFile(root_dir):
    filepath = os.path.join(root_dir,  'Alignment.txt')
    import codecs
    result = []
    count = 0
    error = 0
    with codecs.open(filepath, "r", 'gbk') as myfile:
        for line in myfile:
            try:
                count += 1
                items = line.split()
                #print count, items
                coordinates = map(lambda x: int(string.atof(x)), items[1:])
                roi = boundRect(coordinates)
                result.append((os.path.join(root_dir,'EyesResolution', items[0]), roi))
                #result.append(line.encode('utf-8'))
#if count >= 100:
#break
            except Exception, e:
                print "Exception happens:", e
                print traceback.format_exc()
                print line
                error += 1
    print "read from ",filepath, "total:",len(result), "error:", error
    return result

def saveImage(path, img):
    data_dir = os.path.dirname(path)
    if not os.path.exists(data_dir):
	    os.makedirs(data_dir)
#cv2.imwrite(path, img)
    img.save(path)

def newPath(image_path):
    items = image_path.encode('ascii', errors='ignore').replace(' ','').split('/')
    prex = os.urandom(8).encode('hex')
    items[-1] = prex+'_'+items[-1]
    new_path = os.path.join(*items)
    return new_path


def process(pics):
        i = 0
        total = len(pics)
        error = 0
        for image_path, roi in pics:
            try:
                img = Image.open(image_path.encode('gbk'))
                crop = img.crop(roi)      #just copy out
                print 'ok' , image_path
                print  img.height,img.width, ' crop -> ', crop.height, crop.width
                print  "crop h/w:", crop.height*1.0/crop.width
                if image_path[-8:] == 'left.png':
                    base = 'left-crops'
                else:
                    base = 'right-crops'
                crop_path = os.path.join(base, *image_path.split('/')[1:])
                crop_path = newPath(crop_path)
                #crop_path = crop_path.replace(' ','')
                print crop_path
                saveImage(crop_path, crop) 
                print i, "/", total
                i += 1
            except Exception,e:
                print "Exception happens:", e
                print traceback.format_exc()
                error += 1
#time.sleep(1)
        print "total:", total, "error:", error

if __name__ == "__main__":
    pics = readFileListFromDescFile(sys.argv[1])
    raw_input('press any key to continue.')
    process(pics)

