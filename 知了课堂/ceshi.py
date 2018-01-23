#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Human(object):
    def __init__(self,name):
        self.name=name
    sleep="睡觉"
    action="跑"
    def jump(self):
        return self.name


class People(Human):
    pass


p=People("egon")
print(p.sleep)
print(p.jump())