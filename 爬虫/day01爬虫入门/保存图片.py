#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

response = requests.get("https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2556139272,1053388184&fm=27&gp=0.jpg")

with open("tupian.jpg","wb") as f:
    f.write(response.content)