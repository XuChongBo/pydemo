#!/usr/bin/env python
# -*- coding:utf-8 -*-

class MyClass():
    a = '123'

    @staticmethod
    def foo():
        print MyClass.a
        print 'in foo()'

if __name__ == '__main__':
    MyClass.foo()
