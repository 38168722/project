from django.contrib import admin
from app01 import models
from django.utils.safestring import mark_safe
# Register your models here.
class employeeConfig(admin.ModelAdmin):
    list_display = ["username","email","xxxx","more","did"]
    list_display_links = ['email']
    list_filter = ['username','email']
    list_editable = ['username']
    search_fields = ['username']
    def func(self,request,queryset):
        print(self,request,queryset)
        print(request.POST.getlist('_selected_action'))

    func.short_description = "中文显示自定义Actions"
    actions = [func,]
    # change_list_template = "myuserinfo.html"

    def xxxx(self,obj):
        return obj.username+"最美"

    def more(self,obj):
        return mark_safe("<a href='http://www.xiaohua100.com'>点击查看写真</a>")

admin.site.register(models.Employee,employeeConfig)

class employeeInline(admin.StackedInline):
    extra = 0
    model = models.Employee

class DepartmentConfig(admin.ModelAdmin):
    list_display = ["id","dname"]
    inlines = [employeeInline,]

admin.site.register(models.Department,DepartmentConfig)

