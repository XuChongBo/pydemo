import subprocess
import socket, fcntl, struct
from fabric.api import *
from fabric.api import env 
import time

env.user = "xucb"
env.hosts = ['180.150.190.52:666'] 
# env.password = 'www'


REMOTE_PATH = '/data/ocr/ocr_service/logs'

records = {}
def get_and_show(): 
    env.host = '180.150.190.52:6' 
    env.user = "xucb"
    while True:
        remote_filename = REMOTE_PATH+'/'+'ocr_20150902.log' 
        #local_filename  = LOCAL_PATH +'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        remote_ret = run(""" tail  -n10 %s | grep -E 'Downloading http|Return result' """ % remote_filename)
        lines =  remote_ret.split('\n');
        for line in lines:
            items = line.split()
            print items        
        time.sleep(5)
