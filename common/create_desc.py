#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

def readFileListFromDir(root_dir, exts=['.jpg','.png']):
    result = []
    root_dir = root_dir.rstrip("/")
    i = 0
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            #if filename.endswith('.'+ext):
            if filename[-4:] in exts:
                i += 1
                image_path = os.path.join(root, filename)
                print i, image_path
                try:
                    #Image.open(image_path).save(savefilepath , "JPEG")
                    result.append(image_path)
                except Exception,e:
                    print "Exception happens:", e
                    print traceback.format_exc()
                    time.sleep(2)
    return result

if __name__ == "__main__":
    dir_path =  sys.argv[1]
    desc_path =  sys.argv[2]
    all_file_list = readFileListFromDir(dir_path)
    with open(desc_path, "w") as myfile:
        for line in all_file_list:
            try:
                myfile.write(line.encode('utf-8')+os.linesep)
            except:
                print "error"
                continue
            #myfile.write(line+os.linesep)

