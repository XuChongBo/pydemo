#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import traceback
import time

def walk_dir(root_dir):
    root_dir = root_dir.rstrip("/")
    i = 0
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.png'):
                i += 1
                image_path = os.path.join(root, filename)
                print i, image_path
                try:
                    filename2 =  "%s.png" % i
                    new_path =  os.path.join(root, filename2)
                    print 'to', new_path
                    os.rename(image_path, new_path)
                except Exception,e:
                    print "Exception happens:", e
                    print traceback.format_exc()
                    time.sleep(2)

if __name__ == "__main__":
 walk_dir(sys.argv[1])
