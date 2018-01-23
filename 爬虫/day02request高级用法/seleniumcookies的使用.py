#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver

browser=webdriver.Chrome()

browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
browser.add_cookie({'k1':'xxxxx','k2':'yyyy'})
print(browser.get_cookies())