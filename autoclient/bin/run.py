#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os,importlib
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from conf import settings
for k,v in settings.PLUGIN_ITEMS.items():
    module_path,cls_name=v.rsplit(".",maxsplit=1)
    m=importlib.import_module(module_path)
    cls=getattr(m,cls_name)
    obj=cls()
    ret=obj.process()
    print(ret)