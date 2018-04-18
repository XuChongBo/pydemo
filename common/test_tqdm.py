#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tqdm import tqdm
import time
for i in tqdm(range(20)):
    time.sleep(0.1)

length = 100
ll = range(length)  # just doing something random
for r in tqdm(ll, total=length):
    print r
    pass
