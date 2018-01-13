#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,session
import os

app=Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)

@app.route('/')
def hello_world():
    session['username']='zhiliao'
    return 'Hello world'

@app.route('/get/')
def get():
    username=session.get('username')
    return username

@app.route('/delete/')
def delete():
    print(session.get('username'))
    session.pop('username')
    print(session.get('username'))
    return "success"

@app.route('/clear/')
def clear():
    print(session.get('username'))
    #删除session中的所有数据
    session.clear()
    print(session.get('username'))
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)