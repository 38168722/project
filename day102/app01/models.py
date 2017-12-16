from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    email = models.EmailField(verbose_name="邮件")
    role = models.ForeignKey(to="Role",verbose_name="所属角色")
    class Meta:
        verbose_name_plural="用户信息"

class Role(models.Model):
    name = models.CharField(max_length=32,verbose_name="角色名称")


