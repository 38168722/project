"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^article/',views.article),
    # url(r'^son', views.son),
    # url(r'^book', views.book),
    # url(r'^base/(\d+)', views.base),
    url(r'^index', views.index),
    # # url(r'^del/(\d+)', views.delitem),
    # url(r'^del/', views.delitem),
    # url(r'^update/', views.upda),
    # url(r'^addbook/', views.addbook),
    # url(r'^query', views.query),
    url(r'^index/',views.index),
    url(r'^ajax/',views.ajax_test),
    url(r'^booklist/',views.booklist),
    url(r'^upload_file/',views.upload_file),
    # url(r'^login',views.login),
    # url(r'^register', views.register),
    # url(r'^article/(\d{4})/(\d{2})$', views.article),
    # url(r'^printinfo/(\d{4})/(\d{2})$', views.printinfo)
    # url(r'^app01/', include('app01.urls'))
]

# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)