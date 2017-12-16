from django.conf.urls import url,include
from blogs import settings
from app01 import views
urlpatterns = [
    url(r'^(?P<username>.*)/articles/(?P<article_id>\d+)',views.homeSite),
    url(r'^.*/manager/',views.manager),
    url(r'^(?P<username>.*)/(?P<condition>tag|category|date)/(?P<para>.*)', views.homeSite),
    url(r'^(?P<username>.*)', views.homeSite,name="userhome"),

]
