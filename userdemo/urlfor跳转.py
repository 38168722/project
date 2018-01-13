#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,render_template

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # return "hello world"
    return render_template("login.html")

if __name__ == '__main__':
    app.run()