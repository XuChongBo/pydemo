#!/usr/bin/env python
# -*- coding:utf-8 -*-



import codecs
filepath = "xx.txt"

with codecs.open(filepath, "r", 'utf-8') as myfile:
    for line in myfile:
        with codecs.open("new.txt", "w", 'utf-8') as myfile:
            myfile.write(u"".join(line))
