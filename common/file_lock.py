# -*- coding: utf-8 -*-

import os
import stat
import fcntl
import time


class LockException(Exception):
    pass


class ExLock(object):
    def __init__(self, lock_name):
        self._lock_file = '/tmp/%s.lock' % (lock_name)
        self._fd = None

    def acquire(self):
        self._fd = os.open(self._lock_file, os.O_RDWR | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
        for i in range(10):
            try:
                fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except (IOError, OSError) as e:
                print "Attemp acquire exclusive lock error (%s) " % e
                time.sleep(1)
        else:
            os.close(self._fd)
        raise LockException("To long waitting for exclusive lock .")


    def release(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)
        os.close(self._fd)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._fd:
            self.release()
            self._fd = None

    def __del__(self):
        if self._fd:
            self.release()
