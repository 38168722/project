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
        if is_header:
            return "部门"
        return obj.depart.caption

    def display_roles(self,obj=None,is_header=False):
        if is_header:
            return "扮演角色"
        return obj.roles.title

    list_display = ['id','name','email',display_gender,display_depart,display_roles]
    comb_filter=["gender","depart","roles"]

class RoleConfig(v1.StarkConfig):
    list_display = ["title"]

class DepartmentConfig(v1.StarkConfig):
    list_display = ["caption"]


v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)
v1.site.register(models.Department,DepartmentConfig)