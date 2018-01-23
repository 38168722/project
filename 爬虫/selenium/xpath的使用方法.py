#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素

browser=webdriver.Chrome()

browser.get('https://www.amazon.cn/ref=z_cn?tag=zcn0e-23')
wait=WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.ID,'cc-lm-tcgShowImgContainer')))

tag=browser.find_element(By.CSS_SELECTOR,'#cc-lm-tcgShowImgContainer img')

print(tag.get_attribute('src'))

print("tag.id",tag.id)
print("tag.location",tag.location)
print("tag.tag_name",tag.tag_name)
print("tag.size",tag.size)
browser.close()