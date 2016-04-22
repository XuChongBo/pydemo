#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016-4-6

from fabric.api import run, local, lcd, env, task, cd, hosts,sudo,put

"""
USAGE:
 fab -l 
 fab -f docker_registy.py  set_crt -H hello@192.168.100.221:666
 host字符串采用这种格式：username@hostname:port
"""


@task
def set_crt():
    DIR_PATH = "/etc/docker/certs.d/docker.zuoyetong.com.cn:8888/"
    sudo("mkdir -p %s" % DIR_PATH)
    put('ca.crt','/tmp/')
    sudo("mv /tmp/ca.crt  %s " % DIR_PATH)
    sudo("ls  %s " % DIR_PATH)

