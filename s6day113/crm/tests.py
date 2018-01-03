from django.test import TestCase

# Create your tests here.

num = 2
def func(n):
    print("=========1",n)
    if n>1:
        func(n-1)
    print("=======2",n)

func(num)