from django.shortcuts import render,redirect,HttpResponse
from rbac import models

# Create your views here.
def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    username=request.POST.get("username")
    password=request.POST.get("password")
    user_obj=models.User.objects.filter(username=username,password=password).first()
    if not user_obj:
        return render(request,"login.html",{"error":"用户名或密码错误"})
    else:
        permission_list=user_obj.role.values("permission__id",
                                             "permission__title",
                                             "permission__code",
                                             "permission__url",
                                             "permission__menu_gp",
                                             "permission__group_id",
                                             "permission__group__menu__title",
                                             "permission__group__menu_id").distinct()


        #权限相关
        result={}
        for item in permission_list:
            group_id=item["permission__group_id"]
            code=item["permission__code"]
            url=item["permission__url"]
            if group_id in result:
                result[group_id]["codes"].append(code)
                result[group_id]["urls"].append(url)
            else:
                result[group_id]={
                    "codes":[code,],
                    "urls":[url,]
                }

        #菜单相关
        menu_list={}
        for item in permission_list:
            if item["permission__menu_gp"]:
                continue
            menu_id=item["permission__group__menu_id"]
            if menu_id in menu_list:
                menu_list[menu_id]["children"].append({"title":item["permission__title"],"url":item["permission__url"],"active":True,"gid":item["permission__group_id"]})
            else:
                menu_list[menu_id]={
                    "menu_id":menu_id,
                    "menu_title":item["permission__group__menu__title"],
                    "active":True,
                    "children":[
                        {"title":item["permission__title"],"url":item["permission__url"],"active":True,"gid":item["permission__group_id"]}
                    ]
                }

        request.session["menulist"]=menu_list
        request.session["permission_dic"]=result
        return redirect("/userinfo/list/")

def index(request):
    codes = request.permission_codes
    menulist=request.session.get("menulist")
    print("menulist是个什么东西",menulist)
    return render(request,"index.html",{"codes":codes,"menulist":menulist})


def add(request):
    return HttpResponse("this is add page")