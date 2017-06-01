#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import traceback

def walk_dir(root_dir):
    root_dir = root_dir.rstrip("/")
    i = 0
    ext = '.png'
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(ext):
                i += 1
                image_path = os.path.join(root, filename).decode('utf8')
                print i, image_path
                items = image_path.encode('ascii', errors='ignore').replace(' ','').split('/')
                prex = os.urandom(8).encode('hex')
                items[-1] = prex+'_'+items[-1]
                new_path = os.path.join(*items)
                try:
                    print 'to', new_path
                    os.rename(image_path, new_path)
                except Exception,e:
                    print "Exception happens:", e
                    print traceback.format_exc()
                    time.sleep(2)

if __name__ == "__main__":
 walk_dir(sys.argv[1])
