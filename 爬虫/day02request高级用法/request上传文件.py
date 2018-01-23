#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
files={'files':open('a.jpg','rb')}

response = requests.post('http://httpbin.org/post',files=files)

print(response.status_code)