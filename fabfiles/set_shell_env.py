#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from fabric.api import env, run, local, shell_env
 
env.hosts = ['bjhee@example1.com', ]
env.password = '111111'
 
def hello():
    with shell_env(JAVA_HOME='/opt/java'):
        run('echo $JAVA_HOME')
        local('echo $JAVA_HOME')
