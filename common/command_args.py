#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

if 3==len(sys.argv):
    a=sys.argv[1]
    b=sys.argv[2]
else:
    print "usage: %s <train|test> <days>" % __file__
    sys.exit(1)

print a,b
