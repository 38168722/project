#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import requests
# response = requests.get('http://www.baidu.com')
# with open('baidu.html','w',encoding="utf8") as f:
#     f.write(response.text)

#在请求头内将自己伪装成浏览器.
# response=requests.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=python',
#                       headers={
#                         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#                       })
#
# with open('baidu.html','w',encoding='utf-8') as f:
#     for item in response.text:
#         f.write(item)

#上述操作可以用requests模块的一个params参数搞定

from urllib.parse import urlencode
import requests,re
# wd='egon老师'
# pn=1
#
#
# response=requests.get('https://www.baidu.com/s',
#                       params={
#                        'wd':wd,
#                        'pn':pn
#                       },
#                       headers={
#                         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
#                       }
#                       )
#
# res2=response.text
#
# with open('a.html','w',encoding='utf-8') as f:
#     f.write(res2)

import requests
# response=requests.get("https://www.zhihu.com/explore",
#                       headers={
#                         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#                       }
#                       )
# print(response.status_code)


# Cookies={'user_session':'0YSajQOw_TiIMzc2A5FhQUyJHsYyjpuz_Ib1ZvpgCk1YpTzk',}
# response=requests.get('https://github.com/settings/emails',cookies=Cookies)
# print('38168722@qq.com' in response.text)

# r1 = requests.get('https://github.com/login')
# r1_cookie=r1.cookies.get_dict()   #拿到初始cookie(未被授权)
# authenticity_token=re.findall(r'name="authenticity_token".*?value="(.*?)"',r1.text)[0]
#
# data={
#     'commit':'Sign in',
#     'utf8':'✓',
#     'authenticity_token':authenticity_token,
#     'login':'38168722@qq.com',
#     'password':'cao123.com'
# }
#
# r2=requests.post('https://github.com/session',data=data,cookies=r1_cookie)
#
# login_cookie=r2.cookies.get_dict()
#
# r3 = requests.get('https://github.com/settings/emails',cookies=login_cookie)
#
# print('38168722@qq.com' in r3.text)

session = requests.session()
#第一次请求
r1 = session.get('https://github.com/login')
authenticity_token=re.findall(r'name="authenticity_token".*?value="(.*?)"',r1.text)[0]

#第二次请求
data={
    'commit':'Sign in',
    'utf8':'✓',
    'authenticity_token':authenticity_token,
    'login':'38168722@qq.com',
    'password':'cao123.com'
}

r2=session.post('https://github.com/session',data=data,)

r3=session.get('https://github.com/settings/emails')
print("38168722@qq.com" in r3.text)



