#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models_sep import db
class Article(db.Model):
    __tablename='article'
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)