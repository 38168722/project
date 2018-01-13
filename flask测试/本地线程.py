#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
local_values=threading.local()

class A(object):
    localnum=None

a=A()

def func(num):
    a.localnum=num

    # local_values.name=num
    time.sleep(2)
    print(a.localnum,threading.current_thread().name)

for i in range(5):
    th = threading.Thread(target=func,args=(i,),name="线程%s"%i)
    th.start()

