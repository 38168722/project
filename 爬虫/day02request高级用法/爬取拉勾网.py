#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re

session = requests.session()

r1 = session.get('https://login.51job.com/login.php?lang=c',
                 headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                 },
                 )

r2=session.post('https://login.51job.com/login.php?lang=c',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                    'Referer':'https://login.51job.com/login.php?lang=c',
                },
                data={
                    "lang":"c",
                    "action":"save",
                    "from_domain":"i",
                    "loginname":"caoxing2018",
                    "password":"cao123.com",
                    "verifycode":'',
                    "isread":"on",
                },
                )

r6=session.get('http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&keyword=C%2B%2B%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9',
                 headers={
                        'Referer':'http://search.51job.com/list/',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                 },
                  # data={
                  #       'lang':'c',
                  #       'stype':'2',
                  #       'postchannel':'0000',
                  #       'fromType':'1',
                  #       'line':'',
                  #       'confirmdate':'9',
                  #       'from':'',
                  #       'keywordtype':'2',
                  #       'jobarea':'010000',
                  #       'keyword':'(unable to decode value)',
                  #       'industrytype':'',
                  #       'funtype':'',
                  # },
                  # params={
                  #       'fromJs':'1',
                  #       'jobarea':'010000',
                  #       'keyword':'C++开发工程师',
                  #       'keywordtype':'2',
                  #       'lang':'c',
                  #       'stype':'2',
                  #       'postchannel':'0000',
                  #       'fromType':'1',
                  #       'confirmdate':'9',
                  # },

                )

from pprint import pprint
r6.encoding="gbk"
# print(r6.text)
comapines_list=re.findall('name="delivery_jobid".*?value="(.*?)".*?title="(.*?)".*?href="(.*?)".*?class="t2".*?title="(.*?)".*?class="t4">(.*?)</span>',r6.text,re.S)
for company in comapines_list:
    positionId=company[0]
    job=company[1]
    company_link=company[2]
    company_name=company[3]
    salary=company[4]
    print("""
    职位ID:%s
    职位名:%s
    公司链接:%s
    公司名:%s
    薪资:%s
    """%(positionId,job,company_link,company_name,salary))
    r7=session.get(company_link,
                   headers={
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                        'Referer': 'http://jobs.51job.com/beijing-cyq/97923399.html?s=01&t=0',
                    }
                   )
    session.get('http://i.51job.com/delivery/delivery.php',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'Referer': 'http://jobs.51job.com/beijing-cyq/97923399.html?s=01&t=0',
                },
                params={
                    'jobid':positionId,
                    'deliverytype':1,
                }
                )
    print('%s 投递成功'%(company_name))