from django.test import TestCase

# Create your tests here.
import copy
abc=[1,2,3]
b=copy.deepcopy(abc)
abc.pop(1)
print(abc)
print(b)