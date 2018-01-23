#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,url_for

from user import user

app = Flask(__name__)
app.config['SERVER_NAME']='wo.com:5000'
app.register_blueprint(user.bp)

@app.route("/")
def home():
    print(url_for('user.index'))
    return "this is homepage"

if __name__ == '__main__':
    app.run(debug=True)
