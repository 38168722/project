from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名称")
    class Meta:
        verbose_name_plural="用户信息表"
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=32,verbose_name="角色名称")
    class Meta:
        verbose_name_plural="角色表"

    def __str__(self):
        return self.name

