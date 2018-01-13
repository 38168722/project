#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,request,redirect,render_template,jsonify,make_response,Markup
from urllib.parse import urlencode,quote,unquote
app = Flask(__name__)

def tst(a1,a2):
    return a1+a2

@app.template_global
def sb(a1,a2):
    return a1+a2+100

@app.template_filter
def db(a1,a2,a3):
    return a1+a2+a3

@app.route('/index',endpoint='xx')
def index():
    v1="字符串"
    v2=[11,22,33]
    v3={"k1":"v1","k2":"v2"}
    v4=Markup("<input type='text'>")
    return render_template('index.html',v1=v1,v2=v2,v3=v3,v4=v4,tr=tst)

if __name__ == '__main__':
    app.run()