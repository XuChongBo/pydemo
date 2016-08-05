#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


from subprocess import Popen, PIPE
from tempfile import SpooledTemporaryFile as tempfile
f = tempfile()
f.write('one\ntwo\nthree\nfour\nfive\nsix\n')
f.seek(0)
print Popen(['/bin/grep','five'],stdout=PIPE,stdin=f).stdout.read()
f.close()

