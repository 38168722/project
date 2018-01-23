#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser=webdriver.Chrome()
try:
    browser.get('http://mail.163.com/')
    wait=WebDriverWait(browser,5)
    frame=wait.until(EC.presence_of_element_located((By.ID,'x-URS-iframe')))
    browser.switch_to.frame(frame)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-container')))

    inp_user = browser.find_element_by_name('email')
    inp_pwd = browser.find_element_by_name('password')
    button = browser.find_element_by_id('dologin')
    inp_user.send_keys('m15313911386@163.com')
    inp_pwd.send_keys('cao123.com')
    button.click()
    wait.until(EC.presence_of_element_located((By.ID, 'dvNavTop')))
    write_msg = browser.find_elements_by_css_selector('#dvNavTop li')[1]  # 获取第二个li标签就是“写信”了
    write_msg.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tH0')))
    recv_man = browser.find_element_by_class_name('nui-editableAddr-ipt')
    title = browser.find_element_by_css_selector('.dG0 .nui-ipt-input')
    recv_man.send_keys('563312205@qq.com')
    title.send_keys('圣旨')
    print(title.tag_name)
    frame=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'APP-editor-iframe')))
    browser.switch_to.frame(frame)
    body=browser.find_element(By.CSS_SELECTOR,'body')
    body.send_keys('egon很帅，可以加工资了')

    browser.switch_to.parent_frame() #切回他爹
    send_button=browser.find_element_by_class_name('nui-toolbar-item')
    send_button.click()

    #可以睡时间久一点别让浏览器关掉，看看发送成功没有
    import time
    time.sleep(20)

except Exception as e:
    print(e)
finally:
    browser.close()