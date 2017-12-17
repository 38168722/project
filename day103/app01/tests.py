from django.test import TestCase

# Create your tests here.
from types import FunctionType, MethodType
def hello():
    print("helo world")

print(isinstance(hello,MethodType))

class Human(object):
    def func(self):
        print("this is function")

obj=Human()
print(isinstance(obj.func,MethodType))
print(isinstance(Human.func,MethodType))

