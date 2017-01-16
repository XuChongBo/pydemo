#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
filepath = "xx.txt"


###  handle chinese file path
descFilePath = os.path.join(config.UPLOAD_FOLDER, chinese_in_unicode, u"desc.txt")
print descFilePath, type(descFilePath)   
print descFilePath.encode("utf-8")
f  = open(descFilePath.encode("utf-8"), "r") 

##############

with codecs.open(filepath, "r", 'utf-8') as myfile:
    #line =  myfile.readline()
    #print len(line)
    #line = sorted(set(line))
    for line in myfile:
        with codecs.open("new.txt", "w", 'utf-8') as myfile:
            myfile.write(u"".join(line))


# def read_handwriting(filepath):
#     import codecs
#     with codecs.open(filepath, "r", 'utf-8') as myfile:
#         line =  myfile.readline()
#     print "read from ",filepath, "total:",len(line)
#     return line



