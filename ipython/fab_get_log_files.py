#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import datetime
import traceback
import subprocess
import socket, fcntl, struct
from fabric.api import *

#env.hosts = ['10.166.138.151:36000']   #测试机
#env.hosts = ['172.27.180.119:36000']   #前台机
env.user = "cmcom"
env.password = 'cmcom@secu'

#目标机器上的运行目录
#REMOTE_PATH = '/data/cmcom/trunk/'
REMOTE_PATH = '/data/cmcom/running/'
LOCAL_PATH = '/data/cmcom/cmcom_data/'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s','eth1'[:15]))[20:24])



@task
def sync_sessionserverlog():
    try:
        APP_NAME = 'sessionserver'
        remote_filename = REMOTE_PATH+APP_NAME+'/log/'+'audit_logSessionServer.txt' 
        local_filename  = LOCAL_PATH +APP_NAME+'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        #取远程log文件的日期
        ret = run('head -n1 %s' % remote_filename)
        if not ret:  #空文件则取当天
            remote_datetime_indent = datetime.datetime.today().strftime('%Y-%m-%d')
        else:
            print ret
            remote_datetime_indent = ret.split()[0]


        #获取本地log文件的日期    
        ret = local('head -n1 %s' % local_filename, capture=True)
        if not ret: #空文件则取当天
            local_datetime_indent = datetime.datetime.today().strftime('%Y-%m-%d')
        else:
            print ret
            local_datetime_indent = ret.split()[0]
        print remote_datetime_indent, local_datetime_indent

        #若本地日期不等远程日期，则认为 远程log文件已回卷
        if (local_datetime_indent!=remote_datetime_indent):
            remote_filename += '.' + local_datetime_indent

        #读取远程log文件的尾部
        ret = local('wc -l  %s' % local_filename, capture=True)
        num = int(ret.split()[0]) + 1
        tmp_log_file = '~/tmp.sed.session.log'
        run(""" sed -n '%s,$p' %s > %s""" % (num, remote_filename, tmp_log_file))
        get( tmp_log_file,  tmp_log_file)
        local('cat %s >> %s' % (tmp_log_file, local_filename))
        #校验同步情况
        remote_ret = local(' wc -l %s' % local_filename, capture=True)
        line_num = remote_ret.split()[0]
        remote_ret = run(""" head -n %s  %s | md5sum """ % (line_num, remote_filename))
        local_ret = local(""" head -n %s  %s | md5sum """ % (line_num, local_filename), capture=True)
        print remote_ret
        print local_ret
        assert(remote_ret.split()[0]==local_ret.split()[0])

        print 'get %s from %s ok at %s' % (remote_filename,env.host,datetime.datetime.now())


        #若本地日期不等远程日期，则认为 远程log文件已回卷
        if (local_datetime_indent!=remote_datetime_indent):
            #比较两个文件
            FUNCTION_verify_two_files(remote_filename, local_filename)

            local_archivename  = LOCAL_PATH +APP_NAME+'_logs/'+'audit_logSessionServer.txt' + '.'+local_datetime_indent
            #追加到存档文件
            local('cat %s >> %s' % (local_filename, local_archivename))

            #校验归档中某部分机器内容
            FUNCTION_verify_sessionserver_achive(remote_filename, local_archivename)
            #清空
            local("""cat /dev/null > %s""" % local_filename)

            print 'complete %s from %s ok at %s' % (local_archivename,env.host,datetime.datetime.now())
    except:       
        traceback.print_exc()
        subprocess.check_call(['/data/cmcom/public_tools/sms.sh', 'marcchen','marcchen', "ERROR", "timestamp:%s;  msg: sync_sessionserverlog error; from:%s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),local_ip), '3'])


