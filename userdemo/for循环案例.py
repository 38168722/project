#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,render_template

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

@app.route('/')
def index():
    user={
        'username':'黄帝',
        'age':18
    }
    books=[
        {
            "name":"三国演义",
            "author":"罗贯中",
            "price":100,
         },
        {
            "name":"红楼梦",
            "author":"曹雪芹",
            "price":200,
         },
        {
            "name":"西游记",
            "author":"吴承恩",
            "price":500,
         },
        {
            "name":"水浒传",
            "author":"施耐庵",
            "price":100,
         },
    ]

    websites=["wwww.baidu.com","www.google.com"]
    # avatar="http://imgsrc.baidu.com/image/c0%3Dshijue1%2C0%2C0%2C294%2C40/sign=d2d2d79494510fb36c147fd4b15aa2e0/0e2442a7d933c895e55c0156db1373f0820200f8.jpg"
    return render_template('index.html',user=user,websites=websites,books=books)

if __name__ == '__main__':
    app.run()