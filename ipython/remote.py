import subprocess
import socket, fcntl, struct
from IPython.display import Image
from IPython.display import display
from IPython.display import clear_output
from fabric.api import *
import time

env.host = '180.150.190.52:6' 
env.user = "xucb"
# env.password = 'www'


REMOTE_PATH = '/data/ocr/ocr_service/logs'

records = {}
def get_and_show(): 
    env.host = '180.150.190.52:6' 
    env.user = "xucb"
    while True:
        clear_output()    
        remote_filename = REMOTE_PATH+'/'+'ocr_20150902.log' 
        #local_filename  = LOCAL_PATH +'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        remote_ret = run(""" tail  -n10 %s | grep -E 'Downloading http|Return result' """ % remote_filename)
        lines =  remote_ret.split('\n');
        for line in lines:
            items = line.split()
            #print items        
            if len(items)>=13 and items[11]=="Downloading":
                process_id =  items[10]
                img_url = items[12]            
                #print img_url
                if (process_id in records) and records[process_id] != img_url:
                    print process_id,":", "Exception! does't complete it work."
                    display(Image(url=records[process_id]))    
                    records.pop(process_id);        
                records[process_id] = img_url
                continue            

            if len(items)>=15 and items[12]=="result:":
                process_id = items[10][:-1]
                ocr_result = " ".join(items[14:-1])
                if (process_id in records):
                    print process_id,":", ocr_result
                    display(Image(url=records[process_id]))    
                    records.pop(process_id);
                continue           
        print "processing:", records
        print "b"
        time.sleep(2)

get_and_show() 
