# coding=utf-8
import sys
import base64
import requests
import json
import traceback
import os
from multiprocessing import Pool, Value
import datetime
import ctypes
import urllib2
import time
import random


is_running = Value(ctypes.c_bool,True)
reload(sys)
sys.setdefaultencoding('utf-8')

# product
LOGIN_URL = "http://nuwa-dev.zuoyetong.com.cn/api/account/login"
DOWNLOAD_URL = "http://nuwa-dev.zuoyetong.com.cn/api/resource/download"

def get_token():
    data = {'username':'admin', 'password':'xxx'}
    headers={'content-type': 'application/json'}
    resp = requests.post(LOGIN_URL, headers=headers, data=json.dumps(data))
    print resp
    print resp.content
    assert(resp.status_code==200)
    return json.loads(resp.content)['token']
# def get_token():
#     TOKEN_URL = "http://tiku-upload.zuoyetong.com.cn/resource/token/"
#     data = {"username": "abc", "password": "abc"}
#     resp = requests.post(TOKEN_URL, data=data)
#     if resp.status_code == 200:
#         return json.loads(resp.content)['token']
#     return None
TOKEN = get_token()

class NeedAuthException(Exception):
    pass

def check_authorization(func):
    def wrapper(*args):
        count = 0
        while count < 2:
            try:
                return func(*args)
            except NeedAuthException:
                global TOKEN
                TOKEN = get_token()
            finally:
                count += 1
    return wrapper

def download_url_1(code, cookies):
    pid = os.getpid()
    #req = urllib2.Request(DOWNLOAD_URL+'?code='+code)
    req = urllib2.Request(code)
    #req.add_header('Content-Type','application/json')
    req.add_header('Cookie', 'nuwa_token='+cookies['nuwa_token'])
    print "[%s %s] read begin." % (pid, datetime.datetime.now())
    data = urllib2.urlopen(req).read()
    filename = '%s.doc' % pid
    print "[%s %s] read end." % (pid, datetime.datetime.now())
    with open(filename, "wb") as fd:
        fd.write(data)

def download_url(url):
    pid = os.getpid()
    code = 'x'
    resp = requests.get(url, timeout=2)
    filename = '%s.doc' % pid
    chunk_size = 1024*10
    print '[%s %s] downloading: %s' % (pid, datetime.datetime.now(), code)
    s = '-'
    with open(filename, 'wb') as fd:
        for chunk in resp.iter_content(chunk_size):
            print '[%s %s] %s %s' % (pid, datetime.datetime.now(), code, s)
            fd.write(chunk)
            time.sleep(5*random.random())
            s+='-'
    print '[%s %s] finish: %s' % (pid, datetime.datetime.now(), code)

@check_authorization
def download_resource(code):
    global is_running
    pid = os.getpid()
    cookies = {"nuwa_token": TOKEN}
    print '[%s] get: %s' % (pid, code)
    resp = requests.get(DOWNLOAD_URL, cookies=cookies, params={'code': code}, timeout=2)
    code = code[0:8]
    filename = code+'.doc'
    chunk_size = 1024*10
    print '[%s] downloading: %s' % (pid, code)
    s = '-'
    with open(filename, 'wb') as fd:
        for chunk in resp.iter_content(chunk_size):
            print '[%s %s] %s %s' % (pid, datetime.datetime.now(), code, s)
            sys.stdout.flush()
            fd.write(chunk)
            #time.sleep(5*random.random())
            s+='-'
    #download_url_1(code, cookies)
    print '[%s] finish: %s' % (pid, code)
    
def run(code):
    global is_running
    try:
        download_resource(code)
        #download_url(code)
    except Exception, e:
        traceback.print_exc()  
        print "xxxxxx"
        is_running.value = False
        raise e
    
    


if __name__ == '__main__':
    print "start at:", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    pool = Pool(2)
    code_list = ['89898f44-1111-11e6-a735-0242ac117592',
                 '0a8ae110-1112-11e6-8fe6-0242ac117592', 
                 '8b6bbae4-1111-11e6-a216-0242ac117592',
                 '667c43c0-1111-11e6-8fe6-0242ac117592']
    url_list = ['http://tiku-upload.zuoyetong.com.cn/media/section/document/14/72/a4/7250bbd26c556d0cb84d9a92fe5a5da4.doc',
                'http://tiku-upload.zuoyetong.com.cn/media/section/document/14/3b/d2/3b4fdb49e196a7783135283b3d25fbd2.doc',
                'http://tiku-upload.zuoyetong.com.cn/media/section/document/14/86/d3/860d7b88e0ff39bab5c51e46e950b9d3.doc']
    pool.map(run, code_list)
    while True:
        if not is_running.value:
            time.sleep(0.1)
            break
        pass

    pool.close()
    pool.join()
    print "end at:", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# from multiprocessing import Pool, Value, Lock
# import ctypes
# import urllib
# import httplib2

# from suds.client import Client
# import logging 
# import threading
# import datetime
# import time
# import json
# import random
# import sys
# import os

# is_running = Value(ctypes.c_bool,True)



# def DoLogin(task_id):
#     global is_running
#     pid = 'do login. pid:%s, task_id:%s' % (os.getpid(), task_id)
#     print pid
#     try:
#         if not is_running.value:
#             #print 'over.'
#             return
#         #不断访问
#         for i in range(10000):
#             if not is_running.value:
#                 return

#             #break
#             time.sleep(5*random.random())
#             #time.sleep(100*random.random())
#     except:
#         #output_str += '\n%s' %  ('time:' % datetime.datetime.now())
#         print
#         print pid, 'end error'
#         is_running.value = False
#         raise



# if __name__ == '__main__':
#     """
#     if len(sys.argv) !=3:
#         print "usage: cmd <user_name>"
#         sys.exit(1)
#     """    

    # auth_pool = Pool(N)
    # for i in range(N):
    #     result = auth_pool.apply_async(DoLogin, args=(i,))
    # auth_pool.close()



    #login_pool.join()
    #auth_pool.join()


