#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016 Feb 18 17:32 


"""
run "fab -l"  to show the tasks

usage:  
fab deploy:test   OR  fab -f fabfile.py deploy:test

usage:
fab deploy:product
fab deploy:test

fab image:build
fab image:push

fab dev:start
fab dev:stop

"""


from fabric.api import *
from fabric.colors import green, red, yellow, blue
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
import os

env.hosts = ['x.x.190.50:x']
env.user = "abc"
env.password = 'abc'






def run_mkdir_safe(path, as_root=False):
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

REPOSITORY = 'docker.zuoyetong.com.cn:8888/xucb/hanzi_machine_appserver'
@task
def image(operation,tag="latest"):
    """
        fab image:build,1.2-20160318
    """
    if operation=="build":
        print green("============== build =============")
        local("docker build -t %s:%s ./appserver" % (REPOSITORY,tag))
        print green("============== check exists =============")
        local("docker images | grep '%s' " % REPOSITORY)
    elif operation=="push":
        local("docker push  %s " % REPOSITORY)  #push all tags of the repository



@task
def dev(operation):
    dev_compose_yml = 'dev-compose.yml'
    PROJECT_NAME = 'hanzi_machine_dev'
    print green("============== %s =============" % operation)
    local('pwd')
    if operation=="setup":
        local_mkdir_safe(path='logs')
        local_mkdir_safe(path='data/stroke_images')
        local_mkdir_safe(path='data/unlabeled_stroke_images')
        dev("stop")
        dev("rm")
        dev("start")
        dev("reset_redis")
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
    elif operation=="reset_redis":
        local('docker exec hanzimachinedev_appserver_1  python /appserver/scripts/reset_data_in_redis.py /data/stroke_images/  /appserver/scripts/handwriting.txt')
    else: 
        print red("ERROR:  %s is not defined" % operation)

@task
def product(operation):
    PROJECT_NAME = 'hanzi_machine_product'
    #目标机器上的运行目录
    DST_PROJECT_PATH = "/home/xucb/"+PROJECT_NAME
    LOGS_PATH = os.path.join(DST_PROJECT_PATH, 'logs')
    LABELED_DATASET_PATH = os.path.join(DST_PROJECT_PATH, 'data/stroke_images')
    UNLABELED_DATASET_PATH = os.path.join(DST_PROJECT_PATH, 'data/unlabeled_stroke_images')
    print green("============== %s =============" % operation)
    if operation=="setup":
        # 创建部署文件夹
        print green("============== 1. mkdir -p in remote host =============")
        run_mkdir_safe(path=DST_PROJECT_PATH)
        run_mkdir_safe(path=LOGS_PATH)
        run_mkdir_safe(path=LABELED_DATASET_PATH)
        run_mkdir_safe(path=UNLABELED_DATASET_PATH)
        with cd(DST_PROJECT_PATH):
            run('pwd')
            print green("============== 2. upload files to remote host =============")
            put('./product-compose.yml', os.path.join(DST_PROJECT_PATH, "docker-compose.yml"))
            put('./nginx.conf', DST_PROJECT_PATH)


            print green("============== 3. run docker things =============")
            run('docker pull %s' % REPOSITORY)
            #run('supervisorctl  -c ../conf/upervisor.conf restart all', pty=False)
            product("stop")
            product("rm")
            product("start")
            product("reset_redis")
    else:
        with cd(DST_PROJECT_PATH):
            if operation=="start":
                run('docker-compose  up -d', pty=False)
            elif operation=="restart":
                run('docker-compose  restart', pty=False)
            elif operation=="stop":
                run('docker-compose  stop', pty=False)
            elif operation=="rm":
                run('docker-compose  rm -f', pty=False)
            elif operation=="ps":
                run('docker-compose ps', pty=False)
            elif operation=="reset_redis":
                run('docker exec hanzimachineproduct_appserver_1  python /appserver/scripts/reset_data_in_redis.py /data/stroke_images/  /appserver/scripts/handwriting.txt')
            else: 
                print red("ERROR:  %s is not defined" % operation)
@task
def test(operation):
    PROJECT_NAME = 'hanzi_machine_test'
    #目标机器上的运行目录
    DST_PROJECT_PATH = "/tmp/"+PROJECT_NAME
    LOGS_PATH = os.path.join(DST_PROJECT_PATH, 'logs')
    LABELED_DATASET_PATH = os.path.join(DST_PROJECT_PATH, 'data/stroke_images')
    UNLABELED_DATASET_PATH = os.path.join(DST_PROJECT_PATH, 'data/unlabeled_stroke_images')
    print green("============== %s =============" % operation)
    if operation=="setup":
        # 创建部署文件夹
        local_mkdir_safe(path=DST_PROJECT_PATH)
        local_mkdir_safe(path=LOGS_PATH)
        local_mkdir_safe(path=LABELED_DATASET_PATH)
        local_mkdir_safe(path=UNLABELED_DATASET_PATH)
        local('pwd')
        local('cp ./test-compose.yml %s ' % os.path.join(DST_PROJECT_PATH, "docker-compose.yml"))
        local('cp ./nginx.conf  %s ' % DST_PROJECT_PATH)
        # #local('supervisorctl  -c ../conf/upervisor.conf restart all', pty=False)
        with lcd(DST_PROJECT_PATH):
            test("stop")
            test("rm")
            test("start")
            test("reset_redis")
    else:
        with lcd(DST_PROJECT_PATH):
            if operation=="start":
                local('docker-compose up -d')
            elif operation=="restart":
                local('docker-compose  restart')
            elif operation=="stop":
                local('docker-compose  stop')
            elif operation=="rm":
                local('docker-compose  rm -f')
            elif operation=="ps":
                local('docker-compose ps')
            elif operation=="reset_redis":
                local('docker exec hanzimachinetest_appserver_1  python /appserver/scripts/reset_data_in_redis.py /data/stroke_images/  /appserver/scripts/handwriting.txt')
            else: 
                print red("ERROR:  %s is not defined" % operation)
