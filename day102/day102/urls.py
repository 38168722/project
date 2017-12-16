"""day102 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import HttpResponse, render, redirect


def list_view(request):
    return HttpResponse("列表页面")


def add_view(request):
    return HttpResponse("添加页面")


def delete_view(request, nid):
    return HttpResponse("删除页面")


def edit_view(request, nid):
    return HttpResponse("编辑页面")


# def get_urls():
#     temp = [
#         url(r'^$'.format(app_name,cls_name),list_view),
#         url(r'^add/$'.format(app_name,cls_name),add_view),
#         url(r'^del/$'.format(app_name,cls_name),delete_view),
#         url(r'^change/$'.format(app_name,cls_name),edit_view),
#     ]
#     return temp

# url_list=[]
# for model_class,v in admin.site._registry.items():
#     #当前类名小写
#     cls_name = model_class._meta.model_name
#     #当前类所在的app名称
#     app_name = model_class._meta.app_label
#
#     all_url = url(r'^{0}/{1}/'.format(app_name,cls_name),include(get_urls()))
#
#     url_list.append(all_url)
#
#     # list_url = url(r'^%s/%s/$'%(app_name,cls_name),list_view)
#     # url_list.append(list_url)
#     #
#     # add_url = url(r'^%s/%s/add/$'%(app_name,cls_name),add_view)
#     # url_list.append(add_url)
#     #
#     # del_url = url(r'^%s/%s/(\d+)/del/$'%(app_name,cls_name),delete_view)
#     # url_list.append(del_url)
#     #
#     # change_url = url(r'^%s/%s/(\d+)/change/$'%(app_name,cls_name),edit_view)
#     # url_list.append(change_url)
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^ceshi/',(url_list,None,None)),
# ]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/userinfo/',[[
        url(r'^$',list_view,name="login"),
    ],None,None],None,None),
    url(r'^app02/userinfo/',[[
        url(r'^$',list_view,name="login"),
    ],None,None],None,None)
]

reversed("login")



# def changelist_view(request):
#     return HttpResponse("列表页面")
#
# def add_view(request):
#     return HttpResponse("添加页面")
#
# def delete_view(request,nid):
#     return HttpResponse("删除页面")
#
# def change_view(request,nid):
#     return HttpResponse("修改页面")
#
# def get_urls():
#     temp = [
#         url(r'^$'.format(app_name, cls_name), changelist_view),
#         url(r'^add/$'.format(app_name, cls_name), add_view),
#         url(r'^del/$'.format(app_name, cls_name), delete_view),
#         url(r'^change/$'.format(app_name, cls_name), change_view)
#     ]
#     return temp
#
# url_list=[]
#
# for model_class,v in admin.site._registry.items():
#     cls_name = model_class._meta.model_name
#     app_name = model_class._meta.app_label
#     print("cls_name==",cls_name)
#     print("app_name==",app_name)
