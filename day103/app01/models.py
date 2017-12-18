from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名称")
    email = models.EmailField(verbose_name="邮箱",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)
    role = models.ForeignKey(verbose_name="角色",to="Role",null=True,blank=True,default=1)

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

class Host(models.Model):
    hostname=models.CharField(verbose_name="主机名",max_length=32)
    ip = models.GenericIPAddressField(verbose_name="IP地址",protocol="both")
    port = models.IntegerField(verbose_name="端口")
