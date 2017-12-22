#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
# start_time=time.time()
# for i in range(0,1001):
#     for j in range(0,1001):
#             z=1000-i-j
#             if i+j+z ==1000 and i**2+j**2==z**2:
#                 print("i==%s,j==%s,z==%s"%(i,j,z))
# end_time=time.time()
# print("times:%s"%(end_time-start_time))

def func4(x):
    if x>0:
        func4(x-1)
        print(x)

func4(10)