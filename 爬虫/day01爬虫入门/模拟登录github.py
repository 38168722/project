#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,requests

r1 = requests.get('https://github.com/login',
                  headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                  },)

authenticity_token = re.findall('name="authenticity_token".*?value="(.*?)"', r1.text, re.S)[0]
r1_cookies=r1.cookies.get_dict()
print("r1_cookies==%s"%r1_cookies)
print(authenticity_token)


r2 = requests.post('https://github.com/session',
                   headers={
                       "Referer": "https://github.com/",
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                   },
                   cookies=r1_cookies,
                   data={
                       "commit": "Sign in",
                       'utf8': "✓",
                       "authenticity_token": authenticity_token,
                       "login": "38168722@qq.com",
                       "password": "cao123.com",
                   },
                   allow_redirects=False
                   )

cookies=r2.cookies.get_dict()
print("post cookie==%s"%cookies)
r3=requests.get('https://github.com/settings/emails',
             headers={
                 "Referer": "https://github.com/",
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
             },
             cookies=cookies)
print("r3.text==",r3.text)
print('38168722@qq.com' in r3.text)