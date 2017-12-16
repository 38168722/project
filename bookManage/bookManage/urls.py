"""bookManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pj01 import views

urlpatterns = [
    url(r'^root/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^delbook/', views.delbook),
    url(r'^admin/', views.admin),
    url(r'^edit/', views.edit),
    url(r'^addbook/', views.addbook),
    url(r'^authors/', views.authors),
    url(r'^authlist/', views.authlist),
    url(r'^addauth/', views.addauth),
    url(r'^addauthlist/', views.addauthlist),
    url(r'^editauth/', views.editauth),
    url(r'^editpublish/', views.editpublish),
    url(r'^publishlist/', views.publishlist),
    url(r'^addpublish/', views.addpublish),
    url(r'^publish/', views.publish),
    url(r'^delauth/', views.delauth),
    url(r'^delpublish/', views.delpub),
    url(r'^systemuser/', views.systemuser),
    url(r'^adduser/', views.adduser),
    url(r'^delsystemuser/', views.delsystemuser),
    url(r'^edituser/', views.edituser),
    # url(r'^test/', views.hello),
    url(r'^ceshi/', views.ceshi),
    url(r'^log_out/', views.log_out),
    url(r'^register/', views.register),
    url(r'^changepwd/', views.changepwd),
]
