#!/usr/bin/env python
# -*- coding:utf-8 -*-
import xlwt
import datetime

def saveExcel(knowledges, file_name):
    book = xlwt.Workbook()
    sheet = book.add_sheet(u'第一个sheet')
    for i ,row in enumerate(knowledges):
        for j, col in enumerate(row):
            sheet.write(i, j, str(col).decode('utf-8'))
    book.save(file_name)

if __name__ == "__main__":
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = '%s_%s.xls' % ("hello", time_str)
    saveExcel([["x1", "x2", "x3"],["yy1","y2"]], file_name)
