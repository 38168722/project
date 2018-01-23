#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
response=requests.get('http://www.autohome.com/news')
response.encoding="gbk"
with open('auto.html','w') as f:
    for item in response.text:
        f.write(item)

