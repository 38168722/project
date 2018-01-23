#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for,views,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    print(url_for('zhiliao'))
    return " index home"

def my_list():
    return "我是列表项"

class JSONView(views.View):
    def get_data(self):
        raise NotImplementedError

    def dispatch_request(self):
        return jsonify(self.get_data())

class ListView(JSONView):
    def get_data(self):
        return {"username":"zhiliao",'password':'111111'}


app.add_url_rule('/list/',endpoint='zhiliao',view_func=ListView.as_view('list'))

if __name__ == '__main__':
    app.run(debug=True)
