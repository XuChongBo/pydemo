#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

import pipes
import tempfile

p = pipes.Template()
p.debug(True)
p.append('grep f $IN  $OUT', 'ff')

t = tempfile.NamedTemporaryFile('w+r')

t1 = tempfile.NamedTemporaryFile('w+r')

t1.write('one\ntwo\nthree\nfour\nfive\nsix\n')
t1.seek(0)

p.copy(t1.name, t.name)

t.seek(0)
print t.read()
t.close()
t1.close()
