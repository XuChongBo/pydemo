#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

import pipes
import tempfile

p = pipes.Template()
p.debug(True)
#p.append('unoconv -f pdf -o $OUT $IN', 'ff')
p.append('grep one  $IN  >  $OUT ', 'ff')

t = tempfile.NamedTemporaryFile('w+r')
t.write('one\ntwo\nthree\nfour\nfive\nsix\n')
t.seek(0)

p.copy(t.name, "/tmp/a.pdf")  # 'ff' $IN $OUT

t.close()
