#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,redirect

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

@app.route('/')
def index():
    url=url_for("login")
    return redirect(url)

@app.route('/login/')
def login():
    return "这是登录页面"

@app.route('/question/<is_login>/')
def question(is_login):
    if is_login=="1":
        return "这是发布问答页面"
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
