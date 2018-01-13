#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,views

app=Flask(__name__)

def auth(func):
    def inner(*args,**kwargs):
        result = func(*args,**kwargs)
        return result
    return inner

class IndexView(views.MethodView):
    methods = ["GET","POST"]
    decorators = [auth,]

    def get(self):
        return "GET"

    def post(self):
        return "POST"

app.add_url_rule('/index',view_func=IndexView.as_view(name='index'))

if __name__ == '__main__':
    app.run()

