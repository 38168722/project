#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

driver=webdriver.Chrome()
driver.get('https://www.baidu.com')
try:
    wait=WebDriverWait(driver,10)
    login = driver.find_element_by_link_text('登录')
    login.click()
    # print(driver.find_element_by_tag_name('a'))
    # 6 find_element_by_name
    input_user=wait.until(EC.presence_of_element_located((By.NAME,'userName')))
    input_pwd=wait.until(EC.presence_of_element_located((By.NAME,'password')))
    commit = wait.until(EC.element_to_be_clickable((By.ID, 'TANGRAM__PSP_10__submit')))
    input_user.send_keys('15217897782')
    input_pwd.send_keys('lhf@12321321')
    commit.click()
finally:
    driver.close()