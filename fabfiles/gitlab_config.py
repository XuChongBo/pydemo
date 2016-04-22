#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016-4-6

from fabric.api import run, local, lcd, env, task, cd, hosts,sudo,put

"""
USAGE:
 fab -l 
 fab -f gitlab_config.py  set_config -H hello@192.168.100.221:666
 host字符串采用这种格式：username@hostname:port
"""


@task
def set_config():
    DIR_PATH = "~/.ssh/"
    put('gitconfig.txt','%s/config' % DIR_PATH)
    run("ls  %s " % DIR_PATH)


@task
def put_id_rsa():
    DIR_PATH = "~/.ssh"
    run("ls  %s " % DIR_PATH)
    put('~/.ssh/id_rsa', DIR_PATH)
    run("chmod 600 %s/id_rsa " % DIR_PATH)
    run("ls  %s " % DIR_PATH)

