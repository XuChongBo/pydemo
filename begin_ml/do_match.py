#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    detect one dimension pattern on one dimension signal.
    1. detect method is  slide window.   scale=1, shift=1
    2. match method is the pattern template match.
"""

p=[12,35,58]
s=[12,35,58,12,35,12,35,58,9,12,35,58,1,12,35,12,23,35,58]

def find_p(p, s):
    """
    detect p in s.  no scale.  shift=1.
    template match is complete match.
    """
    i=0
    N=len(s)
    while i<N:
        #check begin at s[i]
        for j,elem in enumerate(p):
            k=i+j
            if k>=N:
                break
            if elem!=s[k]:
                break
            if j==len(p)-1:
                print 'found. begin at:',i
        i+=1


def find_p_almost(p, s, equal_factor=0.8):
    """
    detect p in s.  no scale.  shift=1.
    template match is complete match.  
    the equal_factor portion of the p  is treated to be matched.
    """
    i=0
    N=len(s)
    below_limit=len(p)*equal_factor
    print 'belowlimit:',below_limit
    while i<N:
        #check begin at s[i]
        cnt=0
        j=0
        while j<len(p):
            elem =p[j]
            k=i+j
            if k>=N:
                break
            if elem==s[k]:
                cnt+=1 
            j+=1
        if cnt>=below_limit:
            print 'found. begin at:',i
            i+=len(p)
        else:    
            i+=1


if __name__=="__main__":
    print p, s
    print p, zip(range(len(s)),s)
    find_p(p,s)
    find_p_almost(p,s,1)
    find_p_almost(p,s,0.5)
