#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import traceback
import psycopg2 
import psycopg2.extras
import sys
from py2neo import Graph, Node, Relationship, watch, authenticate


http_port = 7474
bolt_port = 7687
host = "x.com.cn"

authenticate("%s:%s" % (host, http_port), "name", "password")
# connect to authenticated graph database
g = Graph("http://%s:%s/db/data/" % (host, http_port), bolt_port=bolt_port)
g.data('match (n) return count(*)')
g.run('match (n) return count(*)').dump()
now_datetime = datetime.datetime.now()

def getDBConnection():
    conn = psycopg2.connect(
        host="x.com.cn",
        port=432,
        user="uu",
        password="xx",
        dbname="xx",
        connect_timeout=10)
    return conn

watch('httpstream')

conn = getDBConnection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def gradeNode(g):
    label = "Grade"
    key = "code"
    if not g.schema.get_uniqueness_constraints(label):
        g.schema.create_uniqueness_constraint(label, key)

    #sql = "select stage_subject, chapter_id, knowledges from tiku_chapter_knowledge_mapping limit 10"
    sql = "select   code, \
                    stagesubject as stage_subject,\
                    name, sequence,create_time,update_time  \
           from tiku_grade"
    cursor.execute(sql)
    count = 0
    tx = g.begin()
    for record in cursor:
        #NOTE: Here record is a DictRow, you can also trans it to a normal dict by dict(record)
        if record['create_time'] is None:
            record['create_time'] = now_datetime 
        if record['update_time'] is None:
            record['update_time'] = now_datetime
        record['create_time'] = datetime.datetime.strftime(record['create_time'], '%Y%m%d%H%M%S')
        record['update_time'] = datetime.datetime.strftime(record['update_time'], '%Y%m%d%H%M%S')
        #print record
        try:
            n = Node(label, **record)
            tx.merge(n, primary_label=label, primary_key=key) 
            count += 1
            print count, n
        except:
            print "record: ", record
            print traceback.format_exc()
            raw_input('press enter to continue or ctrl+c to exit.')
    tx.commit() 
    g.run('match (n:%s) return count(*)' % label).dump()


gradeNode(g)

