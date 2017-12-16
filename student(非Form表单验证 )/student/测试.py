#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
s = time.time()
myList = []
for a in range(1000):
    for b in range(1000):
        for c in range(1000):
            if a + b + c == 1000 and a**2 + b**2 == c**2:
                myList.append((a,b,c))
print(myList)
print(time.time()-s)
