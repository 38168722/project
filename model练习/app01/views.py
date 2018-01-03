from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render,redirect,HttpResponse
from app01.modelForms import *
from app01 import models
# Create your views here.

def edit(request):

    if request.method=="POST":
        uid = request.GET.get("uid")
        obj = models.UserInfo.objects.get(id=uid)
        mf=UserInfoModelForm(request.POST,instance=obj)
        if mf.is_valid():
            mf.save()
        return redirect("/index/")
    else:
        uid = request.GET.get("uid")
        obj = models.UserInfo.objects.get(id=uid)
        user = UserInfoModelForm(instance=obj)
        return render(request,"edit.html",{"user":user})


def list_user(request):
    if request.method=="POST":
        pass
    else:
        departId=request.GET.get("departId","88")
        params = QueryDict(mutable=True)
        params['_list_filter'] = request.GET.urlencode()
        list_condition = params.urlencode()

        print("departId==",departId)
        roleId=request.GET.get("roleId")
        condition = Q()
        condition.connector="or"
        depart_all=models.Department.objects.all()
        if departId=="88":
            data_all=models.UserInfo.objects.all()
        else:
            data_all=models.UserInfo.objects.filter(department_id=departId)
        role_all=models.Role.objects.filter()
        return render(request,"userlist.html",{"userall":data_all,"depart":depart_all,"role":role_all,"departId":int(departId)})
