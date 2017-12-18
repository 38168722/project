from django.db import models

# Create your models here.
from django.forms import ModelForm


class UserInfo(models.Model):
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    email=models.EmailField(verbose_name="邮件",null=True,blank=True)
    tel=models.IntegerField(verbose_name="手机号",null=True,blank=True)
    role=models.ForeignKey(verbose_name="角色",null=True,blank=True,to="Role")

class Role(models.Model):

    name=models.CharField(verbose_name="角色名称",max_length=32)

    def __str__(self):
        return self.name
