#!/usr/bin/python
import random
import os
import sys
"""
    produce the samples 
"""
print 'ok'
print random.random()


def target_fun(x): 
    return 2*x+1

def draw_one_sample():
    a=1000000*random.random()       #[0,1000000]
    return (a, target_fun(a))

def draw_one_sample_set(index_num):
    n=1000
    try:
        x_file = open('./data/data%s.x'%index_num, 'w')
        y_file = open('./data/data%s.y'%index_num, 'w')
        while n>0:  
            n-=1
            one_sample=draw_one_sample()
            x_file.writelines('%s ' % (one_sample[0]) + os.linesep)
            y_file.writelines('%s ' % (one_sample[1]) + os.linesep)
    finally:
        if x_file:
            x_file.close()
        if y_file:
            y_file.close()

if __name__ == '__main__':
    print target_fun(3)
    print draw_one_sample()
    draw_one_sample_set(2)
    if len(sys.argv)!=2: 
        print 'usage: ./xx.py index_num'
        exit(1)
    draw_one_sample_set(sys.argv[1])
    print '+++++++ end +++++++++'
