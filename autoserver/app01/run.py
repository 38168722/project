#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import requests
result = subprocess.getoutput("ipconfig")
message=result[40:50]
print("message==",message)
api="http://127.0.0.1:8080/api/server.html"
requests.post(url=api,data={"k1":message})

