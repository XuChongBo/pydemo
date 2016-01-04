#!/usr/bin/env python
# -*- coding:utf-8 -*-
class Foo(object):
  def __init__(self, val=2):
     self.val = val

  def __getstate__(self):
     print "I'm being pickled"
     self.val *= 2
     return self.__dict__

  def __setstate__(self, d):
     print "I'm being unpickled with these values:", d
     self.__dict__ = d
     self.val *= 3

import pickle
f = Foo()
print f.val
f_string = pickle.dumps(f)
print f.val
f_new = pickle.loads(f_string)
print f_new.val
