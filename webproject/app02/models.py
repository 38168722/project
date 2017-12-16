from django.db import models
# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=32,verbose_name="文章标题")
    describe=models.CharField(max_length=700,verbose_name="文章描述")
    publishDate=models.DateField(verbose_name="发布日期")
    readnum=models.IntegerField(verbose_name="阅读数")
    recommend=models.IntegerField(verbose_name="推荐数")
    commentnum=models.IntegerField(verbose_name="评论数")
    ArticleDetail=models.OneToOneField(verbose_name="文章详细信息",to="ArticleDetail",null=True,blank=True)
    user=models.ManyToManyField(to="User",null=True,blank=True,verbose_name="作者")
    classfication=models.ForeignKey(to="Classfication",null=True,blank=True,verbose_name="分类")
    tag=models.ManyToManyField(to="Tag",null=True,blank=True,verbose_name="标签")
    poll=models.OneToOneField(verbose_name="文章点赞",to="Poll",null=True,blank=True)

    class Meta:
        verbose_name_plural="文章表"


class Blog(models.Model):
    url=models.CharField(max_length=80,verbose_name="个人博客地址")
    title=models.CharField(max_length=80,verbose_name="博客标题")
    fansnum=models.IntegerField(verbose_name="粉丝数")
    blogage=models.IntegerField(verbose_name="园龄")
    watchs=models.IntegerField(verbose_name="关注数")

    class Meta:
        verbose_name_plural="博客表"


class User(models.Model):
    username=models.CharField(max_length=32,unique=True,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    nickname=models.CharField(max_length=32,verbose_name="别名")
    avatar=models.CharField(verbose_name="头像",max_length=132)
    comment=models.ManyToManyField(to="Comment",verbose_name="用户评论",null=True,blank=True)
    poll=models.ForeignKey(verbose_name="用户点赞",to="Poll",null=True,blank=True)
    blog=models.OneToOneField(verbose_name="博客地址",to="Blog",null=True,blank=True)

    class Meta:
        verbose_name_plural="用户表"


class ArticleDetail(models.Model):
    content=models.CharField(max_length=88888,verbose_name="文章主体内容")

    class Meta:
        verbose_name_plural="文章详细表"


class Tag(models.Model):
    title = models.CharField(max_length=132,verbose_name="标签名称")

    class Meta:
        verbose_name_plural="标签表"


class Classfication(models.Model):
    title = models.CharField(max_length=132,verbose_name="分类名称")

    class Meta:
        verbose_name_plural="分类表"


class Comment(models.Model):
    content = models.CharField(verbose_name="评论内容",max_length=300)
    date = models.DateField(verbose_name="评论日期")
    pid = models.IntegerField(verbose_name="主帖ID")
    article=models.ForeignKey(to="Article",verbose_name="文章评论",null=True,blank=True)

    class Meta:
        verbose_name_plural="评论表"

class Poll(models.Model):
    pollnum=models.IntegerField(verbose_name="点赞数")

    class Meta:
        verbose_name_plural="点赞表"



