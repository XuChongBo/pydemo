#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016-4-6

from fabric.api import run, local, lcd, env, task, cd, hosts, roles

"""
USAGE:
 fab -l 
 fab -H localhost,ocr1 test 
 fab hello:name=xx
 fab test2 -H 180.150.190.50:666
 fab test2 --host=180.150.190.50:666,180.150.190.52:666
 fab test2 hello -H 180.150.190.50:666
 fab test2 hello --host=180.150.190.50:666,180.150.190.52:666
 fab test2:hosts="180.150.190.52:666;180.150.190.50:666"
 fab hello:hosts="180.150.190.50:666" test2:hosts="180.150.190.52:666;180.150.190.50:666"
"""

def set_hosts():
    env.hosts = ['host1', 'host2']


env.roledefs.update({
    'webserver': ['xucb@180.150.190.50:666', 'localhost:666'],
    'dbserver': ['180.150.190.50:666']
})

@roles('webserver', 'dbserver')
@task
def test1():
    with lcd('/tmp'):
        local('ls')

@roles('dbserver')
@task
def test2():
    with lcd('/tmp'):
        local('ls')


@task
@hosts('180.150.190.52:666','180.150.190.50:666')
def test3():
    local('ls')
    run('pwd')

def doSomething():
    print "call internal func doSomething"
