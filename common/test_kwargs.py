#!/usr/bin/env python
# -*- coding:utf-8 -*-

def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}".format(key, value))

greet_me( a=3, b=6, **{'x': 4, 'y':56})
