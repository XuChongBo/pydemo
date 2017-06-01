# -*- coding: utf-8 -*-

import os
import stat
import fcntl
import time
from file_lock import ExLock

try:
    with ExLock("doc2pdf2swf"):
        print "got it"
except LockException as e:
    print e
