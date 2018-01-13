#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,redirect,render_template

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

class Person(object):

    def __init__(self,name,age):
        self.name=name
        self.age=age


@app.route('/')
def index():
    p=Person("黄勇",33)
    context={
        'username':'知了课堂',
        'gender':'男',
        'age':18,
        'person':p,
    }

    return render_template("index.html",**context)

if __name__ == '__main__':
    app.run()
