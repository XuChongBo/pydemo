#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil

def mkdir(path, clean=False):
    """
    Safely create a directory
    Arguments:
        path -- the directory name
    Keyword arguments:
        clean -- if True and the directory already exists, it will be deleted and recreated
    """
    if os.path.exists(path):
        if clean:
            shutil.rmtree(path)
        else:
            return
    os.mkdir(path)


# def read_handwriting(filepath):
#     import codecs
#     with codecs.open(filepath, "r", 'utf-8') as myfile:
#         line =  myfile.readline()
#     print "read from ",filepath, "total:",len(line)
#     return line

#def data_list_desc(dirpath):


