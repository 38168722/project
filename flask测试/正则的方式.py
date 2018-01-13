#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,url_for

app = Flask(__name__)

#定义转换的类
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    """
    自定义URL匹配正则表达式
    """
    def __init__(self,map,regex):
        super(RegexConverter, self).__init__(map)
        self.regex=regex

    def to_python(self, value):
        """
        路由匹配时，匹配成功后传递给视图函数中参数的值
        :param value:
        :return:
        """
        return int(value)

    def to_url(self, value):
        val = super(RegexConverter, self).to_url(value)
        return val

#添加到converts中
app.url_map.converters['xxx'] = RegexConverter

#进行使用
@app.route('/index/<xxx("\d+"):nid>',endpoint='xx')
def index(nid):
    url_for('xx',nid=123)
    return "Index"

if __name__ == '__main__':
    app.run()