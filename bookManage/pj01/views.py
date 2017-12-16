from django.shortcuts import render,redirect,HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from pj01 import models
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Max,Min,Count,Sum,F,Q
from django.contrib import auth
import json
# Create your views here.
def login(request):
    if request.method=="POST":
        name=request.POST.get("username").strip()
        pwd=request.POST.get("password")
        user_obj=models.User.objects.filter(username=name,password=pwd).first()
        if user_obj:
            request.session["username"]=name
            return redirect("/admin/")
        else:
            return render(request, "login.html", {"status": "用户名或密码错误，请重新登陆"})
    return render(request,"login.html")


def auth_login(func):
      def inner(request,*args,**kwargs):
          name = request.session.get('username',None)
          if name:
            return func(request,*args,**kwargs)
          return redirect('/login/')
      return inner



@auth_login
def admin(request):
    book_list=models.Book.objects.all()
    username=request.session["username"]
    paginator=Paginator(book_list,5)
    page=request.GET.get("page",1)
    print("类型",type(page),"值是",page)
    currentPage = int(page)
    print("转换后的值是",currentPage,"类型",type(currentPage))
    book_list=paginator.page(currentPage)
    pages=paginator.num_pages

    if (currentPage>5) and (currentPage<pages-5):
        pageRange=range(currentPage-5,currentPage+5)
    else:
        if pages<10:
            pageRange = range(1,pages+1)
        elif (currentPage + 5 > pages):
            pageRange = range(pages - 9, pages+1)
        else:
            pageRange=range(1,11)

    return render(request,"admin.html",{'book_list':book_list,"username":username,"paginator":paginator,"currentPage":currentPage,"pageRange":pageRange})



@auth_login
def edit(request):
    # 编辑用户时通过 ajax 取得出版社、作者信息
    if request.POST.get("method")=="edit_ajax":
        auths=models.Author.objects.all()
        auth_list=[]
        for a in auths:
            auth_list.append({"id":a.id,"name":a.name})
        publishs=list(models.Publish.objects.all())
        publish_list=[]
        for p in publishs:
            publish_list.append({"id":p.id,"name":p.name})
        book_json={"publish":publish_list,"authlist":auth_list}
        return JsonResponse(book_json)
    if request.POST.get("method")=="edit_save":
        bookid=request.POST.get("bookid")
        title=request.POST.get("title")
        publishdate=request.POST.get("publishdate")
        publish=request.POST.get("publish")
        price=request.POST.get("price")
        wordnum=request.POST.get("wordnum")
        readnum=request.POST.get("readnum")
        authors=request.POST.getlist("authors")
        print("书籍ID==%s 书名%s 发布日期 %s 出版社 %s 价格%s 字数%s 阅读数%s 作者%s"%(bookid,title,publishdate,publish,price,wordnum,readnum,authors))
        #查出出版社的对象
        # publish_obj=models.Publish.objects.filter(id=publish).first()
        #查出所有作者
        auths=models.Author.objects.filter(id__in=authors)
        book_obj=models.Book.objects.filter(id=bookid).first()
        book_obj.authorlist.clear()             #更新前先清空旧对象再添加新对象
        for a in auths:
            book_obj.authorlist.add(a)
        models.Book.objects.filter(id=bookid).update(title=title,publishDate=publishdate,price=price,wordNum=wordnum,readNum=readnum,publish=publish)
        return redirect("/admin/")

@auth_login
def addbook(request):
    if request.GET.get("method")=="addbook":
        auths = models.Author.objects.all()
        publishs = models.Publish.objects.all()
        return render(request, "addbook.html",{"auths":auths,"publishs":publishs})
    elif request.POST.get("method")=="bookadd":
        # 添加一本书
        title = request.POST.get("title")
        publishdate = request.POST.get("publishdate")
        publish = request.POST.get("publish")
        price = request.POST.get("price")
        wordnum = request.POST.get("wordnum")
        readnum = request.POST.get("readnum")
        authors = request.POST.getlist("authors")
        # 查出出版社的对象
        publish_obj = models.Publish.objects.filter(id=publish).first()
        # 查出所有作者
        auths = models.Author.objects.filter(id__in=authors)
        print("所有的作者", auths)
        print("所有的出版社", publish,type(publish))
        book_obj=models.Book.objects.create(title=title, publishDate=publishdate, price=price, wordNum=wordnum,readNum=readnum,publish=publish_obj)
        for auth in auths:
            book_obj.authorlist.add(auth)
        return redirect("/admin/")



def delbook(request):
    bookid=request.GET.get("bookid")
    models.Book.objects.filter(id=bookid).delete()
    return redirect("/admin/")


@auth_login
def authors(request):
    authors=models.Author.objects.all()
    username=request.session["username"]
    return render(request,"authlist.html",{"auth_list":authors,"username":username})

@auth_login
def authlist(request):
    return redirect("/authors/")


@auth_login
def addauthlist(request):
    username = request.session["username"]
    return render(request,"addauthlist.html",{"username":username})

@auth_login
def addauth(request):
    if request.method=="POST":
        authname=request.POST.get("authname")
        age = request.POST.get("age")
        tel = request.POST.get("tel")
        addr=request.POST.get("addr")
        models.Author.objects.create(name=authname,age=age,tel=tel,addr=addr)
        return redirect("/authors/")
    else:
        return redirect("/addauthlist/")


@auth_login
def delauth(request):
    authid=request.GET.get("authid")
    models.Author.objects.get(id=authid).delete()
    return redirect("/authors/")

@auth_login
def editauth(request):
    if request.method=="GET":
        authid=request.GET.get("authid")
        auth_obj=models.Author.objects.get(id=authid)
        username = request.session["username"]
        return render(request,"editauthlist.html",{"auth_obj":auth_obj,"username":username})
    else:
        authid=request.POST.get("authid")
        authname=request.POST.get("authname")
        age=request.POST.get("age")
        tel=request.POST.get("tel")
        addr=request.POST.get("addr")
        models.Author.objects.filter(id=authid).update(name=authname,age=age,tel=tel,addr=addr)
        return redirect("/authors/")

@auth_login
def publishlist(request):
    publish_list=models.Publish.objects.all()
    username = request.session["username"]
    return render(request,"publishlist.html",{"publish_list":publish_list,"username":username})

@auth_login
def publish(request):
    return redirect("/publishlist/")

@auth_login
def addpublish(request):
    if request.method=="POST":
        pubname=request.POST.get("pubname")
        addr=request.POST.get("addr")
        models.Publish.objects.create(name=pubname,addr=addr)
        return redirect("/publishlist/")
    username = request.session["username"]
    return render(request,"addpublish.html",{"username":username})

@auth_login
def delpub(request):
    pid=request.GET.get("pid")
    models.Publish.objects.filter(id=pid).delete()
    return redirect("/publishlist/")


@auth_login
def editpublish(request):
    if request.method=="POST":
        pubname=request.POST.get("pubname")
        addr=request.POST.get("addr")
        publishid=request.POST.get("pid")
        models.Publish.objects.filter(id=publishid).update(name=pubname,addr=addr)
        return redirect("/publishlist/")
    else:
        pid=request.GET.get("pid")
        pub_obj=models.Publish.objects.filter(id=pid)[0]
        username = request.session["username"]
        return render(request,"editpublish.html",{"pub_obj":pub_obj,"username":username})

@auth_login
def systemuser(request):
    users=models.User.objects.all()
    username = request.session["username"]
    return render(request,"systemuser.html",{"users":users,"username":username})

@auth_login
def adduser(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    mail=request.POST.get("mail")
    tel=request.POST.get("telphone")
    models.User.objects.create(username=username,password=password,email=mail,tel=tel)
    return redirect("/systemuser/")


def delsystemuser(request):
    userid=request.GET.get("userid")
    models.User.objects.filter(id=userid).delete()
    return redirect("/systemuser/")


@auth_login
def edituser(request):
    if request.method=="GET":
        userid=request.GET.get("userid")
        user_obj=models.User.objects.filter(id=userid).first()
        username = request.session["username"]
        return render(request,"edituser.html",{"user_obj":user_obj,"username":username})
    else:
        uid = request.POST.get("uid")
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        tel=request.POST.get("tel")
        models.User.objects.filter(id=uid).update(username=username,password=password,email=email,tel=tel)
        return redirect("/systemuser/")


# def hello(request):
#     import time
#     # ps=request.POST.getlist("person")
#     # print(ps)
#     # num={"name":"张三","age":30}
#     # people={"name":"apple","price":20,"age":333,"num":num}
#     obj=HttpResponse("去你妈的")
#     obj.set_signed_cookie("login","hello",salt="wo")
#     time.sleep(2)
#     qianming=request.get_signed_cookie("login",salt="wo")
#     print("去你妈的是啥",qianming)
#     return obj


def log_out(request):
    request.session.flush()
    return redirect("/login/")


def ceshi(request):
    return render(request,"changepwd.html")


def register(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        mail = request.POST.get("mail")
        tel = request.POST.get("telphone")
        models.User.objects.create(username=username, password=password, email=mail, tel=tel)
        return redirect("/login/")
    return render(request,"register.html")


def changepwd(request):
    username = request.session["username"]
    if request.method=="GET":
        username=request.session["username"]
        return render(request,"changepwd.html",{"username":username})
    else:
        if request.POST.get("method")=="authpwd":
            oldpassword=request.POST.get("oldpassword")
            user_obj=None
            user_obj=models.User.objects.filter(password=oldpassword).first()
            if user_obj is None:
                return HttpResponse("false")
            return HttpResponse("true")
        if request.POST.get("method")=="upval":
            newpassword=request.POST.get("newpassword")
            models.User.objects.filter(username=username).update(password=newpassword)
            return redirect("/login/")
    return render(request,"changepwd.html",{"username":username})

