from django.test import TestCase

# Create your tests here.
dicts = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
for v in dicts.values():
    print("值是多少%s"%v)