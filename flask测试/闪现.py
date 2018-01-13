#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,session,Session,flash,get_flashed_messages,redirect,render_template,request
app = Flask(__name__)
app.secret_key="fdsafdsafdsafdsa"

@app.route('/users')
def users():
    v = get_flashed_messages()
    print(v)
    msg=""
    return render_template('user.html',msg=msg)

@app.route("/useradd")
def user_add():
    flash("添加成功")
    return redirect("/users")

if __name__ == '__main__':
    app.run()