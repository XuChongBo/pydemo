# -*- coding: utf-8 -*-

import os
import stat
import fcntl
import time
from lock import ExLock

with ExLock("doc2pdf2swf"):
    print "got it"
    time.sleep(10)
