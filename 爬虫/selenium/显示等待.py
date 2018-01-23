#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素

browser=webdriver.Chrome()
browser.get('https://www.baidu.com')

input_tag=browser.find_element_by_id('kw')
input_tag.send_keys('清纯美女')
time.sleep(5)
input_tag.clear()
input_tag.send_keys('霸气美女')
input_tag.send_keys(Keys.ENTER)

wait=WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.ID,'content_left')))

contents=browser.find_element(By.CSS_SELECTOR,"#content_left")

import time
time.sleep(10)
browser.close()
