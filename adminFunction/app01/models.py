from django.db import models

# Create your models here.
class Employee(models.Model):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    did = models.ForeignKey("Department",blank=True,null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="员工表"

class Department(models.Model):

    dname = models.CharField(max_length=32)

    def __str__(self):
        return self.dname

    class Meta:
        verbose_name_plural="部门表"
