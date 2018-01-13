#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,session,url_for

app = Flask(__name__)
app.config['SERVER_NAME']='bjg.com:5000'

@app.route("/index",subdomain='<hello>')
def index(hello):
    return "%s.bjg.com"%(hello)

if __name__ == '__main__':
    app.run()