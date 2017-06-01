#!/usr/bin/env python

import sys
import os.path
import time
import urllib2
import lmdb

import requests

proxies = {
  "http": "socks5://wan:bjyxj@10.7.20.15:443",
  "https": "http://10.4.29.15:443/",

}

"""
proxies = {
  "http": "sg-rs.gfw.io:443",
  "https": "rs.gfw.io:443",

}
from requests.auth import HTTPProxyAuth
auth = HTTPProxyAuth('wan', 'bjy')
headers = {"Connection": "close"}
r = requests.get("http://stackoverflow.com/", proxies=proxies, auth=auth, headers=headers)
"""

from requests.auth import HTTPProxyAuth
"""
auth = HTTPProxyAuth('wan', 'by')
urllib2.ProxyHandler({'http': 'http://user:pass@proxy:328'}))
"""
r=requests.get("http://www.google.co.jp", proxies=proxies)
print r
#r=requests.get("https://google.com", proxies=proxies)
print r.text
