#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from fabric.api import *
from fabric.colors import green, red, yellow, blue
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

"""
usage:  fab deploy  OR  fab -f fabfile.py deploy

"""

#env.hosts = ['10.166.138.153:36000', '10.177.151.158:36000']
env.hosts = ['120.132.59.209:666']
env.user = "xucb"
#env.password = 'cmcom@secu'

DEPLOY_PATH = '/data/xucb/'
PROJECT_NAME = 'hanzi_machine'
#目标机器上的运行目录
PROJECT_PATH = '%s%s' % (DEPLOY_PATH, PROJECT_NAME)
LOGS_PATH = '%s%s' % (DEPLOY_PATH, 'logs')
DATA_PATH = '%s%s' % (DEPLOY_PATH, 'data')


def mkdir_safe(path, as_root=False):
    mkdir_command = "mkdir {}".format(path)
    if not exists(path):
        if as_root:
            sudo(mkdir_command)
        else:
            run(mkdir_command)



# def rm(prefix=None, path=None):
#     rm_command = "rm -rf {}".format(path)
#     if exists(path):
#         if sudo:
#             sudo(rm_command)
#         else:
#             run(rm_command)
    

# 初始次发布
# def install():
#     """
#     处理proto协议，生成辅助代码
#     protoc --python_out=. session.proto
#     在脚本./produce_pb.sh 中

#     #阻止其它用户访问sessionserver
#     iptables -A INPUT -i eth1 -p tcp --destination-port 8091 -j DROP
#     """
#     #创建运行目录
#     if 'yes'==prompt('create sessionserver path %s ? ' % PROJECT_PATH, default='yes|skip', validate=r'(yes|skip)'):
#         run('mkdir %s' % PROJECT_PATH)
#     #创建sessionserver用户
#     if 'yes'==prompt('create db account?', default='yes|skip', validate=r'(yes|skip)'):
#         run("""mysql -uroot -e "GRANT SELECT ON cmcom_db.* TO 'sessionserver'@'%' identified by 'sessionserver@secu'; flush privileges;" """)
#     with cd(PROJECT_PATH):
#         #创建日志目录
#         if 'yes'==prompt('create logdir?', default='yes|skip', validate=r'(yes|skip)'):
#             run('mkdir ./log')
#      #把本地代码发布上去   
#     if 'yes'==prompt('upgrade sessionserver?', default='yes|skip', validate=r'(yes|skip)'):
#         upgrade()

image_name = 'docker.zuoyetong.com.cn:8888/hanzi_machine_appserver:1.0-20160201'
dev_compose_yml = 'dev-compose.yml'

def build():
    local("docker build -t  %s ./appserver" % image_name)
    local("docker images | grep appserver")

def start():
    local('docker-compose -f %s up -d' % dev_compose_yml)

def stop():
    local('docker-compose -f %s stop' % dev_compose_yml)

def restart():
    local('docker-compose -f %s restart' % dev_compose_yml)


# 更新文件，并重启
def deploy():
    """ 
    发布更新  目标机器153或158
    """


    # 创建部署文件夹
    mkdir_safe(path=PROJECT_PATH)
    mkdir_safe(path=LOGS_PATH)
    mkdir_safe(path=DATA_PATH)
    # 
    with cd(PROJECT_PATH):
        #打包本地代码,放到上层目录
        print green("Start to Deploy the Project")
        print green("="*40)
        print blue("do tar")
        print blue("*"*40)
        local('pxwd')
        local('tar -czf /tmp/%s.release.tgz  product-compose.yml nginx.conf   fabfile.py  readme.txt ' % PROJECT_NAME )
        #上传代码
        print blue("upload the tgz.")
        print blue("*"*40)
        put('/tmp/%s.release.tgz'%PROJECT_NAME, DEPLOY_PATH)

        #备份线上代码,放到上层目录
        run('pwd')
        run('tar -czf ../%s.last.tgz  ./'% PROJECT_NAME)

        #清除运行目录下的 all
        #if 'yes'==prompt('clean  %s ? ' % PROJECT_PATH, default='yes|skip', validate=r'(yes|skip)'):
        #   run('rm -rf *')

        #解压新代码
        run('tar -xf ../%s.release.tgz' % PROJECT_NAME)

        run(""" sed -i 's/LOCAL_MODE = True/LOCAL_MODE = False/g' config.py """)

        #重启server
        #run('./check_server.sh restart', pty=False)
        run('source ../bin/activate & supervisorctl  -c ../conf/upervisor.conf restart all', pty=False)
        #run('supervisorctl  -c ../conf/upervisor.conf restart all', pty=False)
