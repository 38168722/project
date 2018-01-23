#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode

# response = requests.get('https://www.taobao.com',
#                         headers={
#                             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#                         },
#                         )
#
# with open('a.html','w',encoding='utf-8') as f:
#     f.write(response.text)

# response = requests.get(url='https://github.com/settings/emails',
#                         headers={
#                             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#                         },
#                         cookies={
#                             "k1":"v1",
#                         }
#                         )
#
# print(response.text)


import requests
import re
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(50)
movie_path=r'C:\mp4'

def get_page(url):
    response=requests.get(url)
    try:
        if response.status_code==200:
            print("response.content==",response.content)
            print("response.text==",response.text)
            return response.text
    except Exception:
        pass

# def parse_index(content):


abc=get_page('http://www.qq.com')
