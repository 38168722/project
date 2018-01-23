#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

browser = webdriver.Chrome()

try:
    browser.get('https://www.baidu.com')
    input_tag=browser.find_element_by_id('kw')
    input_tag.send_keys('美女')
    input_tag.send_keys(Keys.ENTER)
    wait=WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.page_source)
    print(browser.current_url)
    print(browser.get_cookies())

finally:
    browser.close()
