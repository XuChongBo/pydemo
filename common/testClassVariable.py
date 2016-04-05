#!/usr/bin/env python
# -*- coding:utf-8 -*-

class MyClass():
    a = '123'
    @staticmethod
    def foo():
        print MyClass.a
        print 'in foo()'

    @staticmethod
    def putclass():
	c = MyClass()
	MyClass.c = c 
	c.a = "the statict instance c"

b = MyClass()
MyClass.b = b
b.a = "the statict instance b"
MyClass.putclass()
if __name__ == '__main__':
    MyClass.foo()
    x = MyClass()
    print x.a
    print MyClass.b.a
    print MyClass.c.a
"""
>>> m = MyClass()
>>> m.i = 4
>>> MyClass.i, m.i
>>> (3, 4)
"""
