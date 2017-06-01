#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import base64

#data = {'name': 'letian'}
#headers = {'content-type': 'application/json'}
#url = 'http://192.168.43.193:110/seg_hair_upload_json'
url = 'http://172.1.3.3:110/seg_hair_upload_json'
#filename = '/3T/images/x.png'
filename = '/3T/images/helen/helen_1/288344083_1.jpg'
files = {'imagefile': open(filename, 'rb')}
r = requests.post(url, data={}, files=files)
#r = requests.post(url, data={}, files={'magefile':('xxx.jpg', opem(filename, 'rb'))})
print dir(r)
print r.status_code
print r.content
print r.headers
d = r.json()
img_data = base64.b64decode(d['imageData'])

with open('out.png', "wb") as fd:
    fd.write(img_data)

