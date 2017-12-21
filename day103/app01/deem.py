#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Parent(object):

    def hello(self):
        print("这个self是个什么鬼self%s"%self)


class Son(Parent):

    def printInfo(self):
        print("测试printInfo")

    def hello(self):
        print("会先执行自己吗")

a1 = Son()
a1.hello()