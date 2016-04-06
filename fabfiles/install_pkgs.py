#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
    author: brantxu 
    create: 2013-03-22
"""


from fabric.api import *
import logging,copy
import threading
import datetime
import time
import random
import sys

#env.hosts = ['10.166.138.151:36000', '172.27.180.119:36000', '10.129.145.236:36000']
#env.hosts = [ '172.27.180.119:36000']
#env.hosts = [ '10.208.15.11:36000']
#env.hosts = [ '10.166.138.151:36000']
#env.hosts = [ '10.166.138.153:36000']
#env.hosts = [ '10.177.151.158:36000']
#env.hosts = [ '10.129.145.236:36000']
#env.hosts = [ '10.163.164.144:36000']
#env.hosts = [ '10.128.12.81:36000']
env.hosts = [ '10.163.165.40:36000']
env.user = 'root'
env.password = 'password'

#env.passwords = {'root@10.166.138.151:36000':'password'}

def install_mysql():
    """
    install mysql to /usr/local/mysql,  with data_path=/data/mysql_db/       depends: cmake

    #注意安装后 把mysql的lib 目录添加到系统库目录列表中  以便第三方模块能找到mysql的动态库
    """
    run("""find / -name 'mysql'""")
    run("""find / -name 'mysqld'""")

    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('mysql-5.5.14.tar.gz', PKG_PATH)
            run("tar -xf mysql-5.5.14.tar.gz")

        with cd(PKG_PATH+'mysql-5.5.14/'):
            if 'yes'==prompt('extract end. to create account?: ', default='yes|skip', validate=r'(yes|skip)'):
                #添加mysql用户    
                run('groupadd mysql')
                run('useradd -g mysql mysql')

            #创建数据目录
            data_path = '/data/mysql_db/'
            if 'yes'==prompt('to create %s as data dir: ' % data_path, default='yes|skip', validate=r'(yes|skip)'):
                run('mkdir %s' % data_path)
                run('chown -R mysql %s' % data_path)
                run('chgrp -R mysql %s' % data_path)

            #cmake
            if 'yes'==prompt('to run cmake?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DMYSQL_DATADIR=%s -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DMYSQL_USER=mysql' % data_path)

            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
                with cd('/usr/local/mysql'):
                    run('chown -R mysql .')
                    run('chgrp -R mysql .')
                    run('./scripts/mysql_install_db --basedir=/usr/local/mysql --datadir=%s --user=mysql' % data_path)

            if 'yes'==prompt('to create my.cnf and mysql.server?: ', default='yes|skip', validate=r'(yes|skip)'):
                #拷贝配置文件
                run('cp support-files/my-medium.cnf /etc/my.cnf')
                #进程管理脚本    
                run('cp support-files/mysql.server /etc/init.d/')
                run('chmod a+x /etc/init.d/mysql.server')
                #配置开机自动启动
                run('chkconfig --add mysql.server')
            print 'to complete the install, you need to add  /usr/local/mysql/lib to /etc/ld.so.conf and run ldconfig.'
            print 'warings: make sure if my.cnf is ok (specially the bind-address), before start server by /etc/init.d/mysql.server start'


def install_svn():
    """
    install  without openssl.  depends: libxml2 
    """
    run("""find / -name 'svn'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('subversion-1.6.17.tar.gz', PKG_PATH)
            put('subversion-deps-1.6.17.tar.gz', PKG_PATH)
            run("tar -xf subversion-1.6.17.tar.gz")
            run("tar -xf subversion-deps-1.6.17.tar.gz")
        with cd(PKG_PATH+'subversion-1.6.17/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure --without-serf')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')


def install_openssl():
    """
    """
    run(""" find / -regex ".*ssl/bin/openssl$" """)
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('openssl-1.0.1a.tar.gz', PKG_PATH)
            run("tar -xf openssl-1.0.1a.tar.gz")
        with cd(PKG_PATH+'openssl-1.0.1a/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./config -fPIC')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
            if 'yes'==prompt('add /usr/local/ssl/lib to /etc/ld.so.conf and run ldconfig?: ', default='yes|skip', validate=r'(yes|skip)'):
                run(""" echo '/usr/local/ssl/lib' >> /etc/ld.so.conf """)
                run("ldconfig")


def install_pcre():
    """
    """
    run("""find / -name 'libpcre*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('pcre-8.31.tar.gz', PKG_PATH)
            run("tar -xf pcre-8.31.tar.gz")

        with cd(PKG_PATH+'pcre-8.31/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')


def install_cmake():
    """
    """
    run("""find / -name 'cmake'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('cmake-2.8.9.tar.gz', PKG_PATH)
            run("tar -xf cmake-2.8.9.tar.gz")

        with cd(PKG_PATH+'cmake-2.8.9/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')

def install_libxml2():
    """
    """
    run("""find / -name 'libxml*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('libxml2-2.7.4.tar.gz', PKG_PATH)
            run("tar -xf libxml2-2.7.4.tar.gz")
        with cd(PKG_PATH+'libxml2-2.7.4/'):
            if 'yes'==prompt('extract end. to run configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('extract end. to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')

            if 'yes'==prompt('extract end. to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')

def install_curl():
    """
    """
    run("""find / -name 'curl'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('curl-7.23.1.tar.gz', PKG_PATH)
            run("tar -xf curl-7.23.1.tar.gz")
        with cd(PKG_PATH+'curl-7.23.1/'):
            if 'yes'==prompt('extract end. to run configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('extract end. to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('extract end. to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')



def install_php():
    """
    depends: /usr/local/mysql/,   need to reinstall the curl
    """
    run("""find / -name 'php'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('php-5.4.3.tar.gz', PKG_PATH)
            run("tar -xvf php-5.4.3.tar.gz")
        with cd(PKG_PATH+'php-5.4.3/'):
            if 'yes'==prompt('extract end. to run configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure --with-mysql=/usr/local/mysql/ --enable-soap --enable-fpm  --with-curl --with-config-file-path=/etc')
            if 'yes'==prompt('extract end. to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make clean')
                run('make')

            if 'yes'==prompt('extract end. to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')

def install_nginx():
    """
    with-http_ssl_module.  depends: pcre ,  openssl-1.0.1a.tar.gz 
    """
    run("""find / -name 'nginx'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('nginx-1.0.10.tar.gz', PKG_PATH)
            run("tar -xf nginx-1.0.10.tar.gz")

        with cd(PKG_PATH+'nginx-1.0.10/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                #准备openssl的源码
                put('openssl-1.0.1a.tar.gz', './')
                run("tar -xf openssl-1.0.1a.tar.gz")
                #configure
                run('./configure --with-http_ssl_module --with-openssl=./openssl-1.0.1a')

            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')


def install_uwsgi():
    """
    install uwsgi to /usr/local/  .  depends: python>2.7.2 
    """
    run("""find / -name 'uwsgi'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('uwsgi-1.3.tar.gz', PKG_PATH)
            run("tar -xf uwsgi-1.3.tar.gz")
        with cd(PKG_PATH+'uwsgi-1.3/'):
            #没有configure， 直接make
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
        if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
            #直接拷贝 
            run('mv ./uwsgi-1.3 /usr/local/')



def install_python():
    """
    install  /usr/local/bin/python and /usr/bin/python. waring:must intall after openssl installed to avoid troubles.  depends: openssl
    """
    run("""find / -name 'python'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('Python-2.7.2.tar.bz2', PKG_PATH)
            run("tar -xf Python-2.7.2.tar.bz2")

        with cd(PKG_PATH+'Python-2.7.2/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
            if 'yes'==prompt('to ln -s /usr/local/bin/python  /usr/bin/python?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('ln -sf /usr/local/bin/python  /usr/bin/python')
            print 'install completed.'    


def install_pychecker():
    """
    depends: python
    """
    run("""find / -name 'pychecker'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('pychecker-0.8.19.tar.gz', PKG_PATH)
            run("tar -xf pychecker-0.8.19.tar.gz")
        with cd(PKG_PATH+'pychecker-0.8.19/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_MySQL_python():
    """
    depends: python, setuptools
    """
    run("""find / -name 'MySQL_python*.egg'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to upload the pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('MySQL-python-1.2.3.tar.gz', PKG_PATH)
            run("tar -xf MySQL-python-1.2.3.tar.gz")
        with cd(PKG_PATH+'MySQL-python-1.2.3/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):

                #修改cmcom.conf
                run(""" sed -i 's/^#mysql_config = \/usr\/local\/bin\/mysql_config/mysql_config = \/usr\/local\/mysql\/bin\/mysql_config/g' site.cfg  """)
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def install_setuptools():
    """
    depends: python
    """
    run("""find / -name 'setuptools*.egg'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to upload the pkg?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('setuptools-0.6c11-py2.7.egg', PKG_PATH)
        if 'yes'==prompt('to run sh setuptools-0.6c11-py2.7.egg?: ', default='yes|skip', validate=r'(yes|skip)'):
            run('sh setuptools-0.6c11-py2.7.egg')
        print 'install completed'    

def install_ZSI():
    """
    depends: python, PyXML, soapy
    """
    #run("""find / -name 'ZSI*.egg'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('ZSI-2.0-for-cmcom.tar.gz', PKG_PATH)
            run("tar -xf ZSI-2.0-for-cmcom.tar.gz")
        with cd(PKG_PATH+'ZSI-2.0-for-cmcom/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def install_PyXML():
    """
    depends: python
    """
    run("""find / -name 'PyXML*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('PyXML-0.8.4.tar.gz', PKG_PATH)
            run("tar -xf PyXML-0.8.4.tar.gz")
        with cd(PKG_PATH+'PyXML-0.8.4/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_soapy():
    """
    depends: python
    """
    run("""find / -name 'soapy*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('soapy-0.1.tar.gz', PKG_PATH)
            run("tar -xf soapy-0.1.tar.gz")
        with cd(PKG_PATH+'soapy-0.1/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_Django():
    """
    depends: python
    """
    run("""find / -name 'Django*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('Django-1.4.1.tar.gz', PKG_PATH)
            run("tar -xf Django-1.4.1.tar.gz")
        with cd(PKG_PATH+'Django-1.4.1/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_libgmp():
    """
    install libgmp in /usr/local/lib/  and create links in /usr/lib/
    """
    run("""find / -name 'libgmp*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('gmp-5.1.1.tar.bz2', PKG_PATH)
            run("tar -xf gmp-5.1.1.tar.bz2")

        with cd(PKG_PATH+'gmp-5.1.1/'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
                
            if 'yes'==prompt('to create links (to /usr/local/lib/libgmp.a,  xx.la,  xx.so) in /usr/lib/ and /usr/include/gmp.h linking to /usr/local/include/gmp.h?: ', default='yes|skip', validate=r'(yes|skip)'):
                #创建链接
                run('ln -sf /usr/local/include/gmp.h   /usr/include/gmp.h')
                run('ln -sf /usr/local/lib/libgmp.a  /usr/lib/libgmp.a')
                run('ln -sf /usr/local/lib/libgmp.la /usr/lib/libgmp.la')
                run('ln -sf /usr/local/lib/libgmp.so /usr/lib/libgmp.so')
def install_mongo_client():
    """
    """
    run("""find / -name 'mongo'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('mongo_tools.tgz', PKG_PATH)
            run("tar -xf mongo_tools.tgz")
        with cd(PKG_PATH+'mongo_tools/'):
            if 'yes'==prompt('install mongo client?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('mv ./mongo /usr/bin/mongo')
                run('chmod a+x /usr/bin/mongo')


def install_pymongo():
    """
    depends: python,setuptools
    """
    run("""find / -name 'pymongo*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('mongo-python-driver-2.4.1.tar.gz', PKG_PATH)
            run("tar -xf mongo-python-driver-2.4.1.tar.gz")
        with cd(PKG_PATH+'mongo-python-driver-2.4.1/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def install_suds():
    """
    depends: python
    """
    run("""find / -name 'suds*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('suds-0.4.tar.gz', PKG_PATH)
            run("tar -xf suds-0.4.tar.gz")
        with cd(PKG_PATH+'suds-0.4/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_xlwt():
    """
    depends: python
    """
    run("""find / -name 'xlwt*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('xlwt-0.7.4-for-cmcom.tar', PKG_PATH)
            run("tar -xf xlwt-0.7.4-for-cmcom.tar")
        with cd(PKG_PATH+'xlwt-0.7.4-for-cmcom/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')





def install_gnu_cryptoxx():
    """
    not comopleted
    """
    run("""find / -name '*crypto*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put tar and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('gnu-crypto-2.0.1.tar.bz2', PKG_PATH)
            run("tar -xf gnu-crypto-2.0.1.tar.bz2")

        with cd(PKG_PATH+'gnu-crypto-2.0.1'):
            if 'yes'==prompt('to configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
                

def install_fabric():
    """
    depends: python, setuptools, paramiko>=1.10, libgmp>=5
    """
    run("""find / -name 'fabric'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('fabric-1.6.zip', PKG_PATH)
            run("unzip fabric-1.6.zip")
        with cd(PKG_PATH+'fabric-1.6/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def install_paramiko():
    """
    depends: python, pycrypto>=2.1,!=2.4
    """
    run("""find / -name 'paramiko*.egg'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('paramiko-1.10.0.tar.gz', PKG_PATH)
            run("tar -xf paramiko-1.10.0.tar.gz")
        with cd(PKG_PATH+'paramiko-1.10.0/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')


def install_pycrypto():
    """
    depends: python, 
    """
    run(""" find / -name 'pycrypto*.egg*' """)
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('pycrypto-2.6.tar.gz', PKG_PATH)
            run("tar -xf pycrypto-2.6.tar.gz")
        with cd(PKG_PATH+'pycrypto-2.6/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def set_env():
    """
    check and set on linux
    """
    #查看硬盘情况
    if 'yes'==prompt('to check disk?: ', default='yes|skip', validate=r'(yes|skip)'):
        run('df -h')
    #设置时间同步 
    #54 */3 * * * /usr/sbin/ntpdate 172.23.32.142 172.24.18.141 > /dev/null 2>&1
    if 'yes'==prompt('make sure ntpdate is ok.', default='yes|skip', validate=r'(yes|skip)'):
        pass
    #上传.vimrc文件
    if 'yes'==prompt('to upload the .vimrc?: ', default='yes|skip', validate=r'(yes|skip)'):
        put(".vimrc", "~/")

    if 'yes'==prompt('to check iptables?: ', default='yes|skip', validate=r'(yes|skip)'):
        run("iptables -L -v")


def install_psutil():
    """
    depends: python
    """
    #run("""find / -name 'psutil*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('psutil-0.7.1.tar.gz', PKG_PATH)
            run("tar -xf psutil-0.7.1.tar.gz")
        with cd(PKG_PATH+'psutil-0.7.1/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')

def install_httplib2():
    """
    depends: python
    """
    run("""find / -name 'httplib2*.egg*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        #上传文件
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('httplib2-0.7.6.tar.gz', PKG_PATH)
            run("tar -xf httplib2-0.7.6.tar.gz")
        with cd(PKG_PATH+'httplib2-0.7.6/'):
            if 'yes'==prompt('to build?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py build')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('python setup.py install')



def install_protobuf():
    """
    """
    run("""find / -name 'protobuf'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('protobuf-2.4.1.tar.bz2', PKG_PATH)
            run("tar -xf protobuf-2.4.1.tar.bz2")
        with cd(PKG_PATH+'protobuf-2.4.1/'):
            if 'yes'==prompt('to run configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')
                with cd(PKG_PATH+'protobuf-2.4.1/python/'):
                    run('python setup.py install')


def install_openssh():
    """
    """
    run("""find / -name 'ssh*'""")
    PKG_PATH = '/tmp/'
    with cd(PKG_PATH):
        if 'yes'==prompt('check end. to put pkg and extract?: ', default='yes|skip', validate=r'(yes|skip)'):
            put('openssh-6.2p2.tar.gz', PKG_PATH)
            run("tar -xf openssh-6.2p2.tar.gz")
        with cd(PKG_PATH+'openssh-6.2p2/'):
            if 'yes'==prompt('to run configure?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('./configure')
            if 'yes'==prompt('to make?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make')
            if 'yes'==prompt('to install?: ', default='yes|skip', validate=r'(yes|skip)'):
                run('make install')


def set_env_before_install_cmcom():
    """ 
    depends: python2.7

    TODO
    #检查eth1是工作网口
    #检查crontab 中的python版本是否为2.7  使用： * * * * * python -V  > /tmp/x.log 2>&1
    #检查python的版本是否为2.7
    #mysql添加账号replicate_user reader
    """
    #目标机器上的运行目录
    RUNNING_DIR= '/data/cmcom/running/'

    if 'yes'==prompt('create account? ', default='yes|skip', validate=r'(yes|skip)'):
        #创建账号和目录
        run("useradd -d /data/cmcom -m cmcom")
        #给 group 和others  可读可执行权限， 因为nginx需要读取前台静态资源
        run("chmod go+rx /data/cmcom")
        #设置密码
        run("passwd cmcom")

    #创建运行目录
    if 'yes'==prompt('create %s as running dir? ' % RUNNING_DIR, default='yes|skip', validate=r'(yes|skip)'):
        run("mkdir %s " % RUNNING_DIR)
        run("chown -R cmcom:users %s  " % RUNNING_DIR)
    
    if 'yes'==prompt('create db  cmcom_db? if the mysqld no runing. just skip.', default='yes|skip', validate=r'(yes|skip)'):
        run("mysql -uroot -e 'create database cmcom_db;' ")

    #检查是否成功    
    with cd(RUNNING_DIR):
        if 'yes'==prompt('create cmcom link in python lib path?', default='yes|skip', validate=r'(yes|skip)'):
            run("rm -f /usr/local/lib/python2.7/site-packages/cmcom")
            run("ln -s %s /usr/local/lib/python2.7/site-packages/cmcom" % RUNNING_DIR)
            run('touch __init__.py')

    if 'yes'==prompt('svn co to create /data/cmcom/public_tools?', default='yes|skip', validate=r'(yes|skip)'):
        run(""" svn co 'svn://10.161.8.21:8080/dev_group/others/public_tools'  /data/cmcom/public_tools  """)
        run("chown -R cmcom:users /data/cmcom/public_tools")
    #检查是否成功    
    with cd(RUNNING_DIR):
        run("""cat /etc/passwd | grep cmcom""")
        print 'Completed!'

