#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app01 import models
from django.forms import ModelForm


class UserInfoModelForm(ModelForm):
    class Meta:
        model=models.UserInfo
        fields="__all__"

