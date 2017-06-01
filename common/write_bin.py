#!/usr/bin/env python
# -*- coding:utf-8 -*-



img_data = base64.b64decode(d['imageData'])
with open('skin.png', "wb") as fd:
    fd.write(img_data)
