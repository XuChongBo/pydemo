#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

def walk_dir(root_dir):
    i = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.gif'):
                i += 1
                image_path = os.path.join(root, file)
                print i, image_path
                try:
                    #Image.open(image_path).save(savefilepath , "JPEG")
                    txt = process(image_path)
                except Exception,e:
                    print "Exception happens:", e
                    print traceback.format_exc()
                    time.sleep(2)


