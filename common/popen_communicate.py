#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


from subprocess import Popen, PIPE, STDOUT
"""
p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=b'one\ntwo\nthree\nfour\nfive\nsix\n')[0]
print(grep_stdout.decode())
"""


#psql -U nuwa -h 192.168.100.18 -p54321 -d nuwa_db
os.putenv('PGPASSWORD', 'nuwa@123')
a = Popen('psql -U nuwa -h 192.168.100.18 -p54321 -d nuwa_db', shell=True, stdout=PIPE).stdout.readlines()
#a = Popen('psql -U nuwa -h 192.168.100.18 -p54321 -d nuwa_db', shell=True, stdout=PIPE).stdout.readlines()
print "ok"
print a
