#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests.packages import urllib3

response = requests.get('https://www.12306.cn',verify=False)
print(response.text)