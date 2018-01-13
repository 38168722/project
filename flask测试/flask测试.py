# from flask import Flask, request, render_template, session, redirect
# from functools import wraps
# from werkzeug.wrappers import Request,Response
# import flask
# import django
# app = Flask(__name__)
# app.secret_key="flkjdslkfadlksafds"
#
# def auth(func):
#     @wraps(func)
#     def inner(*args,**kwargs):
#         if not session.get('userinfo'):
#             return redirect('/login')
#         ret=func(*args,**kwargs)
#         return ret
#     return inner
#
# @app.route("/login",methods=["GET","POST"])
# def login():
#     if request.method=="GET":
#         return render_template("login.html")
#     else:
#         username=request.form.get("username")
#         password=request.form.get("password")
#         if username=="admin" and password=="admin":
#             session["userinfo"]=username
#             return redirect("/index")
#         else:
#             return render_template('login.html',msg='用户名或密码错误')
#
# @app.route("/index",methods=["GET"])
# @auth
# def index():
#     return "欢迎登陆"
#
# @app.route("/home",methods=["GET"])
# @auth
# def home():
#     return "welcome to home"
#
#
# if __name__ == '__main__':
#     app.run()
#

