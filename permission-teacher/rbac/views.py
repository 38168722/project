from django.shortcuts import render,redirect,HttpResponse
from rbac import models
# Create your views here.
def login(request):
    obj=models.User.objects.filter(username="肾松").first()
    roles=obj.roles.all()
    for role in roles:
        print(role.title)
    p_l=obj.roles.values("permissions__title",'permissions__url')
    print("权限列表%s"%p_l)
    print(obj.username)
    return HttpResponse("ok")