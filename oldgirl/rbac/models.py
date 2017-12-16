from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)
    role = models.ManyToManyField(verbose_name="所属角色",to="Role",blank=True)

    class Meta:
        verbose_name_plural="用户表"

    def __str__(self):
        return self.username

class Role(models.Model):

    title=models.CharField(verbose_name="角色名称",max_length=32)
    permission=models.ManyToManyField(verbose_name="所属权限",to="Permission",blank=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="角色表"


class Permission(models.Model):

    title=models.CharField(verbose_name="权限名称",max_length=32)
    url=models.CharField(verbose_name="访问地址",max_length=182)
    code=models.CharField(verbose_name="权限编码",max_length=182)
    menu_gp=models.ForeignKey(verbose_name="组内菜单",to="Permission",null=True,blank=True)
    group=models.ForeignKey(verbose_name="所属权限组",to="Group",null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="权限表"


class Group(models.Model):

    title=models.CharField(verbose_name="组名称",max_length=32)
    menu=models.ForeignKey(verbose_name="所属菜单",to="Menu",max_length=32,null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="权限组表"

class Menu(models.Model):
    title=models.CharField(verbose_name="菜单名称",max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="菜单表"