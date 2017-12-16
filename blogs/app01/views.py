from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from app01 import forms
from django.db.models import Count,Sum
from django.db.models import F
from django.db import transaction
from django.http import JsonResponse
import datetime
import json
#滑动模块验证码的包
from app01.geetest import GeetestLib
# Create your views here.
def login(request):
    # if request.method=="POST":
    #     if user.is_valid():
    #         del user.cleaned_data['validCode']
    #         user_obj=models.User.objects.filter(**user.cleaned_data).first()
    #         if not user_obj:
    #             return HttpResponse("false")
    #         request.session["username"]=user.cleaned_data.get("username")
    #         request.session["userid"]=user_obj.id
    #         return HttpResponse("true")
    #     return HttpResponse(json.dumps(user.errors))
    # else:
    #     user=forms.UserForm(request)
    user = forms.UserForm(request, request.POST)
    return render(request,"login.html",{"form":user})

def index(request,*args,**kwargs):
    print(kwargs)
    if kwargs:
        article_list=models.Article.objects.filter(site_article_category__name=kwargs.get("site_article_category"))
    else:
        article_list = models.Article.objects.all()
    SiteCategory=models.SiteCategory.objects.all()
    return render(request,"index.html",{"SiteCategory":SiteCategory,"article_list":article_list})

def register(request):
    if request.is_ajax():
        user=forms.UserRegisterForm(request.POST)
        if user.is_valid():
            file_obj = request.FILES.get("avatar","/avatar/default.png")
            user.cleaned_data["avatar"]=file_obj
            user.cleaned_data["create_time"]=datetime.datetime.now()
            del user.cleaned_data["repassword"]
            models.User.objects.create(**user.cleaned_data)
            return HttpResponse("true")
        else:
            print(user.errors)
            return HttpResponse(json.dumps(user.errors))
    user = forms.UserRegisterForm()
    return render(request,"register.html",{"form":user})

def getvalicode(request):
    from io import BytesIO
    import random
    from PIL import Image,ImageDraw,ImageFont
    img = Image.new(mode="RGB",size=(120,40),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw = ImageDraw.Draw(img,"RGB")
    font=ImageFont.truetype("blogs/static/font/kumo.ttf",25)
    valid_list=[]
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_lower_zimu=chr(random.randint(65,90))
        random_upper_zimu=chr(random.randint(97,122))
        random_char=random.choice([random_num,random_lower_zimu,random_upper_zimu])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)
    f=BytesIO()
    img.save(f,"png")
    data=f.getvalue()
    valid_str="".join(valid_list)
    print(valid_str)
    request.session["keepValidCode"]=valid_str
    return HttpResponse(data)

def homeSite(request,username,**kwargs):
    #查询当前用户
    current_user=models.User.objects.filter(username=username).first()
    if not current_user:
        return render(request,"notFound.html")

    #查询当前用户的日期归档
    date_list=models.Article.objects.filter(user=current_user).extra(select={"filter_create_date":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("id"))
    if kwargs:
        if kwargs.get("condition")=="category":
            article_list=models.Article.objects.filter(user=current_user,category__title=kwargs.get("para"))
        elif kwargs.get("condition")=="tag":
            article_list=models.Article.objects.filter(user=current_user,tags__title=kwargs.get("para"))
        elif kwargs.get("condition")=="date":
            year,month=kwargs.get("para").split("/")
            article_list=models.Article.objects.filter(user=current_user,create_time__year=year,create_time__month=month)

    #查询用户文章详细信息
    if kwargs.get("article_id"):
        article=models.Article.objects.filter(id=kwargs.get("article_id")).first()
        obj=render(request,"articleDetail.html",{"user": current_user,"article": article,"date_list":date_list})
        obj.set_cookie("username",request.session.get("username"))
        obj.set_cookie("articleid",article.id)
        return obj

    # 查询当前用户的所有文章
    article_list=models.Article.objects.filter(user=current_user)
    return render(request,"homesite.html",{"user":current_user,"article_list":article_list,"date_list":date_list})

def logout(request):
    del request.session["username"]
    return redirect("/login/")

def test01(request):
    return render(request, "Categorymanager.html")

def poll(request):
    from django.db.models import F
    userid=request.session.get("userid")
    articleid=request.POST.get("articleid")
    try:
        with transaction.atomic():
            models.ArticleUp.objects.create(user_id=userid,article_id=articleid)
            models.Article.objects.filter(id=articleid).update(up_count=F("up_count")+1)
        return HttpResponse("true")
    except:
        return HttpResponse("false")

def sub_comment(request):
    content=request.POST.get("content")         #用户评论
    articleid=request.POST.get("articleid")
    userid=request.session.get("userid")
    commmentResponse={"status":False}
    parentId=request.POST.get("parentId")
    #加载用户评论
    if request.POST.get("action"):
        comment_list = models.Comment.objects.filter(article_id=request.POST.get("articleid")).values("id", "content","pid_id","user__username","create_time","user__blog__site","user__avatar")
        comment_dict = {}
        for comment in comment_list:
            comment["children"] = []
            comment_dict[comment["id"]] = comment
        commentTree = []
        for k, v in comment_dict.items():
            if not v["pid_id"]:
                commentTree.append(v)
            else:
                comment_dict[v["pid_id"]]["children"].append(v)
        return JsonResponse(commentTree,safe=False)
    if not parentId:
        with transaction.atomic():
            # 用户评论xss过滤
            from blogs.plugins import xss_plugin
            content = xss_plugin.filter_xss(content)
            print("过滤后的内容是啥%s" % content)

            comment_obj=models.Comment.objects.create(content=content,article_id=articleid,user_id=userid)
            models.Article.objects.filter(id=articleid).update(comment_count=F("comment_count")+1)
            commmentResponse["create_time"]=str(comment_obj.create_time)
    else:
        with transaction.atomic():
            # 用户评论xss过滤
            from blogs.plugins import xss_plugin
            content = xss_plugin.filter_xss(content)
            print("过滤后的内容是啥%s" % content)

            comment_obj=models.Comment.objects.create(article_id=articleid,user_id=userid,content=content,pid_id=parentId)
            models.Article.objects.filter(id=articleid).update(comment_count=F("comment_count")+1)
            commmentResponse["create_time"]=str(comment_obj.create_time)
            commmentResponse["status"]=True
    return JsonResponse(commmentResponse)

def uploadFile(request):
    from blogs import settings
    print("POST",request.POST)
    print("FILES",request.FILES)
    file_obj=request.FILES.get("imgFile")
    file_name=file_obj.name
    import os
    path=os.path.join(settings.MEDIA_ROOT,"article_uploads",file_name)
    with open(path,"wb") as f:
        for i in file_obj.chunks():
            f.write(i)

    response={
        "error":0,
        "url":"/media/article_uploads/"+file_name+"/"
    }

    import json
    return HttpResponse(json.dumps(response))

#滑动模块验证码函数
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"

def home(request):
    return render(request, "index.html",)

def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

def mobilegetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(mobile_geetest_id, mobile_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

# def pcvalidate(request):
#     if request.method == "POST":
#         gt = GeetestLib(pc_geetest_id, pc_geetest_key)
#         challenge = request.POST.get(gt.FN_CHALLENGE, '')
#         validate = request.POST.get(gt.FN_VALIDATE, '')
#         seccode = request.POST.get(gt.FN_SECCODE, '')
#         status = request.session[gt.GT_STATUS_SESSION_KEY]
#         user_id = request.session["user_id"]
#         if status:
#             result = gt.success_validate(challenge, validate, seccode, user_id)
#         else:
#             result = gt.failback_validate(challenge, validate, seccode)
#         if result:
#             return HttpResponse("true")
#         else:
#             return HttpResponse(json.dumps(user.errors))
#         # result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
#         # return HttpResponse(result)

def pcajax_validate(request):
    if request.method == "POST":
        login_response = {"is_login": False, "error_msg": None}
        # 验证验证码
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        #扩充验证用户名密码
        user = forms.UserForm(request, request.POST)
        if result:
            if user.is_valid():
                del user.cleaned_data['validCode']
                user_obj = models.User.objects.filter(**user.cleaned_data).first()
                if not user_obj:
                    return HttpResponse(json.dumps(user.errors))
                request.session["username"] = user.cleaned_data.get("username")
                request.session["userid"] = user_obj.id
                return HttpResponse("true")
        return HttpResponse(json.dumps(user.errors))

def mobileajax_validate(request):
    if request.method == "POST":
        gt = GeetestLib(mobile_geetest_id, mobile_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")

def manager(request):
    import datetime
    if request.method=="POST":
        print("到底是个什么值%s" % request.POST.get("action"))
        if request.POST.get("action")=="addArticle":
            title=request.POST.get("title")
            content=request.POST.get("content")
            category=request.POST.get("category")
            tags=request.POST.getlist("tag")
            with transaction.atomic():
                obj=models.Article.objects.create(title=title,desc=content[:60],category_id=category,create_time=datetime.datetime.now(),user_id=request.session.get("userid"))
                models.ArticleDetail.objects.create(content=content,article_id=obj.id)
                for item in tags:
                    models.Article2Tag.objects.create(article_id=obj.id,tag_id=item)
            return HttpResponse("true")
        if request.POST.get("action")=="updateArticle":
            print("进来更新了没有")
            articleId=request.POST.get("articleId")
            print("文章id是多少%s"%articleId)
            title=request.POST.get("title")
            content=request.POST.get("content")
            category=request.POST.get("category")
            tags=request.POST.getlist("tag")
            print("标签都有哪些%s"%tags)
            print("类型都有哪些%s"%category)
            with transaction.atomic():
                obj=models.Article.objects.filter(id=articleId)
                obj.update(title=title,desc=content[:60],category_id=category,create_time=datetime.datetime.now())
                models.ArticleDetail.objects.filter(id=articleId).update(content=content)
                # models.Tag.objects.filter(article=obj[0]).delete()
                obj[0].tags.clear()   #清除与标签的关系
                for item in tags:
                    models.Article2Tag.objects.create(article=obj[0],tag_id=item)
            return HttpResponse("true")
        elif request.POST.get("action")=="del":
            articleid=request.POST.get("articleid")
            models.Article.objects.filter(id=articleid).delete()
            return HttpResponse("true")
        elif request.POST.get("action")=="category_del":
            categoryId=request.POST.get("categoryId")
            models.Category.objects.filter(id=categoryId).delete()
            return HttpResponse("true")
        elif request.POST.get("action")=="addCategory":
            title=request.POST.get("title")
            with transaction.atomic():
                blog_obj=models.Blog.objects.filter(user_id=request.session.get("userid"))
                models.Category.objects.create(title=title,blog=blog_obj[0])
            return HttpResponse("true")
        elif request.POST.get("action")=="updateCategory":
            title=request.POST.get("title")
            categoryId=request.POST.get("categoryId")
            models.Category.objects.filter(id=categoryId).update(title=title)
            return HttpResponse("true")
        elif request.POST.get("action")=="updateTag":
            title=request.POST.get("title")
            tagId=request.POST.get("tagId")
            models.Tag.objects.filter(id=tagId).update(title=title)
            return HttpResponse("true")
        elif request.POST.get("action")=="addTag":
            title=request.POST.get("title")
            with transaction.atomic():
                blog_obj=models.Blog.objects.filter(user_id=request.session.get("userid"))
                models.Tag.objects.create(title=title,blog=blog_obj[0])
            return HttpResponse("true")
        elif request.POST.get("action")=="tag_del":
            tagId=request.POST.get("tagId")
            models.Tag.objects.filter(id=tagId).delete()
            return HttpResponse("true")
    else:
        if request.GET.get("action")=="articleEditor":
            articleId=request.GET.get("articleId")
            article_obj=models.Article.objects.get(id=articleId)
            category_list=models.Category.objects.filter(blog__user_id=request.session.get("userid"))
            tag_list=models.Tag.objects.filter(blog__user_id=request.session.get("userid"))
            return render(request,"ArticleEditor.html",{"article":article_obj,"category_list":category_list,"tag_list":tag_list})
        if request.GET.get("action")=="category_manager":
            category_list = models.Category.objects.filter(blog__user_id=request.session.get("userid"))
            return render(request,"Categorymanager.html",{"category_list":category_list})
        if request.GET.get("action")=="categoryEditor":
            categoryId=request.GET.get("categoryId")
            category_obj = models.Category.objects.filter(id=categoryId)
            return render(request,"CategoryEditor.html",{"category":category_obj[0]})
        if request.GET.get("action")=="tagEditor":
            tagId=request.GET.get("tagId")
            tag_obj = models.Tag.objects.filter(id=tagId)
            return render(request,"TagEditor.html",{"tag":tag_obj[0]})
        if request.GET.get("action")=="tag_manager":
            tags=models.Tag.objects.filter(blog__user__id=request.session.get("userid"))
            return render(request,"tagManager.html",{"tags":tags})
        else:
            article_list=models.Article.objects.filter(user__id=request.session.get("userid"))
            category_list=models.Category.objects.filter(blog__user__id=request.session.get("userid"))
            tag_list=models.Tag.objects.filter(blog__user__id=request.session.get("userid"))
            obj=render(request,"Articlemanager.html",{"article_list":article_list,"category_list":category_list,"tag_list":tag_list})
            obj.cookies["username"]=request.session.get("username")
            return obj


