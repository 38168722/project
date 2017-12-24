from django.test import TestCase

# Create your tests here.

class Foo(object):
    def shit(self):
        print("hello world")

class Bar(Foo):
    def abc(self):
        print("wen shao")

f1=Bar()
print(type(f1))