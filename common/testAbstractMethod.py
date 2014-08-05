#!/usr/bin/env python
# -*- coding:utf-8 -*-

class A(object):
    def __init__(self):
        print "init A."

    def foo(self):
        raise NotImplementedError("Please Implement this method")

class B(A):
    def __init__(self):
        A.__init__(self)
        print "init B."

    def foo(self):
        print "foo in B."

if __name__ == '__main__':
    a = B()
    a.foo()
