#!/usr/bin/env python
# -*- coding: utf-8 -*
from flask import Flask,render_template

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

@app.route('/login/<is_login>/')
def index(is_login):
    if is_login=="1":
        user={
            'username':'黄勇',
            'age':21
        }
        return render_template('index.html',user=user)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()