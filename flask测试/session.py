#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,session,Session
from urllib.parse import urlencode,quote,unquote
from werkzeug.local import LocalProxy
app = Flask(__name__)
app.secret_key="fdsafdsfdsa"
app.config["SESSION_COOKIE_NAME"]="session_lvning"

@app.route('/index',endpoint='xx')
def index():
    session['xx3']=123
    return 'xxxx'

if __name__ == '__main__':
    app.run()