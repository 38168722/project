from django.test import TestCase

# Create your tests here.

class StarkConfig(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age

    @property
    def printInfo(self):
        return "用户名=%s 年龄=%s"%(self.name,self.age)


v1=StarkConfig
print(v1.printInfo)