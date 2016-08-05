#!/usr/bin/env python
# -*- coding:utf-8 -*-

current_dir = os.path.dirname(__file__)


#a = importlib.import_module(current_dir, mod)
setattr(sync, mod, __import__(mod))
tables = ['before','after', 'tiku_cate_mapping', 'tiku_external_resource','tiku_stage_subject']
self.customs =  map( __import__, tables)


# 动态加载module
def get_resouce_file(code):
    mod = 'nuwa_resources'
    if mod not in globals():
        globals()[mod] = __import__(mod)
        nuwa_resources.setDirPath(settings.RESOURCE_TOKEN, settings.RESOURCE_DIR)
        logger.info('load nuwa_resources meta data ok.')
    out = nuwa_resources.decodeFile(settings.RESOURCE_TOKEN, code)


