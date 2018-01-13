#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,session,Session,flash,get_flashed_messages,redirect,render_template,request
app = Flask(__name__)
app.secret_key ='sdfsdfsdf'

@app.before_request
def process_request1():
    print('process_request1')

@app.after_request
def process_response1(response):
    print('process_response1')
    return response

@app.before_request
def process_request2(response):
    print("process_request2")

@app.after_request
def process_response2(response):
    print("process_response2")
    return response

@app.route('/index')
def index():
    print("index")
    return "Index"




if __name__ == '__main__':
    app.run()