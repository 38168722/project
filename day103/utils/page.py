#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

"""
使用方法：

from utils.page import Pagination
def users(request):
    current_page = int(request.GET.get('page',1))

    total_item_count = models.UserInfo.objects.all().count()
    # page_obj = Pagination(current_page,total_item_count,request.path_info)
    page_obj = Pagination(current_page,total_item_count,'/users.html')

    user_list = models.UserInfo.objects.all()[page_obj.start:page_obj.end]

    return render(request,'users.html',{'user_list':user_list,'page_html':page_obj.page_html()})

"""


class Pagenation(object):

    def __init__(self,current_page,total_item_count,base_url,per_page_count=10,show_pager_count=11):
        """
        :param current_page:  当前页
        :param total_item_count: 数据库数据总条数
        :param base_url:  分页前缀URL
        :param per_page_count: 每页显示数据条数
        :param show_pager_count: 最多显示的页码
        """
        self.current_page=current_page
        self.total_item_count=total_item_count
        self.base_url=base_url
        self.per_page_count=per_page_count
        self.show_pager_count=show_pager_count
        max_pager_num,b=divmod(total_item_count,per_page_count)
        if b:
            max_pager_num+=1
        self.max_pager_num=max_pager_num


    def start(self):
        return (self.current_page-1)*self.per_page_count

    def end(self):
        return self.current_page*self.per_page_count

    def page_html(self):
        page_list = []
        if self.current_page == 1:
            pre = '<li><a href="#">上一页</a><li>'
        else:
            pre = '<li><a href="%s?page=%s">上一页</a><li>' % (self.base_url, self.current_page - 1)
        page_list.append(pre)
        show_pager_count = 11
        half_show_pager_count = int(show_pager_count / 2)
        # 数据特别少的情况
        if self.max_pager_num < show_pager_count:
            # 页码小于11
            page_start = 1
            page_end = self.max_pager_num + 1
        else:
            if self.current_page <= half_show_pager_count:
                page_start = 1
                page_end = show_pager_count + 1
            else:
                if self.current_page + half_show_pager_count > self.max_pager_num:
                    page_start = self.max_pager_num - show_pager_count + 1
                    page_end = self.max_pager_num
                else:
                    page_start = self.current_page - half_show_pager_count
                    page_end = self.current_page + half_show_pager_count + 1

        for i in range(page_start, page_end):
            if i == self.current_page:
                tpl = '<li class="active"><a href="%s?page=%s">%s</a></li>' % (self.base_url, i, i)
            else:
                tpl = '<li><a href="%s?page=%s">%s</a></li>' % (self.base_url, i, i)
            page_list.append(tpl)
        if self.current_page == self.max_pager_num:
            next = '<li><a href="#">下一页</a><li>'
        else:
            next = '<li><a href="%s?page=%s">下一页</a><li>' % (self.base_url, self.current_page + 1)
        page_list.append(next)
        return mark_safe(''.join(page_list))


