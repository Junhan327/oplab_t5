from django.shortcuts import render,HttpResponse
from app_forum import models
# Create your views here.
def login(request):
    return render(request,"login.html")

def test(request):
    models.user_info.objects.create(name='test',password='123')
    return HttpResponse("连接成功")