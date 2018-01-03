from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    department=models.ForeignKey(to="Department",verbose_name="部门",blank=True,null=True)
    role=models.ManyToManyField(to="Role",verbose_name="角色",blank=True,null=True)

    class Meta:
        verbose_name="用户表"

    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=32,verbose_name="部门名称")

    class Meta:
        verbose_name="部门表"

    def __str__(self):
        return self.name

class Role(models.Model):
    name=models.CharField(max_length=32,verbose_name="角色")

    class Meta:
        verbose_name="角色"

    def __str__(self):
        return self.name