#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,time,hashlib

def get_page(url):
    print('GET %s'%url)
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass

def parse_index(index_page):
    urls=re.findall('class="items".*?href="(.*?)"',index_page.decode("gbk"),re.S)
    for url in urls:
        if not url.startswith('http'):
            url='http://www.xiaohuar.com'+url
        yield url

def parse_detail(res):
    print("进来detail了没")
    obj = re.compile('id="media".*?src="(.*?)"',re.S)
    res = obj.findall(res.decode('gbk'))
    print("匹配的视频==",res)
    if len(res)>0:
        movie_url=res[0]
        if movie_url.endswith(".mp4"):
            return movie_url

def save(movie_url):
    print("进来了没有")
    response=requests.get(movie_url,stream=False)
    print(response.status_code)
    if response.status_code==200:
        m=hashlib.md5()
        m.update(('%s%s.mp4'%(movie_url,time.time())).encode('utf-8'))
        filename=m.hexdigest()
        print("filename=%s"%filename)
        with open(r'C:/movie/%s.mp4'%filename,'wb') as f:
            f.write(response.content)
            f.flush()

def main():
    index_url='http://www.xiaohuar.com/list-3-{0}.html'
    for i in range(1,4):
        print('*'*50,i)
        #爬取主页面
        index_page=get_page(index_url.format(i))
        #解析主页面，拿到视频所在的地址列表
        detail_urls=parse_index(index_page)
        #循环爬取视频页
        for detail_url in detail_urls:
            #爬取视频页
            detail_page=get_page(detail_url)
            #拿到视频的url
            movie_url=parse_detail(detail_page)
            if movie_url:
                #保存视频
                save(movie_url)

if __name__ == '__main__':
    main()