from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    wordNum=models.IntegerField(default=0)
    readNum=models.IntegerField(default=0)
    publish=models.ForeignKey("Publish")
    authorlist=models.ManyToManyField("Author")

    def __str__(self):
        return self.title

class Publish(models.Model):
    name=models.CharField(max_length=32)
    addr=models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    tel=models.CharField(max_length=32)
    addr=models.CharField(max_length=90)

    def __str__(self):
        return self.name

class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    email=models.CharField(max_length=32,default="")
    tel=models.CharField(max_length=32,default="")
