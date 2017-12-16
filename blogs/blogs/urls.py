"""blogs URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.views.static import serve
from blogs import settings
#滑动模块验证码要导入的包
from app01.views import pcgetcaptcha
# from app01.views import pcvalidate
from app01.views import pcajax_validate
from app01.views import mobileajax_validate
from app01.views import home



urlpatterns = [
    url(r'^comment/$', views.sub_comment),
    # 文章点赞
    url(r'^poll/$', views.poll),
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^uploadFile/', views.uploadFile),

    url(r'^getvalicode/', views.getvalicode),
    # 文章分类配置
    url(r'^cate/(?P<site_article_category>.*)/$', views.index),
    # media 配置
    url(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
    #个人站点首页
    url(r'^blog/',include("app01.urls")),
    url(r'^test01/', views.test01),
    #滑动模块验证码URL
    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),
    url(r'/*', home, name='home'),
]
