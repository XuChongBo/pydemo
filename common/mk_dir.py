#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil

##################################
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

##########################################################
import os
data_dir = './a/b/c'
if not os.path.exists(data_dir):
	os.makedirs(data_dir)


