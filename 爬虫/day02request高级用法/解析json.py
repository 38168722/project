#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re

response = requests.get('http://httpbin.org/get')

import json
res1 = json.loads(response.text)
res2 = response.json()   #直接获取json数据

print('res1==',res1)
print('res2==',res2)
print(res1 == res2)
