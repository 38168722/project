#!/usr/bin/env python
# -*- coding: utf-8 -*-
def extra_url(self):
    app_model_name=(self.model_class._meta.app_label,self.model_class._meta.model_name,)
    patterns=[
        url(r'(\d+)/(\d+)/dc/$',self.wrap(self.delete_course),name="%s")

    ]