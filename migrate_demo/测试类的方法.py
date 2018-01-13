#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Foo:
    def __init__(self):
        pass

    def __new__(self, *args, **kwargs):
        print('__new__')

    def __call__(self, *args, **kwargs):
        print('__call__')

obj = Foo()
obj()