#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import datetime
import traceback
import subprocess
import socket, fcntl, struct
from fabric.api import *

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

        local("""ls""");
        run(""" tail  -n50 %s """ % remote_filename);


        # #获取本地log文件的日期    
        # ret = local('head -n1 %s' % local_filename, capture=True)
        # if not ret: #空文件则取当天
        #     local_datetime_indent = datetime.datetime.today().strftime('%Y-%m-%d')
        # else:
        #     print ret
        #     local_datetime_indent = ret.split()[0]
        # print remote_datetime_indent, local_datetime_indent

        # #若本地日期不等远程日期，则认为 远程log文件已回卷
        # if (local_datetime_indent!=remote_datetime_indent):
        #     remote_filename += '.' + local_datetime_indent

        # #读取远程log文件的尾部
        # ret = local('wc -l  %s' % local_filename, capture=True)
        # num = int(ret.split()[0]) + 1
        # tmp_log_file = '~/tmp.sed.session.log'
        # run(""" sed -n '%s,$p' %s > %s""" % (num, remote_filename, tmp_log_file))
        # get( tmp_log_file,  tmp_log_file)
        # local('cat %s >> %s' % (tmp_log_file, local_filename))
        # #校验同步情况
        # remote_ret = local(' wc -l %s' % local_filename, capture=True)
        # line_num = remote_ret.split()[0]
        # remote_ret = run(""" head -n %s  %s | md5sum """ % (line_num, remote_filename))
        # local_ret = local(""" head -n %s  %s | md5sum """ % (line_num, local_filename), capture=True)
        # print remote_ret


        # print 'get %s from %s ok at %s' % (remote_filename,env.host,datetime.datetime.now())


        #     local_archivename  = LOCAL_PATH +APP_NAME+'_logs/'+'audit_logSessionServer.txt' + '.'+local_datetime_indent
        #     #追加到存档文件
        #     local('cat %s >> %s' % (local_filename, local_archivename))

        #     #清空
        #     local("""cat /dev/null > %s""" % local_filename)

        #     print 'complete %s from %s ok at %s' % (local_archivename,env.host,datetime.datetime.now())
    except:       
        traceback.print_exc()
        


