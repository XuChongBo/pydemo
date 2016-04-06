#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from fabric.api import *

#env.hosts = ['10.166.138.153:36000']
#env.hosts = ['10.177.151.158:36000']
#env.hosts = ['172.27.180.119:36000']
env.hosts = ['10.208.15.11:36000']
#env.hosts = ['10.161.131.100:36000']
#env.hosts = ['10.166.138.151:36000']
#env.hosts = ['10.161.131.100:36000','10.166.138.153:36000','10.177.151.158:36000']
env.user = "root"
env.password = 'xxx'

def create_reader_account():
    """
    this target is master.
    """
    #创建reader账号
    #run("""mysql -uroot -e "grant select on *.* to 'reader'@'%' identified by 'reader@secu'; flush privileges;" """)
    run("""mysql -uroot -e "grant select, show view on *.* to 'reader'@'localhost' identified by 'reader@secu'; flush privileges;" """)

def create_monitor_account():
    """
    this target is master. here, the monitor is 10.208.15.11
    """
    #创建可查slave状态的replicate_user账号
    run("""mysql -uroot -e "grant REPLICATION SLAVE,REPLICATION CLIENT on *.* to 'replicate_user'@'10.208.15.11' identified by 'replicate_user@secu'; flush privileges;" """)


def create_local_monitor_account():
    """
    this target is master. here, the monitor is localhost
    """
    #创建可查slave状态的replicate_user账号
    run("""mysql -uroot -e "grant REPLICATION SLAVE,REPLICATION CLIENT on *.* to 'replicate_user'@'localhost' identified by 'replicate_user@secu'; flush privileges;" """)



def create_replicate_account():
    """
    this target is master.
    """
    #创建replicate_user账号
    run("""mysql -uroot -e "grant replication slave on *.* to 'replicate_user'@'%' identified by 'replicate_user@secu'; flush privileges;" """)

def become_slave_from_master_data(master_ip=None):
    """
    make target to be slave.  depends: ./cmcom_db_master.sql  in local machine 
    """
    if not master_ip:
        print 'need master_ip'
        print 'example:   fab become_slave_from_master_data:x.x.x.x'
        return
    print 'master_ip is ', master_ip

    #上传数据文件
    if 'yes'==prompt('put the cmcom_db_master.sql to /tmp/?', default='yes|skip', validate=r'(yes|skip)'):
        put('./cmcom_db_master.sql', '/tmp/')
        local("""ls -l ./cmcom_db_master.sql""")
        run("""ls -l /tmp/cmcom_db_master.sql""")
        print '=================WARNNING:  make sure the /tmp/cmcom_db_master.sql is ok. ======================'
    #检查slave状态
    run("""mysql -uroot -e 'show slave status\G;' """) 
    print '=================Tip:  check the slave status. ======================'
    #关闭slave
    if 'yes'==prompt('to stop slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave stop;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)   #获取master位置：Relay_Master_Log_File  Exec_Master_Log_Pos  
        print '=================Tip:  make sure slave is stopped. ======================'
    #创建新db
    if 'yes'==prompt('drop database cmcom_db and create new?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'drop database cmcom_db;' """) 
        run("""mysql -uroot -e 'create database cmcom_db;' """) 

    #数据导入db    
    if 'yes'==prompt('run mysql cmcom_db < /tmp/cmcom_db_master.sql?', default='yes|skip', validate=r'(yes|skip)'):
        if 'yes'==prompt('change master_host to %s first' % master_ip, default='yes|skip', validate=r'(yes|skip)'):
            run(""" mysql -uroot -e"reset slave;" """)
            run(""" mysql -uroot -e "change master to 
                            master_host='%s', 
                            master_port=3306,
                            master_user='replicate_user',
                            master_password='replicate_user@secu'; " """ % master_ip)  
            run(""" mysql cmcom_db < /tmp/cmcom_db_master.sql """)
    if 'yes'==prompt('check the slave status?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'show slave status\G;' """)   
    #开启slave    
    if 'yes'==prompt('to start slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave start;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)   
        print '=================Tip:  make sure slave is running and ok. ======================'


 

def become_slave_from_other_slave_data(master_ip=None,master_log_file_name=None, master_log_pos=None):
    """
    make target to be slave.  depends: ./cmcom_db_slave.sql  in local machine
    """
    if not (master_ip and master_log_file_name and master_log_pos):
        print 'need input args: master_ip,master_log_file_name, master_log_pos'
        print 'example:   fab become_slave:xx.xx, binglogxx, 123'
        return
    print master_ip,master_log_file_name, master_log_pos

    if 'yes'==prompt('put the cmcom_db_slave.sql to /tmp/?', default='yes|skip', validate=r'(yes|skip)'):
        put('./cmcom_db_slave.sql', '/tmp/')
        local("""ls -l ./cmcom_db_slave.sql""")
        run("""ls -l /tmp/cmcom_db_slave.sql""")
        print '=================WARNNING:  make sure the /tmp/cmcom_db_slave.sql is ok. ======================'
    #当前slave的状态
    run("""mysql -uroot -e 'show slave status\G;' """) 
    print '=================Tip:  check the slave status. ======================'
    if 'yes'==prompt('to stop slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave stop;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)   #获取master位置：Relay_Master_Log_File  Exec_Master_Log_Pos  
        print '=================Tip:  make sure slave is stopped. ======================'

    if 'yes'==prompt('drop database cmcom_db and create new?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'drop database cmcom_db;' """) 
        run("""mysql -uroot -e 'create database cmcom_db;' """) 
    if 'yes'==prompt('run mysql cmcom_db < /tmp/cmcom_db_slave.sql?', default='yes|skip', validate=r'(yes|skip)'):
        run(""" mysql cmcom_db < /tmp/cmcom_db_slave.sql """)

    if 'yes'==prompt('change master to %s, %s, %s?' % (master_ip,master_log_file_name, master_log_pos), default='yes|skip', validate=r'(yes|skip)'):
        run(""" mysql -uroot -e"reset slave;" """)
        run(""" mysql -uroot -e "change master to 
                    master_host='%s', 
                    master_port=3306,
                    master_user='replicate_user',
                    master_password='replicate_user@secu',
                    master_log_file='%s',
                    master_log_pos=%s;
                    "
            """ % (master_ip,master_log_file_name, master_log_pos) )

        run("""mysql -uroot -e 'show slave status\G;' """)   #获取master位置：Relay_Master_Log_File  Exec_Master_Log_Pos  
    if 'yes'==prompt('to start slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave start;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)   #获取master位置：Relay_Master_Log_File  Exec_Master_Log_Pos  
        print '=================Tip:  make sure slave is running and ok. ======================'


def check_acccounts():
    """
    this target is master.
    """
    run("""mysql -uroot -e 'select user,host from mysql.user;' """)

def show_master_status():
    """
    this target is master.
    """
    run("""mysql -uroot -e 'show master status;' """) 


def start_slave():
    """
    this target is slave.
    """
    run("""mysql -uroot -e 'slave start;' """) 
    run("""mysql -uroot -e 'show slave status\G;' """) 



def show_slave_status():
    """
    this target is slave.
    """
    run("""mysql -uroot -e 'show slave status\G;' """) 

def copy_this_slave():
    """
    this target is the existsing slave.  copy the slave and get cmcom_db_slave.sql.

    从现有的一个slave复制一个slave出来， 不用操作master即可增加一个slave
    ps: 执行机作为现有slave
    """
    #当前slave的状态
    run("""mysql -uroot -e 'show slave status\G;' """) 
    print '=================Tip:  check the slave status. ======================'

    if 'yes'==prompt('to stop slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave stop;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)   #获取master位置：Relay_Master_Log_File  Exec_Master_Log_Pos  
        print '=================Tip:  remember the Master_Host, Relay_Master_Log_File and Exec_Master_Log_Pos. ======================'
        print '=================Tip:  make sure slave is stopped. ======================'

    if 'yes'==prompt('dump cmcom_db data?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'show master status;' """)  
        run("""mysqldump -uroot  cmcom_db > /tmp/cmcom_db_slave.sql""")
        run("""ls -l /tmp/cmcom_db_slave.sql""")
        run("""mysql -uroot -e 'show master status;' """)  #为确认期间没有变更过
        print '=====================WARNING:  make sure the master status has no change. ================================'

    if 'yes'==prompt('to start slave?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'slave start;' """) 
        run("""mysql -uroot -e 'show slave status\G;' """)  #确认slav已开启
        print '=====================WARNING:  make sure the slave is running. ================================'
    if 'yes'==prompt('save cmcom_db_slave.sql to local machine?', default='yes|skip', validate=r'(yes|skip)'):
        get("/tmp/cmcom_db_slave.sql", "./")
        run("""ls -l /tmp/cmcom_db_slave.sql""")
        local("""ls -l ./cmcom_db_slave.sql""")
        print '=================Tip:  make sure they are the same. ======================'

def copy_this_master():
    """
    this target is master.  copy the master and get a copy:  cmcom_db_master.sql.
    """
    print '============WARNING:  make sure u has locked the master by FLUSH TABLES WITH READ LOCK;  ======================='
    if 'no'==prompt('has done that?', default='yes|skip', validate=r'(yes|no)'):
        return

    if 'yes'==prompt('dump cmcom_db data?', default='yes|skip', validate=r'(yes|skip)'):
        run("""mysql -uroot -e 'show master status;' """)  
        run("""mysqldump -uroot --master-data=1  cmcom_db > /tmp/cmcom_db_master.sql""")
        run("""ls -l /tmp/cmcom_db_master.sql""")
        run("""mysql -uroot -e 'show master status;' """)  #为确认期间没有变更过
        print '=====================WARNING:  make sure the master status has no change. ================================'

    if 'yes'==prompt('save cmcom_db_master.sql to local machine?', default='yes|skip', validate=r'(yes|skip)'):
        get("/tmp/cmcom_db_master.sql", "./")
        run("""ls -l /tmp/cmcom_db_master.sql""")
        local("""ls -l ./cmcom_db_master.sql""")
        print '=================Tip:  make sure they are the same. ======================'

    print '============WARNING: u need to unlock the master by UNLOCK TABLES; ======================='
