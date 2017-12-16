from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from rbac.service.init_permission import init_permission
# Create your views here.

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        user=models.User.objects.filter(username=user,password=pwd).first()
        print(request.POST)
        if not user:
            return render(request,"login.html")
        init_permission(user,request)
        return redirect('/index/')


def index(request):
    return HttpResponse('欢迎登录')

class BasePagePermission(object):
    def __init__(self,code_list):
        self.code_list=code_list

    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_edit(self):
        if 'edit' in self.code_list:
            return True

    def has_del(self):
        if 'del' in self.code_list:
            return True

def userinfo(request):
    page_permission=BasePagePermission(request.permission_code_list)
    data_list = [
        {'id':1,'name':'xxx1'},
        {'id':2,'name':'xxx2'},
        {'id':3,'name':'xxx3'},
        {'id':4,'name':'xxx4'},
        {'id':5,'name':'xxx5'},
    ]

    return render(request,'userinfo.html',{'data_list':data_list,'page_permission':page_permission})

def userinfo_add(request):
    page_permission=BasePagePermission(request.permission_code_list)
    return HttpResponse('添加用户页面')

class OrderPagePermission(BasePagePermission):
    def has_report(self):
        if 'report' in self.code_list:
            return True

def order(request):
    order_permission=OrderPagePermission(request.permission_code_list)
    return render(request,"order.html")

def order_add(request):
    return HttpResponse('添加订单页面')