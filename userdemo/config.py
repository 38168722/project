#!/usr/bin/env python
# -*- coding: utf-8 -*-
DEBUG=True

#sqlalchemy 连接配置
DIALECT='mysql'
DRIVER='mysqldb'
USERNAME='root'
PASSWORD='123456'
HOST='127.0.0.1'
PORT='3306'
DATABASE='zhiliao'
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=False     #关闭警告信息


