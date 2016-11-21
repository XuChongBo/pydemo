# coding: utf-8

import sys
import os
import logging
import importlib
import datetime
import json
import time
import psycopg2
import psycopg2.extras
import MySQLdb
import traceback
import uuid
from py2neo import Graph, Node, Relationship
from py2neo import watch, authenticate
from py2neo import NodeSelector
from collections import defaultdict

logger = logging.getLogger("mylog")
debug = False
if debug:
    watch('httpstream')
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

logging.basicConfig(stream=sys.stdout)


def saveToSQLDB(sql, records):

    try:
        conn, cursor = connectSQLDB(dbtype="postgres",host="xx.cn", port=5432, user='xx', password='xx', dbname='dbxx')
#       conn, cursor = connectSQLDB(dbtype="mysql",host="xx.cn", port=3306, user='xx', password='xx', dbname='dbxx')
        cursor.executemany(sql, records)
        conn.commit()
    finally:
        conn.close()



def connectSQLDB(dbtype, host, port, user, password, dbname):
    if dbtype=="postgres":
        sqldb_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            connect_timeout=10)
        sqldb_cursor = sqldb_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    elif dbtype=="mysql":
        sqldb_conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=dbname,
            charset='utf8')
        sqldb_cursor = sqldb_conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    else:
        raise RuntimeError("sqldb type %s is not supported. " % dbtype)
    return sqldb_conn,sqldb_cursor

def connectNeo4j(host, http_port, bolt_port, user, password):
    authenticate("%s:%s" % (host, http_port), user, password)
    # connect to authenticated graph database
    graph = Graph("http://%s:%s/db/data/" % (host, http_port), bolt_port=bolt_port)
    return graph

def saveKnowledge2ChapterIntoSQLDB():
    g = connectNeo4j(host="001.cn", http_port=7476, bolt_port=7689, user='neo4j', password='neo4j')
    graph_cursor = g.run("MATCH (k:Knowledge)-[:ATTACH_TO]->(c:Chapter ) RETURN k.code,k.name, k.stage_subject, c.code,c.name,c.stage_subject ")

    mapping = defaultdict(set)
    records = []
    subject_dict = {}

    for item in graph_cursor:
#        print item
        # chapter -> knowledge
        mapping[item['c.code']].add(item['k.code'])

        # save subject map
        subject_dict[item['c.code']] = item['c.stage_subject']

        print item['c.code'], item['c.name'], "->", item['k.code'], item['k.name'] 

    # convert to list
    for k, v in mapping.items():
        #print k, v
        records.append((k, json.dumps(list(v), ensure_ascii=False), subject_dict[k]))
    print "last 10 of records: ", records[-10:]
    print "total: ", len(records)
    # save to db
    sql = ("insert into xx(chapter_id, knowledges, stage_subject) values (%s,%s, %s)")
    saveToSQLDB(sql, records)

def deriveKnowledge2ChapterIntoNeo4j():
    pass
def createRoots():
    pass
    

if __name__ == "__main__":
    print "createRoots, deriveKnowledge2ChapterIntoNeo4j, saveKnowledge2ChapterIntoSQLDB, deriveMathChapter2ChapterAndSaveToSQLDB"
    func = sys.argv[1]
    globals()[func]()
