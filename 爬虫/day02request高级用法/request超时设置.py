#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

response = requests.get('https://www.baidu.com',timeout=0.01)
print(response.status_code)