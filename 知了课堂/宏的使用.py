#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for,render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True


@app.route('/')
def index():
    return  render_template("index/macro.html")

if __name__ == '__main__':
    app.run(debug=True)
