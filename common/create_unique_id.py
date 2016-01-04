#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import os
id = '%s-%s' % (time.strftime('%Y%m%d-%H%M%S'), os.urandom(2).encode('hex'))
print id
