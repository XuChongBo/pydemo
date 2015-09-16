#!/usr/bin/env python

import sys
import os.path
import time
import urllib2
import lmdb


def check_ok(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        print response
        return True
    except:
        return False


if __name__ == '__main__':
    the_url = "http://www.baidu.com"
    print check_ok(the_url)

