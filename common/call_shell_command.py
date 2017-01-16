#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess

def simple():
    return_code = subprocess.call("ls -a", shell=True)  
    #ret = subprocess.call("ls -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    print return_code

def reload_data():
    cmd = 'python /code/scripts/reset_data_in_redis.py'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  

    if sync_block:  # 等命令执行完
        for line in p.stdout.readlines():  
            app.logger.info(line)
        p.wait()  
        if p.returncode != 0:
            app.logger.error("return code: %s" % p.returncode)
            raise Exception('callCommand error. cmd: '+cmd)
    else:          # 不等命令执行完
        pass
        # 直接退出会把子程序也退出

import subprocess, shlex
from threading import Timer

def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def call_back(p):
        print "timeout happens. to kill subprocess"
        p.kill()

    # 处理单个子进程时
    timer = Timer(timeout_sec, call_back, [proc])   # 原理是开一个线程进行sleep,  醒来查看主线程是否有设置某个事件, 没有则执行call_back.  
    #NOTE: 实际使用时会有很多timer线程在sleep. 因为主线程 做了一轮有一轮的任务, 每一轮的计时器线程都要sleep到时间后才能释放子线程.

    try:
        timer.start()
        stdout,stderr = proc.communicate()
        print "stdout:", stdout
        print "stderr:", stderr
    finally:
        timer.cancel()

if __name__ == "__main__":
    simple() 
#run("wget google.com", 3)
#run("wget baidu.com", 3)
