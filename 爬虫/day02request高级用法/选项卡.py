#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')

print(browser.window_handles)  #获取所有的选项卡
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(10)
browser.switch_to.window(browser.window_handles[0])
browser.get('https://www.sina.com.cn')
browser.close()

