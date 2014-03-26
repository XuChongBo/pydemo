#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

a = [(3,5),(0,19),(1,1),(2,7),(7,0)]
print a

# sort from min to max.   It's non-inplace operation
b = sorted(a, key=lambda x:x[0])
print b


def myfun(x):
    return x[0]**2+x[1]**2
c = sorted(a, key=myfun)
print c 

# sort from max to min
d = sorted(a, key=myfun,reverse=True)
print d
