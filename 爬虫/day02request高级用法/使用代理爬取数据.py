#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
proxies={
    'http':'http://123.207.25.143:3128',
    'http':'http://114.115.140.25:3128',
}

response = requests.get('https://www.12306.cn',proxies=proxies,verify=False)

print(response.status_code)