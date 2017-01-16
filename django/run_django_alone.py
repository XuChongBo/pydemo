# coding: utf-8

from __future__ import unicode_literals
import django
from django.conf import settings
import os

settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DST_DB_NAME'),
            'USER': os.getenv('DST_DB_USER'),
            'PASSWORD': os.getenv('DST_DB_PASSWORD'),
            'HOST': os.getenv('DST_DB_HOST'),
            'PORT': os.getenv('DST_DB_PORT'),
            'TEST': {
                'NAME': 'test_target_pangu',
            },
        },
        'source': {
            # use customize backend for iterator fetch
            'ENGINE': 'common.db.backends.postgresql',
            'NAME': os.getenv('SRC_DB_NAME'),
            'USER': os.getenv('SRC_DB_USER'),
            'PASSWORD': os.getenv('SRC_DB_PASSWORD'),
            'HOST': os.getenv('SRC_DB_HOST'),
            'PORT': os.getenv('SRC_DB_PORT'),
            'TEST': {
                'NAME': 'test_source_pangu',
            },
        }
    },


    INSTALLED_APPS = (
        # add support for postgres
        'django.contrib.postgres',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # apps
        'common',
        'knowledge',
        'section',
        'issue',
        'ex_resource',
    ),
)

django.setup()

from repoze.lru import lru_cache
from django.db.models import Q
from django.db import transaction

from django.db import models
from django.contrib.postgres.fields import JSONField

import os
from table_sync.syncbase import SyncBase

# from common.utils import memoize
from common.base_command import SyncBaseCommand
from common.ks_mapping import KSMappingMixin
from common.db.backends.postgresql.base import server_side_cursors
from ex_resource.models import TikuExternalResource, ExResource


from common.constants import TechUMeta

#class PullFuxi(TechUMeta, KSMappingMixin):
class PullFuxi(SyncBase, TechUMeta, KSMappingMixin):
    help = (
        'sync TikuExternalResource table to ExResource'
        'NOTICE: need KnowledgePoint and SectionPoint'
    )
    SOURCE_DB = 'source'
    LRU_CACHE_SIZE = 2000
    K2S_MAP = {}
    S2S_MAP = {}

    def __init__(self):
        task_dir = os.path.dirname(__file__)
        super(PullFuxi, self).__init__(task_dir)

    @lru_cache(LRU_CACHE_SIZE)
    def _get_knowledge_path(self, code, resource):
        """return kid and its ancestors"""
        kids = self.get_knowledge_ancestors(code)
        if not kids:
            self.stdout.write('knowledge <{c}:{s}> ex_resource <{r}> not found'.format(
                c=code, s=resource.stage_subject, r=resource.code))
        return kids

    @lru_cache(LRU_CACHE_SIZE)
    def _get_section_path(self, code, resource):
        """return sid and its ancestors"""
        sids = self.get_section_ancestors(code)
        if not sids:
            self.stdout.write('section <{c}:{s}> ex_resource <{r}> not found'.format(
                c=code, s=resource.stage_subject, r=resource.code))
        return sids

    def _get_extend_codes(self, resource):
        data = {}
        code = resource.parentcode
        source_key = ExResource.EXRESOURCE_SOURCE_TYPE_MAP.get(resource.sourcetype)
        if (resource.sourcetype == ExResource.SOURCE_TYPE.ISSUE
           or resource.sourcetype == ExResource.SOURCE_TYPE.GENERAL):
            # just return self
            data = {
                source_key: [code]
            }
        elif resource.sourcetype == ExResource.SOURCE_TYPE.KNOWLEDGE:
            section_key = ExResource.EXRESOURCE_SOURCE_TYPE_MAP[ExResource.SOURCE_TYPE.SECTION]
            merge_sections = [
                self._get_section_path(s, resource)
                for s in self.K2S_MAP.get(code, [])
            ]
            data = {
                source_key: self._get_knowledge_path(code, resource)
            }
            if merge_sections:
                data.update({
                    section_key: list(set(self.flat_list_of_lists(merge_sections)))
                })
        elif resource.sourcetype == ExResource.SOURCE_TYPE.SECTION:
            # extend section to section
            merge_sections = [
                self._get_section_path(s, resource)
                for s in self.S2S_MAP.get(code, [code])
            ]
            data = {
                source_key: list(set([
                    item for sublist in merge_sections for item in sublist
                ]))
            }
        return data

    def _sync_ex_resources(self, batch_size=1000, limit=0):
        # sync knowledge to section mapping
        self.K2S_MAP = self.get_knowledge2section_map()
        self.S2S_MAP = self.get_section2section_map()
        query_filter = Q()
        if self.subjects:
            query_filter &= Q(stage_subject__in=self.subjects)
        if self.start_time:
            query_filter &= Q(uploadtime__gte=self.start_time)
        if self.end_time:
            query_filter &= Q(uploadtime__lte=self.end_time)
        ex_resources = TikuExternalResource.objects.using(
            self.SOURCE_DB).filter(query_filter).order_by('pk')
        if limit:
            ex_resources = ex_resources[:limit]
        created_count = 0
        updated_count = 0
        with transaction.atomic(using=self.SOURCE_DB):
            with server_side_cursors(ex_resources, itersize=batch_size):
                for r in ex_resources.iterator():
                    source_key = ExResource.EXRESOURCE_SOURCE_TYPE_MAP.get(r.sourcetype)
                    if not source_key:
                        self.stdout.write('ignore ex_resource({c}) illegal source type({t})'.format(
                            c=r.code, t=r.sourcetype))
                        continue
                    r_dict = {
                        'code': r.code,
                        'content': r.content,
                        'type': r.type,
                        'stage_subject': r.stage_subject,
                        'label_code': r.labelcode,
                        'upload_time': r.uploadtime,
                        'extend_codes': self._get_extend_codes(r),
                    }
                    sync_r, created = ExResource.objects.update_or_create(code=r.code, defaults=r_dict)
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                    if (created_count + updated_count) % 1000 == 0:
                        self.stdout.write('sync {c} ex_resource records'.format(
                            c=created_count + updated_count))
        return created_count, updated_count

    def beforeMerge(self, cursor):
        pass


    def afterMerge(self, cursor):

        sql = 'update tiku_external_resource set download_num=0 where download_num is null;'
        cursor.execute(sql)
        sql = 'update tiku_external_resource set favorite_num=0 where favorite_num is null;'
        cursor.execute(sql)
        sql = 'update tiku_external_resource set view_num=0 where view_num is null;'
        cursor.execute(sql)

    def test(self):
        self.limit = 0
        self.start_time = None
        self.end_time = None
        self.subjects = None
        created_count, updated_count = self._sync_ex_resources( batch_size=1000)
        self.stdout.write('sync created {c} ex_resource records'.format(
            c=created_count))
        self.stdout.write('sync updated {c} ex_resource records'.format(
            c=updated_count))



if __name__ == '__main__':
    worker = PullFuxi()
    worker.test()
    #worker.run()
