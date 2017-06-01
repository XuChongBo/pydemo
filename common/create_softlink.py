#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import os

src = '/3T/images/girls'
dst = '/tmp/a.jpg'
# ln -s src  -dst
if not os.path.lexists(dst):
    os.symlink(src, dst)
    print "symlink created"
else:
    print "dst has exists ", dst

