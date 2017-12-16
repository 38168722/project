from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def collectInfo(request):
    print(request.POST)
    return HttpResponse("收到了")