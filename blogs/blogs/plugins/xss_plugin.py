#!/usr/bin/env python
# -*- coding: utf-8 -*-

def filter_xss(html_str):
    black_list=["script","link"]
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_str,"html.parser")

    ####### 改成dict
    for ele in soup.find_all():
        #过滤非法标签
        if ele.name in black_list:
            ele.decompose()
    print(soup)

    return soup.decode()