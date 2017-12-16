#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django.template import Library
from django.conf import settings
register = Library()

@register.inclusion_tag("xxxx.html")
def menu_html(request):
    menu_list=request.session[settings.PERMISSION_MENU_KEY]
    current_url=request.path_info
    result={}
    for item in menu_list:
        url=item['url']
        regex="^{0}$".format(url)
        active=False
        if re.match(regex,current_url):
            active=True
        menu_id=item['menu_id']
        if menu_id in result:
            result[menu_id]['children'].append({"title":item['title'],'url':item['url'],'active':active})
            if active:
                result[menu_id]['active']=True
        else:
            result[menu_id]={
                'menu_id':menu_id,
                'menu_title':item['menu_title'],
                'active':active,
                'children':[
                    {'title':item['title'],'url':item['url'],'active':active},
                ]
            }
    return {'menu_dict':result}