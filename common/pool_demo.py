# coding=utf-8
import sys
import base64
import requests
import json
import traceback
import os
from multiprocessing import Pool
import datetime
import ctypes
import urllib2
import time
import random

def run(code):
    pid = os.getpid()
    print pid,code
    time.sleep(2)

if __name__ == '__main__':
    print "start at:", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    pool = Pool(2)
    code_list = ['89898f44-1111-11e6-a735-0242ac117592',
                 '0a8ae110-1112-11e6-8fe6-0242ac117592', 
                 '8b6bbae4-1111-11e6-a216-0242ac117592',
                 '667c43c0-1111-11e6-8fe6-0242ac117592']
    def call_back(arg):
        print arg
        print "map_async complete. ok"
    chunksize = 1
    #以chunksize为个数单位，把任务发给workers. get(9999) 为ctl-c能kill掉所有worker
    #http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
    pool.map_async(run, code_list, chunksize, call_back).get(9999)   
    pool.close() #Prevents any more tasks from being submitted to the pool. Once all the tasks have been completed the worker processes will exit.
    pool.join()  #Wait for the worker processes to exit. One must call close() or terminate() before using join().
    print "end at:", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

