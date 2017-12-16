#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
def init_permission(user,request):
    """
    初始化权限信息，获取权限信息并放置到session中。
    :param user:
    :param request:
    :return:
    """
    permission_list = user.roles.values('permissions__title',              # 用户列表
                                        'permissions__url',
                                        'permissions__code',
                                        'permissions__is_menu',            # 是否是菜单
                                        'permissions__groups_id',
                                        'permissions__groups__menu_id',     # 菜单ID
                                        'permissions__groups__menu__title',#  菜单名称
                                        ).distinct()
    menu_list=[]

    #去掉不是菜单的URL
    for item in permission_list:
        if not item['permissions__is_menu']:
            continue
        tp1={
            'menu_id':item['permissions__groups__menu_id'],
            'menu_title':item['permissions__groups__menu__title'],
            'title':item['permissions__title'],
            'url':item['permissions__url'],
            'active':False,
        }
        menu_list.append(tp1)
    request.session[settings.PERMISSION_MENU_KEY]=menu_list

    #权限相关
    result={}
    for item in permission_list:
        group_id=item['permissions__groups_id']
        code=item['permissions__code']
        url=item['permissions__url']
        if group_id in result:
            result[group_id]['codes'].append(code)
            result[group_id]['urls'].append(url)
        else:
            result[group_id]={
                'codes':[code,],
                'urls':[url,]
            }
    request.session[settings.PERMISSION_URL_DICT_KEY]=result