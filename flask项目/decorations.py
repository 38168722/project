#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import redirect,url_for,session
from functools import wraps
#登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('hello world')
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return wrapper