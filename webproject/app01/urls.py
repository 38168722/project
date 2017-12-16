#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from app01 import views
urlpatterns = [
    url(r'^login', views.login,name="pattern"),
    url(r'^register$', views.register),
    url(r'^article/', views.article),
    # url(r'^(?P<n1>\d+)/(?P<n2>\d+)', views.news)
    url(r'^db_handel', views.db_handel),
    url(r'^home', views.home),
    url(r'^book', views.book),
    # url(r'^base', views.base),
    url(r'^index/', views.index),
    url(r'^ajax/', views.ajax_test),
]
