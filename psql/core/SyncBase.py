# coding: utf-8

import sys
import os
import logging
import importlib
from db import PgsqlDBProxy
import utils
import time

logger = logging.getLogger()
debug = True
logger.setLevel(logging.DEBUG if debug else logging.INFO)
logging.basicConfig(stream=sys.stdout)


class SyncBase(object):
    def __init__(self, task_dir):
        self.src_db = None
        self.dst_db = None
        self.dst_conn = None
        filepath = os.path.join(task_dir, 'task.yaml')
        self.parse(filepath)
        sys.path.append(task_dir)
        self.customs = {}
        for table in self.dst_table_list:
            try:
                self.customs[table] = importlib.import_module(table)
            except:
                pass
        logger.info('[syncbase] customs: %s' % self.customs)
        # tables = ['tiku_cate_mapping', 'tiku_external_resource', 'tiku_stage_subject']
        # self.customs =  dict(zip(tables, map( __import__, tables)))

    def connect(self):
        self.dst_conn = self.dst_db.get_inst()
        self.dst_cursor = self.dst_conn.cursor()

    def run(self, remote=True):
        try:
            # dump
            if remote:
                self.dump()
            # keep all operations in single transaction
            self.connect()
            # load
            self.load()
            self.commit()
            # do transfer
            start_time = time.time()
            self.before(self.dst_cursor)
            self.transfer()
            self.after(self.dst_cursor)
            # commit
            self.commit()
            end_time = time.time()
            logger.info('[transfer] cost:%s ms' % int((end_time-start_time)*1000) )
        finally:
            self.close()

    def __del__(self):
        pass

    def parse(self, filepath):
        args = utils.load_yaml(filepath)
        print args
        task_name = args.keys()[0]
        self.data_dir = args[task_name]['data_dir']

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        src_db = args[task_name]['src_db']
        dst_db = args[task_name]['dst_db']
        self.src_db = PgsqlDBProxy(src_db['HOST'], src_db['PORT'],
                                   src_db['USER'], src_db['PASSWORD'],
                                   src_db['DB_NAME'])
        self.dst_db = PgsqlDBProxy(dst_db['HOST'], dst_db['PORT'],
                                   dst_db['USER'], dst_db['PASSWORD'],
                                   dst_db['DB_NAME'])
        self.pairs = args[task_name]['pairs']
        self.dst_table_list = [pair['dst_table'] for pair in self.pairs]

    def dump(self):
        logger.info('###################### dump data #######################')
        for pair in self.pairs:
            logger.info('[dump] =====%s====' % pair)
            src_table = pair['src_table']
            dst_table = pair['dst_table']
            columns = pair.get('columns')
            src_cond = pair.get('src_cond', '')
            logger.debug('[dump]columns:%s' % columns)
            # get columns
            src_columns_str = utils.get_src_columns(
                self.src_db, src_table, columns)
            dst_columns_str = utils.get_dst_columns(
                self.src_db, src_table, columns)
            table_file_path = os.path.join(self.data_dir, dst_table+'.bin')

            # predump
            custom_table = self.customs.get(dst_table, None)
            if custom_table and getattr(custom_table, 'predump', None):
                custom_table.predump()
            # dump data
            tmp_table = 'tmp_'+dst_table+'_for_sync'
            utils.dump_from_db(self.src_db, src_table, tmp_table,
                               src_columns_str, dst_columns_str,
                               table_file_path, src_cond)
            logger.info('[dump] from [db:{db}-table:{table}] \
                with condition:{cond} to [file:{file_path}]'.format(
                db=self.src_db,
                table=src_table,
                cond=src_cond,
                file_path=table_file_path))

    def load(self):
        logger.info('###################### load data #######################')
        for pair in self.pairs:
            logger.info('[load] =====%s====' % pair)
            dst_table = pair['dst_table']
            table_file_path = os.path.join(self.data_dir, dst_table+'.bin')
            tmp_table = 'tmp_'+dst_table+'_for_sync'
            # load data
            utils.load_table(
                self.dst_db, self.dst_cursor, tmp_table, table_file_path)
            logger.info('[load] from [file:{file_path}] to \
                [db:{db}-table:{table}]'.format(
                file_path=table_file_path,
                db=self.dst_db,
                table=tmp_table))
            # postload 
            custom_table = self.customs.get(dst_table, None)
            if custom_table and getattr(custom_table, 'postload', None):
                custom_table.postload(self.dst_cursor)

    def before(self):
        pass

    def transfer(self):
        logger.info('################### transfer data #####################')
        for pair in self.pairs:
            logger.info('[transfer] =====%s====' % pair)
            src_table = pair['src_table']
            dst_table = pair['dst_table']
            columns = pair.get('columns')
            dst_cond = pair.get('dst_cond', '')
            logger.debug('[transfer] columns:%s' % columns)

            custom_table = self.customs.get(dst_table, None)
            # pretransfer
            if custom_table and getattr(custom_table, 'pretransfter', None):
                custom_table.pretransfter()

            # transfer
            if custom_table and getattr(custom_table, 'transfer', None):
                custom_table.transfer(self.dst_cursor)
                logger.info('[transfer] custom transfer data ok. from [db:{db}-table:{tmp_table}] to [db:{db}-table:{table}] with \
                    condition:{cond}'.format(tmp_table=tmp_table, db=self.dst_db, table=dst_table, cond=dst_cond))
            else:
                # get columns
                tmp_table = 'tmp_'+dst_table+'_for_sync'
                dst_columns_str = utils.get_dst_columns( self.dst_db, tmp_table, columns)
                # transfer
                utils.table_default_transfer(self.dst_cursor, tmp_table, dst_columns_str, dst_table, dst_cond, pair['dst_pk'])
                logger.info('[transfer] transfer data ok. from [db:{db}-table:{tmp_table}] to [db:{db}-table:{table}] with \
                        condition:{cond}'.format( tmp_table=tmp_table, db=self.dst_db, table=dst_table, cond=dst_cond))

            # posttransfer
            if custom_table and getattr(custom_table, 'posttransfer', None):
                custom_table.posttransfer()

    def after(self, db):
        pass

    def commit(self):
        self.dst_conn.commit()
        logger.info('[syncbase] commit ok.')

    def close(self):
        if self.dst_conn:
            logger.info('[syncbase] close conn: %s' % self.dst_conn)
            self.dst_conn.close()

if __name__ == '__main__':
    if 2 == len(sys.argv):
        do_sync(sys.argv[1])
    else:
        print "usage: %s task.yaml" % __file__
        sys.exit(1)
