#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)
app.config['templates_auto_loads']=True

app.route("/")
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
