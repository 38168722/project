#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from utils.page import Pagenation

class ChangeList(object):

    def __init__(self,config,queryset):
        self.config=config
        self.list_display=config.get_list_display()
        self.model_class=config.model_class

        #分页用
        current_page = config.request.GET.get('page', 1)
        total_item_count =queryset.count()
        self.page_obj=Pagenation(current_page,total_item_count,config.get_list_url(),config.request.GET)
        self.data_list = queryset[self.page_obj.start:self.page_obj.end]

        # 按钮是否显示
        self.show_add_btn = config.get_show_add_btn()

        # 是否显示搜索按钮
        self.show_search_form = config.get_show_search_form()
        self.search_form_val = config.request.GET.get(config.search_key,"")
        self.actions = config.get_actions()
        self.show_actions = config.get_show_actions()


    def modify_actions(self):
        result=[]
        for func in self.actions:
            temp={"name":func.__name__,'text':func.short_desc}
            result.append(temp)
        return result

    def add_url(self):
        return self.config.get_add_url()

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

    def body_list(self):
        """
        生成body表中的数据
        :return:
        """
        for row in self.data_list:
            def inner(obj):
                for field_name in self.list_display:
                    if isinstance(field_name,str):
                        val = getattr(obj,field_name)
                    else:
                        val = field_name(self.config,obj)
                    yield val
            yield inner(row)

class StarkConfig(object):

    list_display = []

    #是否显示添加按钮，默认为True
    show_add_btn=True

    def get_show_add_btn(self):
        return self.show_add_btn

    # model_form_class
    model_form_class = None

    search_fields=[]

    def get_search_fields(self):
        result=[]
        if self.search_fields:
            result.extend(self.search_fields)
        return result

    # 关键字搜索
    show_search_form = False

    def get_show_search_form(self):
        return self.show_search_form

    # actions定制
    show_actions = False
    def get_show_actions(self):
        return self.show_actions

    #6 组合搜索
    com_filter=[]
    def get_comb_filter(self):
        result=[]
        if self.com_filter:
            result.extend(self.com_filter)
        return result

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

    def edit(self,obj=None,is_header=None):
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

    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site = site
        self.request = None
        self._query_param_key="_list_filter"
        self.search_key="_q"

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

    def get_search_condition(self):
        key_word = self.request.GET.get(self.search_key)
        search_fields=self.get_search_fields()
        #使用Q方法的或条件查询
        condition=Q()
        condition.connector="or"
        if key_word and self.get_show_search_form():
            for field_name in search_fields:
                condition.children.append((field_name,key_word))
        return condition

    actions=[]
    def get_actions(self):
        result=[]
        if self.actions:
            result.extend(self.actions)
        return result


    @property
    def urls(self):
        return self.get_urls()

    def changelist_view(self,request,*args,**kwargs):
        """
        有action权限时则让批量删除或初始化，否则啥都不做
        :param request:
        :param args:
        :param kwargs:
        :return: 自定义有返回值时则返回，否则不返回
        """
        if request.method=="POST" and self.get_show_actions():
            func_name_str=request.POST.get("list_action")
            action_func = getattr(self,func_name_str)
            ret =action_func(request)
            if ret:
                return ret

        queryset=self.model_class.objects.filter(self.get_search_condition())
        cl = ChangeList(self,queryset)
        #将传过来的参数保存起来
        # params = QueryDict(mutable=True)
        # params[self._query_param_key] = request.GET.urlencode()
        # list_condition = params.urlencode()
        return render(request,"stark/changelist.html",{"cl":cl})
        # return render(request,"stark/changelist.html",
        #               {"page_html":c1.page_obj.page_html(),
        #                "datalist":c1.body_list(),"head_list"
        #                :c1.head_list(),"add_url"
        #                :self.get_add_url(),
        #                "list_condition":list_condition,
        #                "show_add_btn":self.get_show_add_btn()})

    def add_view(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        if request.method=="GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{"form":form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = "%s?%s" % (self.get_list_url(), list_query_str)
                return redirect(list_url)
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