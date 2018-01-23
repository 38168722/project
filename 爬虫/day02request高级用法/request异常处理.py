#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import *

try:
    r = requests.get('http://www.baidu.com',timeout=0.00001)
except ReadTimeout:
    print("========:")
except RequestException:
    print("Error")
