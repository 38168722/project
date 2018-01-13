#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)



@app.route('/')
def index():
    print(url_for("my_list"))
    print(url_for('article',id='123'))
    return "hello world"

@app.route("/list/")
def my_list():
    return "list"

@app.route('/article/<id>')
def article(id):
    return "您请求的参数是%s"%id

if __name__ == '__main__':
    app.run()
