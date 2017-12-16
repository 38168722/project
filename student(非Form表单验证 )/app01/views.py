from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django.http import JsonResponse
from django.forms import Form,fields,widgets
import json
# Create your views here.

def login(request):
    if request.POST:
        name=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=None
        user_obj=models.User.objects.filter(name=name,password=password).first()
        if user_obj is not None:
            request.session["username"] = name
            return redirect("/index/")
        else:
            return render(request, "login.html",{"status":"帐号或密码错误请重新登陆"})
    return render(request,"login.html")

#装饰器验证用户是否登录成功
def auth_login(func):
    def inner(request, *args, **kwargs):
        name = request.session.get('username', None)
        if name:
            return func(request, *args, **kwargs)
        return redirect('/login/')
    return inner

@auth_login
def index(request):
    teacher_list = models.Teacher.objects.all()
    return render(request, "index.html", {"teacher_list": teacher_list})

@auth_login
def teacher_opr(request):

    if request.POST.get("method")=="ajax_edit":
        classlist=models.Classes.objects.all().only("id","name")
        courselist=models.Course.objects.all().only("id","name")
        utlist=models.UserType.objects.all().only("id","name")
        class_l=[]
        for i in classlist:
            class_l.append({"id":i.id,"name":i.name})
        course_l=[]
        for i in courselist:
            course_l.append({"id":i.id,"name":i.name})
        ut_l=[]
        for i in utlist:
            ut_l.append({"id":i.id,"name":i.name})

        datas={"classeslist":class_l,"courselist":course_l,"utlist":ut_l}
        return JsonResponse(datas)

    elif request.POST.get("method")=="teacheradd":
         name=request.POST.get("name")
         age=request.POST.get("age")
         sex=request.POST.get("sex")
         tel=request.POST.get("tel")
         salary=request.POST.get("salary")
         classes=request.POST.getlist("classes")
         course=request.POST.getlist("course")
         usertype=request.POST.get("usertype")
         usertype_obj=models.UserType.objects.get(id=usertype)
         teacher_obj=models.Teacher.objects.create(name=name,age=age,sex=sex,tel=tel,salary=salary,userType=usertype_obj)
         course_list=models.Course.objects.filter(id__in=course)
         classes_list=models.Classes.objects.filter(id__in=classes)
         #添加course 、classes 数据到教师表中
         teacher_obj.course_list.add(*course_list)
         teacher_obj.class_list.add(*classes_list)
         return redirect("/index/")

    elif request.GET.get("method")=="teacherdel":
         tid=request.GET.get("tid")
         models.Teacher.objects.filter(id=tid).delete()
         return redirect("/index/")

    elif request.POST.get("method")=="teacherupdate":
        tid=request.POST.get("tid")
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        tel = request.POST.get("tel")
        salary = request.POST.get("salary")
        classes = request.POST.getlist("classes")
        course = request.POST.getlist("course")
        usertype = request.POST.get("usertype")
        usertype_obj = models.UserType.objects.get(id=usertype)
        course_list = models.Course.objects.filter(id__in=course)
        classes_list = models.Classes.objects.filter(id__in=classes)
        # 添加course 、classes 数据到教师表中
        teacher_obj=models.Teacher.objects.filter(id=tid)
        teacher_obj[0].course_list.clear()
        teacher_obj[0].class_list.clear()
        teacher_obj[0].course_list.add(*course_list)
        teacher_obj[0].class_list.add(*classes_list)
        teacher_obj.update(name=name, age=age, sex=sex, tel=tel, salary=salary, userType=usertype_obj)

        return redirect("/index/")

    elif request.GET.get("method")=="tedit":
        tid=request.GET.get("tid")
        teacher_obj=models.Teacher.objects.get(id=tid)
        classlist = models.Classes.objects.all().only("id", "name")
        courselist = models.Course.objects.all().only("id", "name")
        utlist = models.UserType.objects.all().only("id", "name")
        sel_classlist=[]
        sel_courselist=[]
        edit_teacher_class_obj=teacher_obj.class_list.all().values("id")
        edit_course_class_obj=teacher_obj.course_list.all().values("id")
        for obj in edit_teacher_class_obj:
            sel_classlist.append(obj.get("id"))
        for obj in edit_course_class_obj:
            sel_courselist.append(obj.get("id"))
        return render(request,"teacheredit.html",{"sel_classlist":sel_classlist,"sel_courselist":sel_courselist,"teacher_obj":teacher_obj,"classlist":classlist,"courselist":courselist,"utlist":utlist})

    return HttpResponse("你有误操作，页面不存在!")

@auth_login
def testh(request):
    return render(request,"studentedit.html")

@auth_login
def student_opr(request):
    if request.GET.get("method")=="studentdel":
        tid=request.GET.get("tid")
        models.Student.objects.filter(id=tid).delete()
        return redirect("/student/")

    elif request.GET.get("method")=="sedit":
        sid=request.GET.get("sid")
        student_obj=models.Student.objects.filter(id=sid)[0]
        course_list=models.Course.objects.all()
        class_list=models.Classes.objects.all()
        return render(request,"studentedit.html",{"student_obj":student_obj,"course_list":course_list,"class_list":class_list})

    elif request.POST.get("method")=="updatestudent":
        sid=request.POST.get("sid")
        name=request.POST.get("name")
        sex=request.POST.get("sex")
        classes=request.POST.get("classes")
        course=request.POST.get("course")
        models.Student.objects.filter(id=sid).update(name=name,sex=sex,classes=classes,course=course)
        return redirect("/student/")

    elif request.POST.get("method") == "studentadd":
        name=request.POST.get("name")
        sex=request.POST.get("sex")
        classes=request.POST.get("classes")
        class_obj=models.Classes.objects.get(id=classes)
        course=request.POST.get("course")
        course_obj=models.Course.objects.get(id=course)
        models.Student.objects.create(name=name,sex=sex,classes=class_obj,course=course_obj)
        return redirect("/student/")

    elif request.POST.get("method") == "studentdel":
        sid=request.GET.get("tid")
        models.Student.objects.filter(id=sid).delete()
        return redirect("/student/")
    student_list=models.Student.objects.all()
    course_list=models.Course.objects.all()
    classes_list=models.Classes.objects.all()
    return render(request,"studentindex.html",{"student_list":student_list,"course_list":course_list,"classes_list":classes_list})

@auth_login
def userType_opr(request):
    if request.GET.get("method")=="usertypedel":
        uid=request.GET.get("uid")
        models.UserType.objects.filter(id=uid).delete()
        return redirect("/userType/")
    elif request.GET.get("method")=="utedit":
        uid=request.GET.get("uid")
        ut_obj=models.UserType.objects.get(id=uid)
        return render(request,"usertypeedit.html",{"ut_obj":ut_obj})
    elif request.GET.get("method")=="updateuserType":
        uid=request.GET.get("uid")
        name=request.GET.get("name")
        models.UserType.objects.filter(id=uid).update(name=name)
        return redirect("/userType/")
    elif request.POST.get("method")=="usertypeadd":
        name=request.POST.get("name")
        models.UserType.objects.create(name=name)
        return redirect("/userType/")

    ut_all=models.UserType.objects.all()
    return render(request,"userTypeindex.html",{"ut_all":ut_all})

@auth_login
def classes_opr(request):
    if request.GET.get("method")=="classesdel":
        cid=request.GET.get("cid")
        models.Classes.objects.filter(id=cid).delete()
        return redirect("/classes/")
    elif request.GET.get("method")=="classedit":
        cid=request.GET.get("cid")
        class_obj=models.Classes.objects.filter(id=cid)[0]
        return render(request,"classedit.html",{"class_obj":class_obj})
    elif request.POST.get("method")=="updateclasses":
        cid=request.POST.get("cid")
        name=request.POST.get("name")
        models.Classes.objects.filter(id=cid).update(name=name)
        return redirect("/classes/")
    elif request.POST.get("method") == "classesadd":
        name=request.POST.get("name")
        models.Classes.objects.create(name=name)
        return redirect("/classes/")

    class_list = models.Classes.objects.all()
    return render(request,"classindex.html",{"class_list":class_list})

@auth_login
def course_opr(request):
    if request.POST.get("method")=="courseadd":
        name=request.POST.get("name")
        price=request.POST.get("price")
        period=request.POST.get("period")
        models.Course.objects.create(name=name,price=price,period=period)
        return redirect("/course/")
    elif request.GET.get("method") == "coursedit":
        cid=request.GET.get("cid")
        course_obj=models.Course.objects.get(id=cid)
        return render(request,"courseedit.html",{"course_obj":course_obj})
    elif request.POST.get("method") == "updatecourse":
        cid = request.POST.get("cid")
        name=request.POST.get("name")
        price=request.POST.get("price")
        period=request.POST.get("period")
        models.Course.objects.filter(id=cid).update(name=name,price=price,period=period)
        return redirect("/course/")
    elif request.GET.get("method") == "coursedel":
        cid = request.GET.get("cid")
        models.Course.objects.filter(id=cid).delete()
        return redirect("/course/")
    course_list=models.Course.objects.all()
    return render(request,"courseindex.html",{"course_list":course_list})

@auth_login
def log_out(request):
    del request.session["username"]
    return redirect("/login/")

@auth_login
def sysuser(request):
    if request.POST.get("method")=="autholdpasswd":
        password=request.POST.get("oldpassword")
        user_obj=models.User.objects.filter(password=password)
        if user_obj:
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    elif request.GET.get("method")=="changpwd":
        return render(request,"sysuseredit.html")
    elif request.POST.get("method")=="updateuser":
        password=request.POST.get("repassword")
        username=request.session["username"]
        models.User.objects.filter(name=username).update(password=password)
        return redirect("/login/")

def testh(request):
    return redirect("http://www.baidu.com/?method=hello")