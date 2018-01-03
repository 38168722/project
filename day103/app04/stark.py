#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stark.service import v1
from app04 import models
class UserInfoConfig(v1.StarkConfig):
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()

    def display_depart(self,obj=None,is_header=False):
        """
         获取用户部门
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "部门"
        return obj.depart.caption

    def display_roles(self,obj=None,is_header=False):
        """
         由于是用户与角色是多对多的关系，所以只能for循环取出所有用户角色后再以html的方式显示出。
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "扮演角色"
        html=[]
        role_list = obj.roles.all()
        for role in role_list:
            html.append(role.title)
        return ",".join(html)

    #列出需要显示的字段
    list_display = ['id','name','email',display_gender,display_depart,display_roles]
    
    #在前端页面上列出需要显示的标签搜索字段
    comb_filter =[
        v1.FilterOption("gender",is_choice=True),
        v1.FilterOption("depart"),
        v1.FilterOption("roles",True),
    ]

class RoleConfig(v1.StarkConfig):
    list_display = ["title"]

class DepartmentConfig(v1.StarkConfig):
    list_display = ["caption"]


v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)
v1.site.register(models.Department,DepartmentConfig)