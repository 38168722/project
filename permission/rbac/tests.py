from django.test import TestCase

# Create your tests here.

dict = {
   1: {"codes":{"Google": 'www.google.com', 'Runoob': 'www.runoob.com', 'taobao': 'www.taobao.com'}},
    2:{"abc":{"baidu": 'www.baidu.com', 'blog': 'www.blog.com', 'oldboy': 'www.oldboy.com'}},

}

for key,values in dict.items():
    print(values)