#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm

from stark.services import v1
from app01 import models
class UserInfoModel(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

class UserInfoConfig(v1.StarkConfig):
    list_display=['username','password','email','tel','role']



v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role)