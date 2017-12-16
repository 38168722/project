from django.shortcuts import render,HttpResponse
from app01 import models
# Create your views here.
def index(request):
    obj=models.Comment.objects.filter(id=1).delete()

    return HttpResponse("hello world")
