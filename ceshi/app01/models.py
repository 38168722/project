from django.db import models
from app01 import views
class Comment(models.Model):
    content=models.CharField(verbose_name="评论内容",null=True,blank=True,max_length=132)
    pid=models.ForeignKey(to="Comment",blank=True,null=True)

