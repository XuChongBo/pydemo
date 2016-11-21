#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json

data = {'xame': 'letian'}
#data = {'name': 'letian'}
headers = {'content-type': 'application/json'}
r = requests.post("http://0.0.0.0:5000/json", data=json.dumps(data), headers=headers)
print dir(r)
print r.status_code
print r.content
print r.headers
print r.json()
