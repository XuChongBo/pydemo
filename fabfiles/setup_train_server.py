#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: XuChongBo
# Created: 2016-4-6

from fabric.api import run, local, lcd, env, task, cd, hosts,sudo,put

"""
USAGE:
 fab -l 
 fab -f setup_train_server.py  do_all -H hello@192.168.100.221:666
 host字符串采用这种格式：username@hostname:port
"""

@task
def put_id_rsa():
    DIR_PATH = "~/.ssh"
    run("mkdir -p %s" % DIR_PATH)
    run("ls  %s " % DIR_PATH)
    put('~/.ssh/id_rsa', DIR_PATH)
    run("chmod 600 %s/id_rsa " % DIR_PATH)
    run("ls  %s " % DIR_PATH)

@task
def put_pub_key():
    remote_pub_file = "/tmp/a.pub"
    local_pub_file = '~/.ssh/id_rsa.pub' 
    #run("ls  %s " % DIR_PATH)
    put(local_pub_file, remote_pub_file)
    run("mkdir -p ~/.ssh/")
    run("cat %s >> ~/.ssh/authorized_keys" % remote_pub_file)

@task
def upgrade_git():
    run('sudo add-apt-repository ppa:git-core/ppa -y')
    run('sudo apt-get update')
    run('sudo apt-get install git') # "sudo apt-get install git -y  " will has some issues.
    run('git --version')

@task
def install_something():
    run('sudo apt-get install tmux') 



@task
def put_vimrc():
    put('~/.vimrc', '~/.vimrc')

@task
def fix_profile():
    run('echo -e "export PATH=/opt/conda/bin:/usr/local/conda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/java/jdk1.8.0_121/bin:/bin\n export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/lib\n export LIBRARY_PATH=/usr/local/cuda/lib64/stubs:\n" >> ~/.profile')

@task
def do_all():
    put_id_rsa()
    put_pub_key()
    #upgrade_git()
    #fix_profile()
