#!/usr/bin/env python
import urllib2
proxies = {
  "http": "http://wan:bj@103.47.209.155:443/",
  "https": "https://10.15.10.8:2630",

}
proxy = urllib2.ProxyHandler(proxies)
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

conn = urllib2.urlopen('https://www.baidu.com/')
return_str = conn.read()
