#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016-4-6

from fabric.api import run, local, lcd, env, task, cd, hosts

"""
使用Fabric，你可以管理一系列host的SSH连接（包括主机名，用户，密码），定义一系列的任务函数，然后灵活的指定在哪些host上执行哪些任务。
除了这里演示的, Fabric还包括大量的功能，比如Role的定义，远程交互及异常处理，并发执行，文件操作等.
不局限于命令行方式，可以在你的应用中调用Fabric.
"""

"""
host参数优先级
1.单个任务，命令行主机列表(fab mytask:host=host1)会覆盖其他一切设置    
2.单个任务，装饰器指定主机列表 (@hosts('host1'))会覆盖 env 设置    
3.Fabfile 中全局 ENV 变量设置 (env.hosts = ['host1']) 会覆盖命令行全局指定主机列表    
4.命令行全局指定主机列表 (--hosts=host1)仅初始化 ENV 变量，在其他三种情况都没有设置的话，使用它指定的值。
"""

"""
host字符串采用这种格式：username@hostname:port
如果server密码不同，还可以在env.passwords中设置(host,password）对，为每个server设置单独的ssh密码。
env.hosts = ['180.150.190.50:666']
同密码一样时，你也可以在env.user中指定一个默认的用户。如果都没有指定，执行fab命令时会提示你输入密码。
env.user = "xucb"
"""

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

@task
def test1():
    with lcd('/tmp'):
        local('ls')

@task
def hello(name="world"):
    print("Hello %s!" % name)
    doSomething()


@task
def test2():
    with cd('/tmp'):
        run('ls')

@task
def test3():
    local('ls')
    run('pwd')

@task
@hosts('180.150.190.52:666','180.150.190.50:666')
def test4():
    local('ls')
    run('pwd')

def doSomething():
    print "call internal func doSomething"
