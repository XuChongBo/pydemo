#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import itertools


a=[3,4,7,4,5,2]

N = len(a)
K = 5
# len(a) choose k
# Elements are treated as unique based on their position, not on their value. So if the input elements are unique, there will be no repeat values in each combination.
coms = itertools.combinations(a, K)
coms_list = []
for c in coms:
    print c
    coms_list.append(c)

#print dir(coms), type(coms)

#coms[0]
#len(coms)

print len(coms_list)
print coms_list[0]
