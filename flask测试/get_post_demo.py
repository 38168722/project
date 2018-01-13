#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,session,redirect,url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)

@app.route('/')
def index():
    return render_template('login.html')

# 如果你想采用post请求，那么要写明
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username =='zhiliao' and password=='111111':
            session['username']='zhiliao'
            return "登陆成功"
        return '登陆失败'

@app.route('/search/')
def search():
    return 'search'


@app.route('/edit/')
def edit():
    if session.get('username'):
        return u'修改成功'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)