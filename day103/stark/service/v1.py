#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.db.models import Q
import copy,json
from django.http import QueryDict
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from utils.page import Pagenation

class FilterOption(object):
    """
     该类主要用来封装 com_filter搜索框的字段值
    """
    def __init__(self,field_name,multi=False,condition=None,is_choice=False,text_func_name=None,val_func_name=None):
        self.field_name=field_name
        self.multi=multi
        self.condition=condition
        self.is_choice=is_choice
        self.text_func_name=text_func_name
        self.val_func_name=val_func_name

    def get_queryset(self,_field):
        if self.condition:
            return _field.rel.to.objects.filter(self.condition)
        return _field.rel.to.objects.all()

    def get_choices(self,_field):
        return _field.choices

class FilterRow(object):
    """
      封装数据对象在此主要封装了用户表中角色、部门、性别数据
    """
    def __init__(self,option,data,request):
        self.data=data
        self.option=option
        self.request=request

    def __iter__(self):
        params = copy.deepcopy(self.request.GET)
        params._mutable = True
        print("option.field_name==%s"%self.option.field_name)
        current_id = params.get(self.option.field_name)
        current_id_list = params.getlist(self.option.field_name) #多选框值的获取
        """
        根据有无传[gender,depart,role]等关键字判断全部选项是否有选中。
        """
        if self.option.field_name in params:
            # del params[self.option.field_name]
            origin_list = params.pop(self.option.field_name)
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<li><a href=%s>全部</a><li>'%(url))
            params.setlist(self.option.field_name,origin_list)
        else:
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<li class="active"><a href=%s>全部</a><li>'%(url))
        """
         迭代的输出数据并判断相关字段是单选还是多选。
        :return:
        """
        for val in self.data:
            if self.option.is_choice:
                pk,text=str(val[0]),val[1]
            else:
                text = self.option.text_func_name(val) if self.option.text_func_name else str(val)
                pk = str(self.option.val_func_name(val)) if self.option.val_func_name else str(val.pk)

            #当前URL? option.field_name
            #参数= 当前URL?gender=pk,通过params 与 request.path_info 生成url
            if not self.option.multi:
                # 单选
                params[self.option.field_name]=pk
                url="{0}?{1}".format(self.request.path_info,params.urlencode())
                if current_id==pk:
                    yield mark_safe("<li class='active'><a href='{0}'>{1}</a><li>".format(url,text))
                else:
                    yield mark_safe("<li><a href='{0}'>{1}</a></li>".format(url,text))
            else:
                # 多选 current_id_list
                _params = copy.deepcopy(params)
                id_list = _params.getlist(self.option.field_name)
                if pk in current_id_list:
                    # 将已选择的多选移除
                    id_list.remove(pk)
                    _params.setlist(self.option.field_name,id_list)
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<li class='active'><a href='{0}'>{1}</a><li>".format(url,text))
                else:
                    from django.http import QueryDict
                    id_list.append(pk)
                    _params.setlist(self.option.field_name,id_list)
                    #创建URL
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<li><a href='{0}'>{1}</a><li>".format(url,text))

class ChangeList(object):

    def __init__(self,config,queryset):
        self.config=config
        self.list_display=config.get_list_display()
        self.model_class=config.model_class
        self.request = config.request
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
        self.show_comb_filter = config.get_show_comb_filter()
        self.comb_filter = config.get_comb_filter()
        self.edit_link = config.get_edit_link()

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
                    # 判断,是否field_name在edit_link里面
                    if field_name in self.edit_link:
                        # 反向生成URL
                        # 获取URL的参数
                        val = self.edit_link_tag(obj.pk,val)
                    yield val
            yield inner(row)

    def gen_comb_filter(self):
        """
         这是一个生成器函数
         通过类名get到userinfo下相应的对象，将所有数据放入data_list列表后在前端展示出来
        :return:
        """
        from django.db.models import ForeignKey,ManyToManyField
        for option in self.comb_filter:
            _field=self.model_class._meta.get_field(option.field_name)
            if isinstance(_field,ForeignKey):
                #获取当前字段depart关联的表并获取其所有数据
                row = FilterRow(option,option.get_queryset(_field),self.request)
            elif isinstance(_field,ManyToManyField):
                row = FilterRow(option,option.get_queryset(_field),self.request)
            else:
                row = FilterRow(option,option.get_choices(_field),self.request)
            yield row

    def edit_link_tag(self,pk,text):

        query_str= self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self.config._query_param_key] = query_str
        return mark_safe('<a href="%s?%s">%s</a>' % (self.config.get_change_url(pk), params.urlencode(),text,))

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

    #6 组合搜索默认为空，用户配置里写了就以用户配置为主
    comb_filter=[]
    def get_comb_filter(self):
        result=[]
        if self.comb_filter:
            result.extend(self.comb_filter)
        return result

    show_comb_filter=False

    def get_show_comb_filter(self):
        return self.show_comb_filter

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
            # data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    edit_link = []

    def get_edit_link(self):
        result=[]
        if self.edit_link:
            result.extend(self.edit_link)
        return result

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

    def default_action(self,request):
        pass


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

        comb_condition = {}
        option_list = self.get_comb_filter()
        print("request.GET.keys==",request.GET.keys())
        for key in request.GET.keys():
            value_list=request.GET.getlist(key)
            flag=False
            for option in option_list:
                print("option==%s"%option)
                print("value_list==",value_list)
                if option.field_name==key:
                    flag=True
                    break
            if flag:
                # print("comb_condition=",comb_condition["%s__in"%key])
                # print("value_list==",value_list)
                comb_condition["%s__in"%key]=value_list

        queryset=self.model_class.objects.filter(self.get_search_condition()).filter(**comb_condition).distinct()
        cl = ChangeList(self,queryset)
        return render(request,"stark/changelist.html",{"cl":cl})

    def add_view(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        _popbackid=request.GET.get("_popbackid")
        if request.method=="GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{"form":form,"config":self})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                #在数据库中创建数据
                new_obj=form.save()
                if _popbackid:
                    #是popup请求
                    #render一个页面，写自执行函数
                    result = {"status":False,"id":None, "text":None, "popbackid": _popbackid}
                    model_name=request.GET.get("model_name")
                    related_name=request.GET.get("related_name")
                    for related_object in new_obj._meta.related_objects:
                        _model_name=related_object.field.model._meta.model_name
                        _related_name=related_object.related_name
                        if (type(related_object) == ManyToOneRel):
                            _field_name=related_object.field_name
                        else:
                            _field_name = 'pk'
                        _limit_choices_to = related_object.limit_choices_to
                        if model_name==_model_name and related_name==str(_related_name):
                            is_exsits=self.model_class.objects.filter(**_limit_choices_to,pk=new_obj.pk).exists()
                            if is_exsits:
                                #如果新创建用户时,销售部的人，页面才增加
                                #分门别类做判断
                                result["status"]=True
                                result["text"]=str(new_obj)
                                result["id"]=getattr(new_obj,_field_name)
                                return render(request,"stark/popup_reponse.html",{"jsonresult":json.dumps(result,ensure_ascii=False)})
                    return render(request, "stark/popup_reponse.html",{"jsonresult": json.dumps(result, ensure_ascii=False)})
                else:
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
            print("form里都有啥====",form)
            return render(request,'stark/change_view.html',{'form':form})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                list_query_str=request.GET.get(self._query_param_key)
                list_url="%s?%s"%(self.get_list_url(),list_query_str,)
                return redirect(list_url)
            return render(request,'stark/change_view.html', {'form': form})

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