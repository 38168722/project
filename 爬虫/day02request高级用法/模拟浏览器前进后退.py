#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.get('https://www.taobao.com')
browser.get('https://www.sina.com.cn')

browser.back()
time.sleep(10)
browser.forward()
browser.close()


