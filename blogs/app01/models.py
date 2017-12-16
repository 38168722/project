from django.db import models
# Create your models here.
# from django.contrib.auth.models import AbstractUser

class User(models.Model):
    """
    用户表
    """
    username=models.CharField(verbose_name="用户名",max_length=32)
    password=models.CharField(verbose_name="密码",max_length=32)
    nickname=models.CharField(verbose_name="别名",max_length=32)
    telephone=models.CharField(verbose_name="手机号码",max_length=11,blank=True,null=True,unique=True)
    avatar=models.FileField(verbose_name="头像",upload_to="avatar",default="/avatar/default.png")
    # create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    create_time=models.DateTimeField(verbose_name="创建时间")
    fans=models.ManyToManyField(
        verbose_name="粉丝们",
        to="User",
        through="UserFans",
        related_name="f",
        through_fields=("myself","follower"),null=True,blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="用户表"

class Blog(models.Model):
    """
    站点信息
    """
    title=models.CharField(verbose_name="个人博客标题",max_length=64)
    site=models.CharField(verbose_name="个人博客后缀",max_length=32)
    theme=models.CharField(verbose_name="博客主题",max_length=32)
    user=models.OneToOneField(to="User",verbose_name="对应用户",null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="站点表"

class Category(models.Model):
    """
    博主个人文章分类表
    """
    title=models.CharField(verbose_name="分类标题",max_length=32)
    blog=models.ForeignKey(verbose_name="所属博客",to="Blog")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="分类表"
        ordering=["title"]

class Article(models.Model):
    """
    文章表
    """
    title=models.CharField(max_length=50,verbose_name="文章标题")
    desc=models.CharField(max_length=255,verbose_name="文章描述")
    read_count=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    up_count=models.IntegerField(default=0)
    down_count=models.IntegerField(default=0)
    create_time=models.DateTimeField(verbose_name="创建时间")
    category=models.ForeignKey(verbose_name="文章类型",to="Category",blank=True,null=True)
    user=models.ForeignKey(verbose_name="所属用户",to="User",null=True,blank=True)
    tags=models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=('article','tag'),
    )

    site_article_category=models.ForeignKey("SiteArticleCategory",null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="文章表"

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content=models.TextField(verbose_name="文章内容")
    article=models.OneToOneField(verbose_name="所属文章",to="Article",blank=True,null=True)

    class Meta:
        verbose_name_plural="文章详细表"

    def __str__(self):
        return self.article.title

class Comment(models.Model):
    """
    评论表
    """
    content=models.CharField(verbose_name="评论内容",max_length=255)
    create_time=models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    up_count=models.IntegerField(default=0)
    user=models.ForeignKey(verbose_name="评论者",to="User")
    article=models.ForeignKey(verbose_name="评论文章",to="Article")
    pid=models.ForeignKey(verbose_name="父级评论",to="self",blank=True,null=True)

    def __str__(self):
        return self.pid_id

    class Meta:
        verbose_name_plural="评论表"

class CommentUp(models.Model):
    """
     评论点赞
    """
    user = models.ForeignKey(verbose_name="所属用户", to="User", null=True, blank=True)
    comment = models.ForeignKey(verbose_name="所属评论", to="Comment", null=True, blank=True)

    class Meta:
        unique_together=[('user','comment')]
        verbose_name_plural="评论点赞表"

class ArticleUp(models.Model):
    """
     文章点赞表
    """
    user=models.ForeignKey(verbose_name="所属用户",to="User",null=True,blank=True)
    article=models.ForeignKey(verbose_name="所属文章",to="Article",null=True,blank=True)

    class Meta:
        unique_together=[('user','article')]
        verbose_name_plural="文章点赞表"

class Tag(models.Model):
    """
     标签表
    """
    title=models.CharField(verbose_name="标签名称",max_length=32)
    blog=models.ForeignKey(verbose_name="所属博客",to="Blog")

    class Meta:
        verbose_name_plural="标签表"

    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    """
    文章标签关系表
    """
    article=models.ForeignKey(verbose_name="文章",to="Article")
    tag=models.ForeignKey(verbose_name="标签",to="Tag")

    class Meta:
        unique_together=[
            ('article','tag')
        ]
        verbose_name_plural="文章标签关系表"

    def __str__(self):
        return self.article.title+"+"+self.tag.title

class UserFans(models.Model):
    """
    用户与粉丝关系表
    """
    myself=models.ForeignKey(verbose_name="博主",to="User", related_name="focus")
    follower=models.ForeignKey(verbose_name="粉丝",to="User", related_name="follows")

    class Meta:
        verbose_name_plural="粉丝表"
        unique_together=[
            ("myself","follower"),
        ]

class SiteCategory(models.Model):

    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="站点分类"


class SiteArticleCategory(models.Model):

    name=models.CharField(max_length=32)
    site_category=models.ForeignKey("SiteCategory")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="站点文章分类"