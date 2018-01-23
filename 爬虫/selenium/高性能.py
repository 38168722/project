#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

def parse_page(res):
    print("解析 %s"%(len(res)))

def get_page(url):
    print('下载 %s'%url)
    response=requests.get(url)
    if response.status_code==200:
        return response.text

if __name__ == '__main__':
    urls=['https://www.baidu.com/','http://www.sina.com.cn/','https://www.python.org']
    for url in urls:
        res=get_page(url)
        parse_page(res)

