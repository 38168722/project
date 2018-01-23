#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re
session = requests.session()

r1 = session.get('https://passport.lagou.com/login/login.html',
                 headers={
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                 },
                 )

X_Anti_Forge_Token = re.findall("X_Anti_Forge_Token = '(.*?)'", r1.text, re.S)[0]
X_Anti_Forge_Code = re.findall("X_Anti_Forge_Code = '(.*?)'", r1.text, re.S)[0]
# print("X_Anti_Forge_Token",X_Anti_Forge_Token)
# print("X_Anti_Forge_Code",X_Anti_Forge_Code)

r2 = session.post('https://passport.lagou.com/login/login.json',
                  headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                      'Referer': 'https://passport.lagou.com/login/login.html',
                      'X-Anit-Forge-Code': X_Anti_Forge_Code,
                      'X-Anit-Forge-Token': X_Anti_Forge_Token,
                      'X-Requested-With': 'XMLHttpRequest'
                  },
                  data={
                      "isValidate": True,
                      'username': '18611453110',
                      'password': '70621c64832c4d4d66a47be6150b4a8e',
                      'request_form_verifyCode': '',
                      'submit': ''
                  }
                  )


r3=session.get('https://passport.lagou.com/grantServiceTicket/grant.html',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer': 'https://passport.lagou.com/login/login.html',
            }
            )


r4=session.get('https://www.lagou.com/resume/myresume.html',
               headers={
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               }
               )

print('18611453110' in r4.text)