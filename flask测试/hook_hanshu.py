#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

@app.before_request
def my_before_request():
    print("在request之前执行")

@app.route('/login/')
def login():
    return 'login'

if __name__ == '__main__':
    app.run(debug=True)