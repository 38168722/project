from django.shortcuts import render,HttpResponse,redirect
from django.template import Template,Context
from app01 import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def login(request):
    if request.method=="POST":
        import pymysql
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='auto')
        cursor = conn.cursor()
        name = request.POST.get("username")
        password = request.POST.get("password")
        sql = 'select * from user where name="%s" and password="%s"' % (name, password)
        ret = cursor.execute(sql)
        cursor.close()
        conn.close()
        if ret:
            return redirect("/app01/home")

        else:
            return HttpResponse("login failed")

    return render(request,'login.html')
# def register(request):
#     return render(request,'register.html')
#
# def article(request,year,mon):
#     return render(request,"article.html",{"year":year,"month":mon})
#
# def printinfo(request,year,mon):
#     return HttpResponse("年"+year+"月"+mon)
def home(request):
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        import pymysql
        conn = pymysql.connect(host="localhost", user="root", password="123456", database='auto')
        cursor = conn.cursor()
        name = request.POST.get("name")
        password = request.POST.get("password")
        sql = 'insert into user(name,password)values("%s","%s")' % (name, password)
        ret = cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        if ret:
            return redirect("/app01/login")
        else:
            return HttpResponse("register failed")
    return render(request,'register.html')

def db_handel(request):
    #增加
    # models.UserInfo.objects.create(username="alex",password="alex123",age=73)
    # dic={"username":"eric","password":"123","age":73}
    # models.UserInfo.objects.create(**dic)
    # return HttpResponse("ok")
    #删除
    # models.UserInfo.objects.filter(username="alex").delete()
    #修改
    # models.UserInfo.objects.all().update(age=18)
    #查找
    # models.UserInfo.objects.all()
    # models.UserInfo.objects.filter(age=18)
    # models.UserInfo.objects.filter(age=18).first()
    user_list_obj=models.UserInfo.objects.all()
    #会取得一个queryset，list
    # for line in user_list_obj:
    #     print(line.username,line.age)
    return render(request,'t1.html',{"li":user_list_obj})
    # print(HttpResponse("ok"))

def home(request):
    return render(request,'home.html')

def article(request):
    import datetime
    l=[111,222,333]
    dic={"name":"yuan","age":18}
    num=10
    date=datetime.datetime.now()
    class Person(object):
        def __init__(self,name):
            self.name=name
    time=datetime.datetime.now()
    yuan=Person("yuan")
    egon=Person("egon")
    alex=Person("alex")
    p_list=[yuan,egon,alex]
    value="hello world"
    chapter="Django version 1.11.6, using settings webproject.settings jango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settingsjango version 1.11.6, using settings webproject.settings"
    abc="<a href="">点我</a>"
    return render(request,'article.html',locals())

def index(request):
    print("files里有啥%s"%request.FILES)
    file_obj=request.FILES.get("upload_file_ajax")
    print("文件名是啥%s"%file_obj.name)
    with open(file_obj.name,"wb") as f:
        for i in file_obj:
            f.write(i)
    return HttpResponse("true")



    # num1=request.GET.get("num1")
    # num2=request.GET.get("num2")
    # result=int(num1)+int(num2)
    # return HttpResponse(result)

def base(request,no):

    return render(request,"base.html",{"no":no})

def son(request):
    return render(request,"son.html")

def upda(request):
    print("接收到的数据是",request.POST)
    print("******************************************")
    nid=request.POST.get("booknid")
    bookname=request.POST.get("bookname")
    author=request.POST.get("author")
    publishdate=request.POST.get("publishdate")
    price=request.POST.get("price")
    models.Book.objects.filter(nid=nid).update(title=bookname,author=author,publishDate=publishdate,price=price)
    return redirect("/book")
# def delitem(request,nid):
#     models.Book.objects.filter(nid=nid).delete()
#     return redirect("/book")
def delitem(request):
    nid=request.POST.get("nid")
    print("nid==",nid)
    obj=models.Book.objects.filter(nid=nid).delete()
    if obj:
        return HttpResponse("1")
    # return redirect("/book")

def addbook(request):
    # print("接收到的数据是",request.POST)
    # bookname=request.POST.get("bookname")
    # author=request.POST.get("author")
    # publishdate=request.POST.get("publishdate")
    # price=request.POST.get("price")
    # models.Book.objects.create(title=bookname,author=author,publishDate=publishdate,price=price)
    # return redirect("/book")
    pubObj=models.Publish.objects.filter(name="人民出版社")[0]
    models.Book.objects.create(title="云计算",price=90,publishDate="2013-09-12",publish=pubObj)
    models.Book.objects.create(title="linux",price=110,publishDate="2012-10-12",publish=pubObj)

    return HttpResponse("ok")

def query(request):
    print("进来了没")
    return HttpResponse("hello")
    # name="alex"
    # return render(request,"query.html",{"name":name})

def ajax_test(request):
    return render(request,"ajax_test.html")

def book(request):
    book_list=models.Book.objects.all()
    paginator=Paginator(book_list,5)
    page = request.GET.get('page',1)
    currentPage=int(page)
    book_list=paginator.page(page)
    pages=paginator.num_pages
    if (currentPage>5) and (currentPage<pages-5):
        pageRange=range(currentPage-5,currentPage+5)
    else:
        if (currentPage + 5 > pages):
            pageRange = range(pages - 9, pages+1)
        else:
            pageRange=range(1,11)


    return render(request,"bookManage.html",{"book_list":book_list,"paginator":paginator,"currentPage":currentPage,"pageRange":pageRange})

def booklist(request):
    import json
    method=request.POST.get("method")
    bid=request.POST.get("bid")
    if method=="addbook":
        bookname=request.POST.get("bookname")
        author=request.POST.get("author")
        publishdate=request.POST.get("publishdate")
        price=request.POST.get("price")
        publish=request.POST.get("publish")
        book_obj=models.Book.objects.create(title=bookname,author=author,publishDate=publishdate,price=price,publish_id=publish)
        if not book_obj:
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    if method=="delete":
        book_obj=models.Book.objects.filter(nid=bid).delete()
        if book_obj:
            return HttpResponse("true")
        else:
            return HttpResponse("false")

    booklist = models.Book.objects.all()
    publish = models.Publish.objects.all()
    print("booklist",booklist)
    return render(request,"booklist.html",{"booklist":booklist,"publish":publish})

def upload_file(request):
    print("FILES:",request.FILES)
    print("POST:",request.POST)
    return HttpResponse("上传成功!")