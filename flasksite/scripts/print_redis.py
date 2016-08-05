#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import redis

r = redis.StrictRedis(host='redis', port= 6379, db=0)

total = 0

def print_hanzi_list():
    hanzi_list = r.lrange("hanzi_list", 0, -1)
    print hanzi_list
    for  ch in hanzi_list:
        print ch
    print "total:", len(hanzi_list)


def print_all_key():
    keys = r.keys("*")
    global total
    for k in keys:
        print k
        if "_count" in k:
            print k, r.get(k)
        else:
            count = len(r.lrange(k, 0, -1))
            print k, count
            total += count

if __name__ == "__main__":
    #print_hanzi_list()
    print_all_key()
    print total



