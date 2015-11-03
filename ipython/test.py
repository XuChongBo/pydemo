#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import datetime
import traceback
import subprocess
import socket, fcntl, struct
from fabric.api import *
import time
from IPython.display import Image
from IPython.display import display


#env.hosts = ['10.166.138.151:36000']   #测试机
env.hosts = ['180.150.190.52:666']   #前台机
env.user = "xucb"
env.password = '313845681@www'

#目标机器上的运行目录
#REMOTE_PATH = '/data/cmcom/trunk/'
REMOTE_PATH = '/data/ocr/ocr_service/logs'
LOCAL_PATH = '/data/cmcom/cmcom_data/'



@task
def check():
    env.hosts = ['180.150.190.52:666']   #前台机
    env.user = "xucb"
    env.password = '313845681@www'
    try:
        remote_filename = REMOTE_PATH+'/'+'ocr_20150902.log' 
        #local_filename  = LOCAL_PATH +'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        remote_ret = run(""" tail  -n6 %s | grep -E 'Downloading http|Return result' """ % remote_filename)
        lines =  remote_ret.split('\n');
        for line in lines:
            items = line.split()
            #print items
            if len(items)>=13 and items[11]=="Downloading":
                img_url = items[12]            
                #print img_url
                id =  items[10]
                #print id
                continue            
            if len(items)>=15 and items[12]=="result:":
                print items[10], "".join(items[14:-1])
                #print id
                if id+':' == items[10]:
                    display(Image(url=img_url))
                continue   

    except:       
        traceback.print_exc()
        


