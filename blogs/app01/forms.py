#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import Form
from app01.views import models
from django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError

class UserForm(Form):

    def __init__(self,request,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.request=request

    username=fields.CharField(
        label="Your name",
        max_length=100,
        required=True,
        error_messages={"required":"用户名不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control input-lg","id":"username"})
    )
    password=fields.CharField(
        label="Your password",
        max_length=100,
        required=True,
        error_messages={"required": "密码不能为空"},
        widget=widgets.PasswordInput(attrs={"class": "form-control input-lg", "id": "password"})
    )

    validCode=fields.CharField(
        label="Your valiCode",
        max_length=100,
        required=True,
        error_messages={"required": "验证码不能为空"},
    )

    def clean_validCode(self):
        v = self.cleaned_data['validCode']
        if v.upper() != self.request.session["keepValidCode"].upper():
            raise ValidationError("验证码有误")
        return v

    def clean_username(self):
        v=self.cleaned_data['username']
        if not models.User.objects.filter(username=v):
            raise ValidationError("用户名不存在")
        return v

    def clean(self):
        value_dict=self.cleaned_data
        v1 = value_dict.get('username')
        v2 = value_dict.get('password')
        if not v2:
            raise ValidationError("密码不能为空")
        elif not models.User.objects.filter(username=v1,password=v2):
            raise ValidationError("密码错误")
        return self.cleaned_data


class UserRegisterForm(Form):

    username=fields.CharField(
        label="Your name",
        max_length=100,
        required=True,
        error_messages={"required":"用户名不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","id":"username"})
    )
    password=fields.CharField(
        label="Your password",
        max_length=100,
        required=True,
        error_messages={"required": "密码不能为空"},
        widget=widgets.PasswordInput(attrs={"class": "form-control", "id": "password"})
    )
    repassword=fields.CharField(
        label="Your password",
        max_length=100,
        required=True,
        error_messages={"required": "密码不能为空"},
        widget=widgets.PasswordInput(attrs={"class": "form-control", "id": "repassword"})
    )

    nickname=fields.CharField(
        label="Your nickname",
        max_length=100,
        required=True,
        error_messages={"required":"别名不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","id":"nickname"})
    )

    telephone=fields.CharField(
        label="Your telephone",
        max_length=100,
        required=True,
        error_messages={"required":"电话号码不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","id":"telephone"}),
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字')],
    )

    avatar=fields.FileField(
        required=False,
        label="Your avatar",
        max_length=100,
    )

    def clean_username(self):
        v=self.cleaned_data['username']
        if models.User.objects.filter(username=v).count():
            raise ValidationError("用户名已存在")
        return v

    def clean_repassword(self):
        password= self.cleaned_data.get('password')
        repassword= self.cleaned_data.get('repassword')
        if repassword==password:
            return repassword
        raise ValidationError('两次密码不一致')

    def clean_telephone(self):
        v=self.cleaned_data.get('telephone')
        if models.User.objects.filter(telephone=v).count():
            raise ValidationError('电话号码已存在')
        return v

