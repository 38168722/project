#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe


class StarkConfig(object):

    def __init__(self,meta_class,site):
        self.meta_class=meta_class
        self.site=site

    def get_urls(self):
        meta_class_model=self.meta_class._meta.app_label,self.meta_class._meta.model_name
        urlpattern=[
            url('^$',self.change_list_view,name="%s_%s_changelist"%meta_class_model),
            url('^add/$',self.add_view,name="%s_%s_add"%meta_class_model),
            url('^(\d+)/change/$',self.change_view,name="%s_%s_change"%meta_class_model),
            url('^(\d+)/delete/$',self.delete_view,name="%s_%s_delete"%meta_class_model)
        ]
        return urlpattern

    list_display=[]

    @property
    def urls(self):
        return self.get_urls()

    def change_list_view(self,request):
        #拿到主体部分数据
        data_list=self.meta_class.objects.all()
        data_all=[]
        for row in data_list:
            temp=[]
            for field_name in self.get_list_display():
                if isinstance(field_name,str):
                    val=getattr(row,field_name)
                else:
                    val=field_name(self,row)
                temp.append(val)
            data_all.append(temp)
        return render(request,"list.html",{"data":data_all,"head":self.get_head_list()})

    def add_view(self,request):
        return HttpResponse("添加")

    def change_view(self,request,nid):




        return HttpResponse("编辑")

    def delete_view(self,request,nid):
        return HttpResponse("删除")

    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑"
        return mark_safe('<a href="%s">编辑</a>'%(self.get_change_url(obj.id)))

    def get_change_url(self,nid):
        name="stark:%s_%s_change"%(self.meta_class._meta.app_label,self.meta_class._meta.model_name,)
        print("name===",name)
        edit_url=reverse(name,args=(nid,))
        return edit_url

    def get_list_display(self):
        data=[]
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
        return data

    def get_head_list(self):
        temp=[]
        for field_name in self.get_list_display():
            if isinstance(field_name,str):
                val=self.meta_class._meta.get_field(field_name).verbose_name
            else:
                val=field_name(self,is_header=True)
            temp.append(val)
        return temp

class StarkSite(object):

    def __init__(self):
        self._register={}

    def register(self,meta_class,stark_config_obj=None):

        if not stark_config_obj:
            stark_config_obj=StarkConfig
        self._register[meta_class]=stark_config_obj(meta_class,self)

    def get_urls(self):
        url_pattern=[]
        for meta_class,stark_config_obj in self._register.items():
            model_name=meta_class._meta.app_label,meta_class._meta.model_name
            curd_url=url(r'%s/%s/'%(model_name),(stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)
        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(),None,'stark')

site=StarkSite()
