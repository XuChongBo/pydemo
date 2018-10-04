#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tqdm import tqdm
import time
print 
def test1():
    pbar = tqdm(total=100)

    for i in range(10):
        pbar.update(10)
        pbar.set_postfix_str('abc')
        time.sleep(0.1)
    pbar.close()


    for i in tqdm(range(20)):
        time.sleep(0.1)

    length = 100
    ll = range(length)  # just doing something random
    for r in tqdm(ll,desc="heheh", total=length, postfix="xxxx"):
        #print r
        pass

def test2():
    pbar1 = tqdm(total=100, position=1)
    pbar1.set_description('tttt')
    pbar2 = tqdm(total=200, position=0)
    for i in range(10):
        pbar1.update(10)
        pbar2.update(20)
        time.sleep(1)

test1()
