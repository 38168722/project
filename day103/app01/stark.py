#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stark.service import v1
from app01 import models
from django.conf.urls import url
from django.shortcuts import HttpResponse,redirect,render
from django.utils.safestring import mark_safe
from django.forms import ModelForm

class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        error_messages={
            'name':{
                'required':'用户名不能为空'
            }
        }

class UserInfoConfig(v1.StarkConfig):

    list_display = ["id", "name", "email", "role"]

    model_form_class = UserInfoModelForm

    def extra_url(self):
        url_list=[
            url(r'^fuck/$', self.func),
        ]
        return url_list

    def func(self,request):
        return HttpResponse("这是一个测试函数")

    show_add_btn = True

    def get_show_add_btn(self):
        #用来判断看session中是否有添加权限
        return self.show_add_btn

class RoleConfig(v1.StarkConfig):

    list_display = ["id","name"]

    show_add_btn = True

    def get_show_add_btn(self):
        #用来判断看session中是否有添加权限
        return self.show_add_btn

class HostModelForm(ModelForm):
    class Meta:
        model = models.Host
        fields=["id","hostname","ip","port"]
        error_messages={
            "hostname":{
                'required':"主机名不能为空"
            },
            'ip':{
                'required':'IP不能为空',
                'invalid':'IP格式错误',
            }
        }

class HostConfig(v1.StarkConfig):

    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return "自定义列"
        return "%s:%s"%(obj.ip,obj.port,)

    #让显示添加按钮
    show_add_btn = True
    #使用自定义model模块
    model_form_class = HostModelForm

    list_display = ["id", "hostname", "ip", "port", ip_port]

    #自定义扩充URL
    def extra_url(self):
        urls=[
            url('^report/$',self.report_view)
        ]
        return urls

    def report_view(self,request):
        return HttpResponse("自定义报表")

    def delete_view(self,request,nid,*args,**kwargs):
        if request.method=="GET":
            return render(request,"stark/my_delete.html")
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())

v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)
v1.site.register(models.Host,HostConfig)
