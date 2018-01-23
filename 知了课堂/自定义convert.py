#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for
from werkzeug.routing import BaseConverter

# 一个url中，含有手机号码的变量，必须限定这个变量的字符串格式满足手机号码格式
class TelephoneConveter(BaseConverter):
    regex=r'\d{11}'

class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')

    def to_url(self, value):
        print("value",value)
        return "+".join(value)

app = Flask(__name__)

app.url_map.converters['tel']=TelephoneConveter
app.url_map.converters['list']=ListConverter

@app.route('/user/<int:user_id>/')
def user_profile(user_id):
    return '您输入的user_id为%s'%user_id

@app.route('/telephone/<tel:tel>/')
def telephone(tel):
    return '您输入的手机号码为%s'%tel

@app.route('/bankuai/<list:boards>/')
def posts(boards):
    return "您提交的版块是:%s"%boards

@app.route('/')
def index():
    # print(url_for('posts',boards=['a','b']))
    return "hello world",404


if __name__ == '__main__':
    app.run(debug=True)