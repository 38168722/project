#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Foo(object):

    _instance=None

    def __init__(self,name):
        self.name=name

    @classmethod
    def instance(self,*args,**kwargs):
        if not Foo._instance:
            obj = Foo(*args,**kwargs)
            Foo._instance=obj
        return Foo._instance


a1 = Foo.instance('alex')
a2 = Foo.instance('egon')

