from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=32)
    sex=models.CharField(max_length=32)
    course=models.ForeignKey("Course")
    classes=models.ForeignKey("Classes")

    def __str__(self):
        return self.name

class Course(models.Model):
    name=models.CharField(max_length=32)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    period=models.IntegerField()
    def __str__(self):
        return self.name

class Classes(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    sex=models.CharField(max_length=12,default="")
    tel=models.CharField(max_length=32,default="")
    salary=models.DecimalField(max_digits=7,decimal_places=2)
    class_list=models.ManyToManyField("Classes")
    course_list=models.ManyToManyField("Course")
    userType=models.ForeignKey("UserType")
    def __str__(self):
        return self.name


class UserType(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name

class User(models.Model):
    name=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
