#!/usr/bin/env python
# -*- coding: utf-8 -*-


i=0
def func(i):
    s=""
    i+=1
    s+='%i'%i
    if i!=10:
        s += func(i)
    print('s',i,'++++++++++++++++++++',s)

    return s

l=func(i)
print(l,i)



