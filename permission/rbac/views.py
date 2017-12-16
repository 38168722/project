from django.shortcuts import render,redirect,HttpResponse
from rbac.service.init_permission import init_permission
from rbac import models
# Create your views here.
def login(request):
    if request.method=="GET":
        print("去你妹的....")
        return render(request,"login.html")
    else:
        username=request.POST.get("user")
        password=request.POST.get("pwd")
        obj=models.User.objects.filter(username=username,password=password).first()
        if not obj:
            return render(request, "login.html",{"status":"帐号或密码错误"})
        else:
            permission_list = obj.roles.values("permissions__title",
                                               "permissions__url",
                                               "permissions__is_menu",
                                               "permissions__code",
                                               "permissions__groups_id")

            print("都有哪些权限%s"%permission_list)

            return HttpResponse("this is ok page")


