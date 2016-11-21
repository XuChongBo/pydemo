# coding: utf-8
import yaml
import os
import re
import logging
from db import PgsqlDBProxy, DBConnectionWrapper
from db import check_table_exist
import subprocess
import tempfile

logger = logging.getLogger('utils')
# define the regex pattern that the parser will use to 'implicitely' tag your node
pattern = re.compile(r'^\<%= ENV\[\'(.*)\'\] %\>(.*)$')

# now define a custom tag ( say pathex ) and associate the regex pattern we defined
yaml.add_implicit_resolver("!pathex", pattern)

# at this point the parser will associate '!pathex' tag whenever the node matches the pattern

# you need to now define a constructor that the parser will invoke
# you can do whatever you want with the node value


def pathex_constructor(loader, node):
    value = loader.construct_scalar(node)
    envVar, remainingPath = pattern.match(value).groups()
    return os.environ[envVar] + remainingPath

# 'register' the constructor so that the parser will invoke 'pathex_constructor' for each node '!pathex'
yaml.add_constructor('!pathex', pathex_constructor)


def load_yaml(filepath):
    return yaml.load(open(filepath))


def call_command(cmd):
    try:
        print cmd
        # 这里不用subprocess提供的PIPE，而是使用自己创建的流
        # 原因是subprocess的PIPE是有大小限制.因此当输出内容超过65536，无法再塞进更多的数据, 会引起阻塞。
        out_temp = tempfile.SpooledTemporaryFile(bufsize=10*1000)
        fileno = out_temp.fileno()
        obj = subprocess.Popen(cmd, stdout=fileno, stderr=fileno, shell=True)
        obj.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        if len(lines) > 0:
            print ''.join(lines)
        if obj.returncode != 0:
            print "returncode:", obj.returncode
            raise Exception('call_command error. cmd:'+cmd)
    finally:
        if out_temp:
            out_temp.close()


def get_src_columns(db, table, columns):
    if columns == 'all':
        # check db supported
        assert(isinstance(db, PgsqlDBProxy))
        sql = 'SELECT column_name FROM information_schema.columns \
            WHERE table_name=\'{table}\' '.format(table=table)
        print sql
        with DBConnectionWrapper(db) as conn:
            cursor = conn.cursor()
            logger.debug('[get column] ' + sql)
            cursor.execute(sql)
            cols = [row[0] for row in cursor.fetchall()]
        assert(cols)
        src_columns_str = ','.join(cols)
    else:
        src_columns_str = ','.join(columns.keys())
    return src_columns_str


def get_dst_columns(db, table, columns):
    if columns == 'all':
        # check db supported
        assert(isinstance(db, PgsqlDBProxy))
        sql = 'SELECT column_name FROM information_schema.columns \
            WHERE table_name=\'{table}\' '.format(table=table)
        print sql
        with DBConnectionWrapper(db) as conn:
            cursor = conn.cursor()
            logger.debug('[get column] ' + sql)
            cursor.execute(sql)
            cols = [row[0] for row in cursor.fetchall()]
        assert(cols)
        dst_columns_str = ','.join(cols)

    else:
        dst_columns_str = ','.join(columns.values())
    return dst_columns_str


def dump_table(db, table, filepath):
    os.putenv('PGPASSWORD', db.passwd)
    cmd = 'pg_dump -F c  -U {user} -h {host} -p {port}  -d {db} -t {table} -O > {filepath}'.format( 
           user=db.user, host=db.host, port=db.port, db=db.db, table=table, filepath=filepath)
    call_command(cmd)
    logger.info('pg_dump')


def load_table(db, cursor, table, filepath):
    drop = ''
    if check_table_exist(cursor, table):
        drop = '-c'
    os.putenv('PGPASSWORD', db.passwd)
    cmd = 'pg_restore -F c -U {user} -h {host} -p {port} -d {db} -t {table} {drop} -O {filepath}'.format(
                user=db.user, host=db.host, port=db.port, db=db.db, table=table, drop=drop, filepath=filepath)
    call_command(cmd)
    logger.info('pg_restore')


def get_plugins(plugins):
    plugin_insts = []
    if plugins:
        logger.info('import plugins ...')
        count = 0
        for plugin in plugins:
            try:
                cls = import_class(plugin)
                plugin_insts.append(cls)
                logger.info('plugin: {p} imported.'.format(p=plugin))
                count += 1
            except ImportError:
                logger.exception('import {p} error'.format(p=plugin))
        logger.info('import {n} plugins.'.format(n=count))
    return plugin_insts


def table_default_transfer(cursor, tmp_table, dst_columns_str,
                           target_table, load_cond, dst_pk):
    if not check_table_exist(cursor, target_table):
        # rename tmp to target
        cursor.execute(
            'ALTER TABLE %s RENAME TO %s' % (tmp_table, target_table))
        logger.info(
            '[data_transfer] rename {tmp} to {target}'.format(
            tmp=tmp_table, target=target_table))
        return

    update_data_sql = 'UPDATE {target_table} \
        SET ({dst_columns_str}) = ({tmp_columns}) \
        FROM (SELECT {dst_columns_str} FROM {tmp_table}) AS tmp \
        WHERE {target_table}.{dst_pk}=tmp.{dst_pk}'.format(
        target_table=target_table,
        dst_columns_str=dst_columns_str,
        tmp_columns=','.join(
            ['tmp.{c}'.format(c=c) for c in dst_columns_str.split(',')]
        ),
        tmp_table=tmp_table,
        dst_pk=dst_pk)
    insert_data_sql = 'INSERT INTO {target_table} ({dst_columns_str}) \
        SELECT {dst_columns_str} \
        FROM {tmp_table} WHERE NOT EXISTS \
        (SELECT {dst_pk} FROM {target_table} \
        WHERE {target_table}.{dst_pk}={tmp_table}.{dst_pk}) {load_cond}'.format(
        target_table=target_table,
        dst_columns_str=dst_columns_str,
        tmp_table=tmp_table,
        dst_pk=dst_pk,
        load_cond=' AND ' + load_cond if load_cond else '')
    # update exist records
    logger.debug(update_data_sql)
    cursor.execute(update_data_sql)
    logger.info('[table:{t}] updated {c} records'.format(
        t=target_table, c=cursor.rowcount))
    # insert new records
    logger.debug(insert_data_sql)
    cursor.execute(insert_data_sql)
    logger.info('[table:{t}] inserted {c} records'.format(
        t=target_table, c=cursor.rowcount))

    # drop tmp table
    drop_tmp_sql = 'DROP TABLE {t}'.format(t=tmp_table)
    logger.debug(drop_tmp_sql)
    cursor.execute(drop_tmp_sql)
    logger.info('[data_transfer] drop tmp table: {t}'.format(t=tmp_table))


def drop_table(db, table):
    with DBConnectionWrapper(db) as conn:
        cursor = conn.cursor()
        if check_table_exist(cursor, table):
            cursor.execute('drop table %s' % table)
            logger.info('[drop_table] drop table: ' + table)
        conn.commit()


# dump question data from source DB with sql_condition
def dump_from_db(src_db, src_table, tmp_table, src_columns_str,
                 dst_columns_str, file_path, sql_condition):
    # clean
    drop_table(src_db, tmp_table)
    # create tmp table
    sql = 'CREATE TABLE {tmp_table}({dst_columns_str}) AS SELECT {src_columns_str} \
        FROM {src_table} {where_condition} WITH DATA;'.format(
        tmp_table=tmp_table,
        dst_columns_str=dst_columns_str,
        src_columns_str=src_columns_str,
        src_table=src_table,
        where_condition='WHERE ' + sql_condition if sql_condition else '')
    with DBConnectionWrapper(src_db) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    # dump
    dump_table(src_db, tmp_table, file_path)
    # clean tmp table
    drop_table(src_db, tmp_table)
