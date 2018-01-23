#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect,url_for,render_template
from datetime import datetime
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

@app.route('/index/')
def ceshi():
    data={
        "name":"张三",
        "age":-18,
        "children":{"name":"小三","age":18},
        "sex":None,
        'create_time':datetime.now(),
    }
    abc='<script>alert("hello wolrd")</script>'

    return render_template("index.html",**data,abc=abc)

@app.route("/login/")
def login():
    return "登陆成功咯"

@app.template_filter('cut')
def cut(value):
    value=value.replace("hello",'')
    return value

@app.template_filter('handle_time')
def handle_time(time):
    if isinstance(time,datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp<60:
            return "刚刚"
        elif timestamp>=60 and timestamp<60*60:
            minutes=timestamp/60
            return "%s分钟前"%int(minutes)
    else:
        return time






if __name__ == '__main__':
    app.run(debug=True)

