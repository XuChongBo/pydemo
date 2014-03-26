#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import datetime
import time

now_time = datetime.datetime.now()
print now_time


start_time = time.time()
time.sleep(2.6)
end_time = time.time()
print start_time
print end_time
print " cost:%s ms" % int((end_time-start_time)*1000)

