#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016 Feb 18 17:32 
"""
run "fab -l"  to show the tasks

usage:  

usage:
    fab image:build,version
    fab image:build
    fab image:push

    fab dev:start
    fab dev:stop

    fab -f fabfile.py dev:start
"""


from fabric.api import *
from fabric.colors import green, red, yellow, blue
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os


env.hosts = ['180.150.190.50:666']
env.user = "xucb"

def run_mkdir_safe(path, as_root=False):
    """
       local_mkdir_safe(path=DST_PROJECT_PATH)
    """
    mkdir_command = "mkdir -p {}".format(path)  # -p, --parents     no error if existing, make parent directories as needed
    if as_root:
        sudo(mkdir_command)
    else:
        run(mkdir_command)

def local_mkdir_safe(path, as_root=False):
    mkdir_command = "mkdir -p {}".format(path)  # -p, --parents     no error if existing, make parent directories as needed
    if as_root:
        sudo(mkdir_command)
    else:
        local(mkdir_command)



REPOSITORY = 'docker.zuoyetong.com.cn:8888/data_manager_webserver'
@task
def image(operation,tag="latest"):
    """
        fab image:build,1.2-20160318
    """
    if operation=="build":
        print green("============== build =============")
        local("docker build -t %s:%s ./webserver" % (REPOSITORY,tag))
        print green("============== check exists =============")
        local("docker images | grep '%s' " % REPOSITORY)
    elif operation=="push":
        local("docker push  %s " % REPOSITORY)  #push all tags of the repository



@task
def dev(operation):
    dev_compose_yml = 'dev-compose.yml'
    PROJECT_NAME = 'data_manager_dev'
    #目标机器上的运行目录
    print green("============== %s =============" % operation)
    local('pwd')
    if operation=="setup":
        dev("stop")
        dev("rm")
        dev("start")
    elif operation=="start":
        local('docker-compose -p %s -f %s up -d' % (PROJECT_NAME, dev_compose_yml))
    elif operation=="restart":
        local('docker-compose -p %s -f %s restart' % (PROJECT_NAME, dev_compose_yml))
    elif operation=="stop":
        local('docker-compose -p %s -f %s stop' % (PROJECT_NAME, dev_compose_yml))
    elif operation=="rm":
        local('docker-compose -p %s -f %s rm -f' % (PROJECT_NAME, dev_compose_yml))
    elif operation=="ps":
        local('docker-compose -p %s -f %s ps' % (PROJECT_NAME, dev_compose_yml))
    else: 
        print red("ERROR:  %s is not defined" % operation)
