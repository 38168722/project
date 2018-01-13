#!/usr/bin/env python
# -*- coding: utf-8 -*-

#1.通过ChangeList封装好多数据
crm 在前端页面展示时从后台要传到前台的数据太多所以直接新建一个changelist类封装起来，这样只需传一个changelist实例化对象即可。

#2.销售中公共资源：Q查询，3天15天
使用Q做或查询，以满足多个条件的任一匹配。

#3.使用yield实现- 生成器函数，对数据进行加工处理- __iter__和yield配合
为避免数据多次循环，所以在后台使用yield的数据返回方式，这样只有在web前端数据展示时才会循环。

#4.获取Model类中的字段对应的对象
主要根据相关对象拿到相应字段，具体方法如下
- models.UserInfo._meta.get_field('name')  # 根据字段名称，获取字段对象
- models.UserInfo._meta.fields  # 获取类中所有的字段
- models.UserInfo._meta._get_fields()  # 获取类中所有的字段（包含反向关联的字段）
- models.UserInfo._meta.many_to_many  # 获取m2m字段

#5.模糊搜索功能
在匹配查询多个数据库字段的时候使用

#6.Type创建类
在问题调查表中有使用，使用type创建不同modelform类

#7.自动派单
- 原来在内存中实现，问题：重启和多进程时，都有问题。
- redis
- 状态
- 原来数据（权重表权重和个数）
- pop数据

#8.使用list_diplay配置
list_display = [函数名, ]

#9.reverse反向生成URL
crm中在生成编辑、删除按钮时使用reverse反向生成url链接

#10.母版
前端web页面中使用，主要是为了减少多页面重复冗余的代码。

#11.ready方法定制起始文件- 文件导入实现单例模式
自定义stark 组件时使用，主要是为了让服务启动后能将相应的model类自动注册到register方法中

#12.inclusion_tag
重复的数据需要在多个页面展示时就可以定义一个自定义标签在其它web页面中多次调用

#13.中间件的使用
系统默认的中间件有，通常我们自己也会根据项目情况自定义中间件如权限中间件。
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',


#15.importlib + getattr
主要用于通过配置文件反向解析包的情况。

#16.FilterOption，lambda表达式
主要用于数据的封装

# 17.QueryDict- 原条件的保留- filter
用于在查询数据时还需返回到查询前的状态。比如编辑数据完成时返回到之前的页面。

# 18.ModelForm
数据的增、删、改都用到了modelform

# 19.面向对象的 @ property @ classmethod
需要将一个方法变成一个属性一样调用时使用@property 例如strak组件中的

# 20.mark_safe
在后台生成的html代码需用mark_safe包装起来才能正常在web前端展示。

# 21.抽象方法抽象类 +raise Im...
主要用于约束子类的实现方法。

# 22.组件中的装饰器，实现self.request = request
用于在不改变已写好函数构造的前提下增加相应功能。

# 23.自执行函数
主要用于web前端当页面加载完成后就执行的js函数

# 24.URL的钩子函数
方便url扩展

# 25.多继承
一个类多继承后就能使用多个父类中的功能。

# 26.批量导入，xlrd
crm做报表批量导入蚨使用.

# 27.redis连接池
crm中在使用redis存取数据时使用，使用的主要原因是连接池则可以实现在客户端建立多个链接并且不释放，当需要使用连接的时候通过一定的算法获取已经建立的连接，使用完了以后则还给连接池，这就免去了数据库连接所占用的时间。


# 28.工厂模式
settings.py
MSG_PATH = "path.Email"


class XXFactory(object):
    @classmethod
    def get_obj(cls):
        settings.MSG_PATH
        # rsplit
        # importlib
        # getattr
        return obj


class Email(object):
    def send ...


class WeChat(object):
    def send ...


class Msg(object):
    def send ...


# 29.Models类中自定义save方法
modelfrom中数据的保存也可以通过model类对像执行save方法实现

# 30.django admin中注册models时候
from django.contrib import admin
from old import models


# 方式一
class UserConfig(admin.ModelAdmin):
    pass
admin.site.register(models.UserInfo, UserConfig)


# 方式二
@admin.register(models.UserInfo)
class UserConfig(admin.ModelAdmin):
    pass

# 31.深浅拷贝
crm项目中的组合搜索中有用到该功能。