#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
d = {}
x = d.setdefault("a",[])
x.append(12)
print d
x = d.setdefault("a",[])
x.append(13)
print d

