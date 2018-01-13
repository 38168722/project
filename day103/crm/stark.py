#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from stark.service import v1
from crm import models

class DepartmentConfig(v1.StarkConfig):
    list_display=["title","code"]

    def get_list_display(self):
        result=[]
        result.append(v1.StarkConfig.checkbox)
        result.extend(self.list_display)
        # result.append(self.edit)
        # result.append(v1.StarkConfig.edit)
        result.append(v1.StarkConfig.delete)
        return result

    edit_link = ['title']

v1.site.register(models.Department,DepartmentConfig)

class UserInfoConfig(v1.StarkConfig):
    list_display=["name","username","email","depart"]

    comb_filter = [
        v1.FilterOption("depart",text_func_name=lambda x:str(x),val_func_name=lambda x:x.code,)
    ]
    edit_link = ["name"]
    search_fields = ["name__contains","email__contains","username__contains"]
    show_search_form = True

v1.site.register(models.UserInfo,UserInfoConfig)

class CourseConfig(v1.StarkConfig):
    list_display = ["name"]
    edit_link = ["name"]

v1.site.register(models.Course,CourseConfig)

class CustomerConfig(v1.StarkConfig):

    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=False):
        if is_header:
            return "学历"
        return obj.get_education_display()

    def display_status(self,obj=None,is_header=False):
        if is_header:
            return "状态"
        return obj.get_status_display()

    def display_course(self,obj=None,is_header=False):
        if is_header:
            return "咨询课程"
        course_list=obj.course.all()
        html=[]
        #self.request.GET
        #self._query_parm_key
        #构造QueryDict
        #urlencode

        for item in course_list:
            temp="<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px' href='/stark/crm/customer/%s/%s/dc/'>%s X</a>"%(obj.pk,item.pk,item.name)
            html.append(temp)
        return mark_safe("".join(html))

    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param customer_id:
        :param course_id:
        :return:
        """
        customer_obj=self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        #跳转回去时，要保留原来的搜索条件
        return redirect(self.get_list_url())

    def record(self,obj=None,is_header=False):
        if is_header:
            return "跟进记录"
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>"%(obj.pk,))

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        patterns=[
            url(r'^(\d+)/(\d+)/dc/$',self.wrap(self.delete_course),name='%s_%s_dc'%app_model_name)
        ]
        return patterns


    list_display = ["qq","name",display_gender,display_education,display_course,display_status,record]
    edit_link = ["qq","name"]

v1.site.register(models.Customer,CustomerConfig)

class SchoolConfig(v1.StarkConfig):
    list_display = ["title"]
    edit_link = ["title"]

v1.site.register(models.School,SchoolConfig)

class ClassListConfig(v1.StarkConfig):

    def course_semester(self,obj=None,is_header=False):
        if is_header:
            return "班级"
        return "%s(%s期)"%(obj.course.name,obj.semester,)

    def num(self,obj=None,is_header=False):
        if is_header:
            return "人数"
        #obj是班级对象
        #学生和班级的关系 M2M
        #作业列举班级人数
        return 666
    list_display = ["school",course_semester,num,"start_date"]
    edit_link = [course_semester]

    #组合搜索

v1.site.register(models.ClassList,ClassListConfig)

class ConsultRecordConfig(v1.StarkConfig):
    list_display = ['customer','consultant','date']

    comb_filter = [
        v1.FilterOption('customer')
    ]

    def changelist_view(self,request,*args,**kwargs):
        customer=request.GET.get("customer")
        #session中获取当前用户ID
        current_login_user_id=1
        ct=models.Customer.objects.filter(consultant=current_login_user_id,id=customer).count()
        if not ct:
            return HttpResponse("别抢客户呀!")

        return super(ConsultRecordConfig,self).changelist_view(request,*args,**kwargs)

v1.site.register(models.ConsultRecord,ConsultRecordConfig)

class CourseRecordConfig(v1.StarkConfig):
    list_display = ['class_obj','day_num']

    def multi_init(self,request):
        """
        自定义执行批量初始化方法
        :param request:
        :return:
        """
        #上课记录的ID列表
        pk_list = request.POST.getlist("pk")
        #上课记录对象
        record_list=models.CourseRecord.objects.filter(id__in=pk_list)
        for record in record_list:
            #day1,day2,day3
            #record.class_obj #关联的班级
            student_list=models.Student.objects.filter(class_list=record.class_obj)
            print(record,student_list)
            bulk_list=[]
            for student in student_list:
                #为每一个学生创建dayn的学习记录
                # models.StudyRecord.objects.create(student=student,course_record=record)
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)


    multi_init.short_desc="学生的初始化"

    actions = [multi_init,]
    show_actions = True

v1.site.register(models.CourseRecord,CourseRecordConfig)

class StudentConfig(v1.StarkConfig):
    list_display = ["username","emergency_contract"]

v1.site.register(models.Student,StudentConfig)