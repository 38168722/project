#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re

#第一次请求
r1 = requests.get('https://github.com/login')
r1_cookie=r1.cookies.get_dict()
authenticity_token = re.findall(r'name="authenticity_token".*?value="(.*?)"',r1.text)[0]

#第二次请求，带着初始cookie和token发送post请求给登录页面

data={
    'commit':'Sign in',
    'utf8':'✓',
    'authenticity_token':authenticity_token,
    'login':'38168722@qq.com',
    'password':'cao123.com',
}

r2 = requests.post('https://github.com/session',
                   data=data,
                   cookies=r1_cookie,
                   allow_redirects=False,
                   )

print(r2.status_code)
print(r2.url)
print(r2.history)
# print(r2.history[0].text)
