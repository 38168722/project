#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint,render_template,url_for

bp = Blueprint('user',__name__,url_prefix='/user',static_folder="pic",template_folder="hello",subdomain="www")

@bp.route('/profile/')
def profile():
    print(url_for('user.index'))
    return render_template("hello.html")

@bp.route('/')
def index():
    return "User's Index Page"



