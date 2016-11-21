# coding: utf-8

import logging
# import MySQLdb
import psycopg2

logger = logging.getLogger('dbproxy')


class DBProxy(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def get_inst(self):
        raise NotImplemented

    def __str__(self):
        return '<{host}:{port}:[{db}]>'.format(
            host=self.host, port=self.port, db=self.db)

"""
class MysqlDBProxy(DBProxy):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        super(MysqlDBProxy, self).__init__(host, port, user, passwd, db)
        self.charset = charset

    def get_inst(self):
        conn = MySQLdb.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset=self.charset)
        return conn
"""


class PgsqlDBProxy(DBProxy):
    def __init__(self, host, port, user, passwd, db, timeout=10):
        super(PgsqlDBProxy, self).__init__(host, port, user, passwd, db)
        self.timeout = timeout

    def get_inst(self):
        print 'trying connect:{host}:{port}:{db} user:{user} passwd:{passwd}'.format(
            host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd)

        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passwd,
            dbname=self.db,
            connect_timeout=self.timeout)
        return conn


class DBConnectionWrapper:
    def __init__(self, proxy):
        self.proxy = proxy
        self.conn = None

    def __enter__(self):
        self.conn = self.proxy.get_inst()
        return self.conn

    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()


def check_db_exist(cursor, dbname):
    res = False
    sql = 'select 1 from  pg_database where datname=\'{dbname}\''.format(
        dbname=dbname)
    cursor.execute(sql)
    res = True if cursor.fetchall() else False
    return res


def check_table_exist(cursor, table):
    res = False
    # sql = 'SELECT 1 FROM information_schema.tables \
    #    WHERE table_name=\'{t}\''.format(t=table)
    sql = 'SELECT 1 FROM pg_catalog.pg_class c \
        INNER JOIN pg_catalog.pg_namespace n \
        ON c.relnamespace=n.oid \
        WHERE n.nspname=\'public\' AND c.relname=\'{t}\''.format(t=table)
    cursor.execute(sql)
    res = True if cursor.fetchall() else False
    return res
