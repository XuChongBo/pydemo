# coding: utf-8

from dbsync.core.SyncBase import SyncBase
import os


from django.conf import settings
settings.DEBUG = False
from metadata.models import Chapter, PaperGroup
from resourcedata.models import ExternalResource


def associate_chapter_resource():
    chapters = Chapter.objects.all()
    for chapter in chapters:
        resources = ExternalResource.objects.filter(
            parent_code=chapter.code)
        for resource in resources:
            chapter.resources.add(resource)


def associate_paper_resource():
    paper_groups = PaperGroup.objects.all()
    for paper_group in paper_groups:
        resources = ExternalResource.objects.filter(
            parent_code=paper_group.code)
        for resource in resources:
            paper_group.resources.add(resource)


def clean_tables(cursor):
    tables = [
        'tiku_book_version', 'tiku_cate_mapping', 'tiku_chapter',
        'tiku_chapter_resources', 'tiku_external_resource', 'tiku_grade',
        'tiku_label', 'tiku_location', 'tiku_paper_group',
        'tiku_paper_group_resources',
        'tiku_paper_type', 'tiku_stage_subject']
    for table in tables:
        sql = 'truncate %s cascade' % table
        cursor.execute(sql)


def insert_locations(cursor):
    locations = [('北京市', '110000'), ('天津市', '120000'),
                 ('河北省', '130000'), ('山西省', '140000'),
                 ('内蒙古自治区', '150000'), ('辽宁省', '210000'),
                 ('吉林省', '220000'), ('黑龙江省', '230000'),
                 ('上海市', '310000'), ('江苏省', '320000'),
                 ('浙江省', '330000'), ('安徽省', '340000'),
                 ('福建省', '350000'), ('江西省', '360000'),
                 ('山东省', '370000'), ('河南省', '410000'),
                 ('湖北省', '420000'), ('湖南省', '430000'),
                 ('广东省', '440000'), ('广西壮族自治区', '450000'),
                 ('海南省', '460000'), ('重庆市', '500000'),
                 ('四川省', '510000'), ('贵州省', '520000'),
                 ('云南省', '530000'), ('西藏自治区', '540000'),
                 ('陕西省', '610000'), ('甘肃省', '620000'),
                 ('青海省', '630000'), ('宁夏回族自治区', '640000'),
                 ('新疆维吾尔自治区', '650000'), ('台湾省', '710000'),
                 ('香港特别行政区', '810000'), ('澳门特别行政区', '820000'),
                 ('海外', '10000020')]
    sql = 'INSERT INTO tiku_location (name, code) VALUES (%s, %s)'
    cursor.executemany(sql, locations)


class PullPangu(SyncBase):
    def __init__(self):
        task_dir = os.path.dirname(__file__)
        super(PullPangu, self).__init__(task_dir) 

    def after(self, cursor):
        sql = """INSERT INTO tiku_chapter_resources(chapter_id,externalresource_id) 
               select a.id,b.id from tiku_chapter as a inner join  tiku_external_resource as b 
               on b.parent_code=a.code;"""
        cursor.execute(sql)
        sql = """INSERT INTO tiku_paper_group_resources(papergroup_id,externalresource_id) 
               select a.id,b.id from tiku_paper_group as a inner join  tiku_external_resource as b 
               on b.parent_code=a.code;"""
        cursor.execute(sql)
        print 'associated'

    def before(self, cursor):
        clean_tables(cursor)
        insert_locations(cursor)
        print 'initialized'


######## usage ############
# worker = PullPangu()
# worker.run()
####################
