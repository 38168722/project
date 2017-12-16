#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stark.service import v1
from app01 import models
from django.shortcuts import HttpResponse,redirect,render
from django.utils.safestring import mark_safe
class UserInfoConfig(v1.StarkConfig):
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择框"
        return mark_safe('<input type="checkbox" name="pk" value="%s">'%(obj.id))

    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑按钮"
        return mark_safe('<a href="/edit/%s">编辑</a>'%obj.id)

    list_display = [checkbox,"id","name",edit]

class RoleConfig(v1.StarkConfig):
    list_display = ["id","name"]


v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role,RoleConfig)
