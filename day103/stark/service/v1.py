#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import QueryDict
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from utils.page import Pagenation

class ChangeList(object):

    def __init__(self,config):
        self.config=config
        self.list_display=config.get_list_display()
        self.model_class=config.model_class

    def head_list(self):
        """
        构造表头
        :return:
        """
        result=[]
        for field_name in self.list_display:
            if isinstance(field_name,str):
                verbose_name=self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name=field_name(self.config,is_header=True)
            result.append(verbose_name)
        return result

class StarkConfig(object):

    list_display = []

    #是否显示添加按钮，默认为True
    show_add_btn=True

    def get_show_add_btn(self):
        return self.show_add_btn

    # model_form_class
    model_form_class = None

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        from django.forms import ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"
        # return TestModelForm
        #通过type类来创建ModelForm实例
        meta = type("Meta",(object,),{'model':self.model_class,'fields':'__all__'})
        TestModelForm = type('TestModelForm',(ModelForm,),{"Meta":meta})
        return TestModelForm

    # 定制列表页面显示的列
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择框"
        return mark_safe('<input type="checkbox" name="pk" value="%s">'%(obj.id))

    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑"
        params = QueryDict(mutable=True)
        params[self._query_param_key] = self.request.GET.urlencode()
        list_condition=params.urlencode()
        if list_condition:
            return mark_safe('<a href="%s?%s">编辑</a>' % (self.get_change_url(obj.id),list_condition))
        return mark_safe('<a href="%s">编辑</a>'%(self.get_change_url(obj.id),))

    def delete(self,obj=None,is_header=False):
        if is_header:
            return "删除"
        query_str = self.request.GET.urlencode()
        if query_str:
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe('<a href="%s?%s">删除</a>' % (self.get_delete_url(obj.id),params.urlencode()))
        return mark_safe('<a href="%s">删除</a>'%self.get_delete_url(obj.id))

    def get_list_display(self):
        data=[]
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

        #下面是错误的加载方式
        # self.list_display.append(StarkConfig.edit)
        # self.list_display.append(StarkConfig.delete)
        # self.list_display.insert(0,StarkConfig.checkbox)
        # return self.list_display

    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site = site
        self.request = None
        self._query_param_key="_list_filter"

     ######## URL 相关 ##############

    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            self.request=request
            return view_func(request,*args,**kwargs)
        return inner

    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns=[
            url(r'^$',self.wrap(self.changelist_view),name="%s_%s_changelist"%app_model_name),
            url(r'^add/$', self.wrap(self.add_view),name="%s_%s_add"%app_model_name),
            url(r'^(\d+)/delete/$',self.wrap(self.delete_view),name="%s_%s_delete"%app_model_name),
            url(r'^(\d+)/change/$',self.wrap(self.change_view),name="%s_%s_change"%app_model_name),
        ]
        url_patterns.extend(self.extra_url())
        return url_patterns

    def extra_url(self):
        return []

    def get_change_url(self,nid):
        name="stark:%s_%s_change"%(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        edit_url=reverse(name,args=(nid,))
        return edit_url

    def get_list_url(self):
        name="stark:%s_%s_changelist"%(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        edit_url=reverse(name)
        return edit_url

    def get_add_url(self):
        name="stark:%s_%s_add"%(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        edit_url=reverse(name)
        return edit_url

    def get_delete_url(self,nid):
        name="stark:%s_%s_delete"%(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        edit_url=reverse(name,args=(nid,))
        return edit_url

    @property
    def urls(self):
        return self.get_urls()

    def changelist_view(self,request,*args,**kwargs):
        c1 = ChangeList(self)
        #生成表头数据
        def head_list():
            for field_name in self.get_list_display():
                if isinstance(field_name, str):
                    yield self.model_class._meta.get_field(field_name).verbose_name
                else:
                    yield field_name(self,is_header=True)

        #分页处理开始
        current_page = int(request.GET.get('page', 1))
        total_item_count = self.model_class.objects.all().count()
        page_obj=Pagenation(current_page,total_item_count,self.get_list_url(),request.GET)
        data_list = self.model_class.objects.all()[page_obj.start:page_obj.end]
        #分页处理结束

        #将传过来的参数保存起来
        params = QueryDict(mutable=True)
        params['_list_filter'] = request.GET.urlencode()
        list_condition = params.urlencode()


        #生成表中body的数据
        def datalist():
            for row in data_list:
                def inner(obj):
                    for field_name in self.get_list_display():
                        if isinstance(field_name,str):
                            val=getattr(obj,field_name)
                        else:
                            val=field_name(self,obj)
                        yield val
                yield inner(row)
        return render(request,"stark/changelist.html",
                      {"page_html":page_obj.page_html(),
                       "datalist":datalist(),"head_list"
                       :head_list,"add_url"
                       :self.get_add_url(),
                       "list_condition":list_condition,
                       "show_add_btn":self.get_show_add_btn()})

    def add_view(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        if request.method=="GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{"form":form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, 'stark/add_view.html', {"form": form})

    def delete_view(self,request,nid,*args,**kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        list_query_str = request.GET.get(self._query_param_key)
        list_url = "%s?%s" % (self.get_list_url(), list_query_str)
        return redirect(list_url)

    def change_view(self,request,nid,*args,**kwargs):

        obj=self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        # GET 显示标签+默认值
        model_form_class = self.get_model_form_class()
        if request.method=="GET":
            form = model_form_class(instance=obj)
            return render(request,'stark/change_view.html',{'form':form})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                list_query_str=request.GET.get(self._query_param_key)
                list_url="%s?%s"%(self.get_list_url(),list_query_str)
                return redirect(list_url)
            return render(request, 'stark/change_view.html', {'form': form})

class StarkSite(object):

    def __init__(self):
        self._registry={}

    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class=StarkConfig
        self._registry[model_class]=stark_config_class(model_class,self)

    def get_urls(self):
        url_pattern=[]
        #为每一个类，创建四个URL
        for model_class,stark_config_obj in self._registry.items():
            app_name=model_class._meta.app_label
            model_name=model_class._meta.model_name
            curd_url=url(r'%s/%s/'%(app_name,model_name,),(stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)

        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(),None,'stark')

site=StarkSite()