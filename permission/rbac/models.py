from django.db import models

class Menu(models.Model):
    """
        菜单组
    """
    title=models.CharField(max_length=32)

class Role(models.Model):
    '''
        Role table
    '''
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField(verbose_name='具有的所有权限',to='Permission',blank=True)
    class Meta:
        verbose_name_plural='角色表'

    def __str__(self):
        return self.title

class Permission(models.Model):
    '''
        permission table
    '''
    url=models.CharField(verbose_name='含正则的url',max_length=182)
    title=models.CharField(verbose_name='标题',max_length=182)
    code=models.CharField(verbose_name='代码',max_length=32,blank=True)
    is_menu=models.BooleanField(verbose_name="是否是菜单")
    groups=models.ForeignKey(to="Group",blank=True)

    class Meta:
        verbose_name_plural="权限表"

    def __str__(self):
        return self.title


class Group(models.Model):
    title=models.CharField(verbose_name='标题',max_length=182,blank=True)
    menu=models.ForeignKey(verbose_name="所属菜单",to='Menu',default=1)

class User(models.Model):
    '''
        User table
    '''
    username=models.CharField(verbose_name="用户名",max_length=182)
    password=models.CharField(verbose_name="密码",max_length=182)
    email=models.CharField(verbose_name="邮箱",max_length=32)
    roles=models.ManyToManyField(verbose_name="具有的所有角色",to='Role',blank=True)

    class Meta:
        verbose_name_plural='用户表'

    def __str__(self):
        return self.username





