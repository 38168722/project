from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django.http import JsonResponse
from django.forms import Form,fields,widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import json
# Create your views here.

class LoginForm(Form):
    name=fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required':'用户不能为空',
            'min_length':'用户长度不能小于3',
            'max_length':'用户长度不能大于18',
        }
    )
    password=fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
         'required':'密码不能为空',
         'min_length':'密码长度不能小于3',
          'max_length':'密码长度不能大于18',
          'invalid':'密码格式错误',
        },
        # validators=[RegexValidator('\d+','只能是数字')]
    )
    def clean_name(self):
        user=self.cleaned_data['name']
        is_exsit=models.User.objects.filter(name=user).count()
        print("有数据没有%s"%is_exsit)
        if not is_exsit:
            print("滚蛋")
            raise ValidationError("用户名不存在")
        return user
    # def clean_password(self):
    #     user=self.cleaned_data['name']
    #     return user

class TeacherForm(Form):
    name = fields.CharField(
        required=True,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','id':'name'})
    )
    age = fields.IntegerField(
        required=True,
        error_messages={'required': '年龄不能为空'},
        widget=widgets.NumberInput(attrs={'class':'form-control','id':'age'})
    )
    sex = fields.CharField(
        required=True,
        error_messages={'required': '性别不能为空'},
        widget = widgets.TextInput(attrs={'class': 'form-control', 'id': 'sex'})
    )
    tel = fields.IntegerField(
        required=True,
        error_messages={'required': '电话不能为空'},
        widget=widgets.NumberInput(attrs={'class': 'form-control', 'id': 'tel'})
    )
    salary = fields.IntegerField(
        required=True,
        error_messages={'required': '薪水不能为空'},
        widget=widgets.NumberInput(attrs={'class': 'form-control', 'id': 'salary'})
    )
    class_list = fields.MultipleChoiceField(
        choices=models.Classes.objects.values_list("id", "name"),
        widget=widgets.SelectMultiple(attrs={'class': 'form-control', 'id': 'classes'})
    )
    course_list = fields.MultipleChoiceField(
        choices=models.Course.objects.values_list("id", "name"),
        widget=widgets.SelectMultiple(attrs={'class': 'form-control', 'id': 'course'})
    )
    userType = fields.ChoiceField(
        choices=models.UserType.objects.values_list("id", "name"),
        widget=widgets.Select(attrs={'class': 'form-control', 'id': 'usertype'})
    )

def login(request):
    if request.method=="GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    elif request.method=="POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            #验证成功
            user = models.User.objects.filter(**form.cleaned_data).first()
            if not user:
                form.add_error('password',ValidationError('用户名或密码错误'))
                return render(request,'login.html',{'form':form})
            else:
                request.session['username']=form.cleaned_data['name']
                return redirect('/index/')
        else:
            #验证失败
            return render(request,'login.html',{'form':form})
    else:
        return HttpResponse('滚蛋')

def index(request):
    teacher_list = models.Teacher.objects.all()
    form=TeacherForm()
    return render(request, "index.html", {"teacher_list": teacher_list,"form":form})

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

    if request.POST.get("method")=="teacheradd":
         form=TeacherForm(data=request.POST)
         if form.is_valid():
             usertype_obj=models.UserType.objects.get(id=form.cleaned_data["userType"])
             teacher_obj=models.Teacher.objects.create(
                                            name=form.cleaned_data["name"],
                                            age=form.cleaned_data["age"],
                                           sex=form.cleaned_data["sex"],
                                           tel=form.cleaned_data["tel"],
                                           salary=form.cleaned_data["salary"],
                                           userType=usertype_obj)
             course_l = form.cleaned_data["course_list"]
             class_l = form.cleaned_data["class_list"]
             teacher_obj.class_list.set(class_l)
             teacher_obj.course_list.set(course_l)
             return redirect("/index/")
         else:
             return HttpResponse("输入所有错误^%s"%form.errors)

    elif request.GET.get("method")=="teacherdel":
         tid=request.GET.get("tid")
         models.Teacher.objects.filter(id=tid).delete()
         return redirect("/index/")

    elif request.POST.get("method")=="teacherupdate":
        id=request.POST.get("tid")
        form = TeacherForm(data=request.POST)
        if form.is_valid():
            teacher_obj=models.Teacher.objects.filter(id=id)
            course_l = form.cleaned_data.pop('course_list')
            class_l = form.cleaned_data.pop('class_list')
            teacher_obj[0].course_list.set(course_l)
            teacher_obj[0].class_list.set(class_l)
            teacher_obj.update(**form.cleaned_data)
            return redirect("/index/")
    elif request.GET.get("method")=="tedit":
        tid=request.GET.get("tid")
        teacher_obj=models.Teacher.objects.get(id=tid)
        form = TeacherForm(initial={'name':teacher_obj.name,
                                    'age':teacher_obj.age,
                                    'sex':teacher_obj.sex,
                                    'tel':teacher_obj.tel,
                                    'salary':teacher_obj.salary,
                                    'class_list':[row.id for row in teacher_obj.class_list.all()],
                                    'course_list':[row.id for row in teacher_obj.course_list.all()],
                                    'userType':teacher_obj.userType.id,
                                    })
        return render(request,"teacheredit.html",{"form":form,"id":tid})
        # classlist = models.Classes.objects.all().only("id", "name")
        # courselist = models.Course.objects.all().only("id", "name")
        # utlist = models.UserType.objects.all().only("id", "name")
        # sel_classlist=[]
        # sel_courselist=[]
        # edit_teacher_class_obj=teacher_obj.class_list.all().values("id")
        # edit_course_class_obj=teacher_obj.course_list.all().values("id")
        # for obj in edit_teacher_class_obj:
        #     sel_classlist.append(obj.get("id"))
        # for obj in edit_course_class_obj:
        #     sel_courselist.append(obj.get("id"))
        # return render(request,"teacheredit.html"
        #               ,{"sel_classlist":sel_classlist,
        #                 "sel_courselist":sel_courselist,
        #                 "teacher_obj":teacher_obj,
        #                 "classlist":classlist,
        #                 "courselist":courselist,
        #                 "utlist":utlist})

    return HttpResponse("你有误操作，页面不存在!")

def testh(request):
    return render(request,"studentedit.html")

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

def log_out(request):
    del request.session["username"]
    return redirect("/login/")

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

