#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
response=requests.get('http://www.jianshu.com')
# print(response.text)
print("response.status_code",response.status_code)
print("response.headers",response.headers)
print("response.cookies",response.cookies)
print("response.cookies.get_dict()",response.cookies.get_dict())
print("response.cookies.items()",response.cookies.items())
print("response.url",response.url)
print("response.history",response.history)
print("response.encoding",response.encoding)