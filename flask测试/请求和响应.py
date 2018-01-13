#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,request,redirect,render_template,jsonify,make_response
from urllib.parse import urlencode,quote,unquote
app = Flask(__name__)
@app.route('/index',endpoint='xx')
def index():
    from werkzeug.datastructures import ImmutableMultiDict
    response = make_response('hello world')
    response.headers['desc']='this is descible'
    return response

if __name__ == '__main__':
    app.run(debug=True)