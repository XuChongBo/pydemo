#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import numpy as np

a = np.array([10, 11, 12, 13, 14])
N = len(a)
print a
print "N:", N
for start_i in range(N):
    cyclic_idx = np.arange(start_i,start_i+N)%N
    print 'start at %s' % start_i
    print a[cyclic_idx]
