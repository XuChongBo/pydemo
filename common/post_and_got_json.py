#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import urllib2,json

url = 'http://192.168.100.22:7001/stroke_sequences'
postdata = {'key':'value', 'a':344,'b':55}

req = urllib2.Request(url)
req.add_header('Content-Type','application/json')
data = json.dumps(postdata)

response = urllib2.urlopen(req,data)
s = response.read()   # take care!!!  the response should be read only once!!
print s
print json.loads(s)
