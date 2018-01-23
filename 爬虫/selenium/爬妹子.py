#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,re

response=requests.get('http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%C7%E5%B4%BF%C3%C0%C5%AE&fr=ala&ala=1&alatpl=cover&pos=0&hs=2&xthttps=000000')

# name="delivery_jobid".*?value="(.*?)
response.encoding="gbk"
pic=re.findall(r'.*?data-imgurl="(.*?)"',response.text,re.S)
print(pic)


