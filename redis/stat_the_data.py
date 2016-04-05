#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import redis

r = redis.StrictRedis(host='localhost', port= 6379, db=0)

total = 0

def read_handwriting(filepath):
    import codecs
    with codecs.open(filepath, "r", 'utf-8') as myfile:
        line =  myfile.readline()
    print "read from ",filepath, "total:",len(line)
    return line

def write_hanzi_list():
    hanzi_list = read_handwriting("./handwriting.txt")
    print hanzi_list
    for idx,tag in enumerate(hanzi_list):
        print idx, tag.encode('utf-8')
        r.rpush('hanzi_list',tag.encode('utf-8'))

def read_hanzi_list():
    hanzi_list = r.lrange("hanzi_list", 0, -1)
    print hanzi_list
    for  ch in hanzi_list:
        print ch
    print "total:", len(hanzi_list)

def paths_of_key(hanzi):
    global total
    path_list = r.lrange(hanzi, 0, -1)
    #for path in path_list: 
    #    print path
    count = len(path_list)
    total += count
    #print "count:", count 
    print hanzi, count 

def print_all_key():
    keys = r.keys("*")
    for k in keys:
        #print k
        if k=="hanzi_list":
            continue
	paths_of_key(k)

if __name__ == "__main__":
    #read_hanzi_list()
    print_all_key()
    #write_hanzi_list()
    print "total:",total



