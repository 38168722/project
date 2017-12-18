from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from app01 import models


def infolist(request):
    userlist = models.UserInfo.objects.all()
    return render(request,"userlist.html",{"userlist":userlist})