from django.shortcuts import render,HttpResponse,redirect
from app_forum import models
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random,datetime
# Create your views here.
def login(request):
    if request.method =="GET":
        return render(request,"login.html")
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    ifexist = models.user_info.objects.filter(name = username,password = password).exists()
    if ifexist:
        # 生成cookie，存放到session
        request.session["info"] = username
        return redirect("/user/")
    else:
        return render(request,'login_error.html',{"error":"账号或密码错误"})

def login_e(request):
    if request.method =="GET":
        return render(request,"login_e.html")
    email = request.POST.get('mail')
    code= request.POST.get('code')
    neededcode = request.session.get('random_code')
    emailexist = models.user_info.objects.filter(email=email).exists()
    if emailexist:
        if code == neededcode:
            print("here")
            uinfo = models.user_info.objects.filter(email = email).first()
            name=uinfo.name
            request.session["info"] = name
            return redirect("/user/")
        else:
            return render(request,'login_error.html',{"error":"验证码错误"})
    else:
        return render(request,'login_error.html',{"error":"邮箱没有注册"})

def logout(request):
    request.session.clear()
    return redirect("/login/")
    
def register(request):
    if request.method =="GET":
        return render(request,"register.html")
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('mail')
    code= request.POST.get('code')
    neededcode = request.session.get('random_code')
    if code==neededcode:
        email_exists = models.user_info.objects.filter(email=email).exists()
        if email_exists:
            return render(request,'register_error.html',{"error":"邮箱已被注册"})
        else:
            username_exists = models.user_info.objects.filter(name=username).exists()
            if username_exists:
                return render(request,'register_error.html',{"error":"用户名已被注册"})
            else:
                models.user_info.objects.create(name=username,password=password,email=email)
                return render(request,'success_register.html')
    else:
        return render(request,'register_error.html',{"error":"验证码错误"})
            

@csrf_exempt
def sentcode(request):
    mail = request.POST.get("email")
    random_code = ''.join([str(random.randint(1, 9)) for _ in range(6)])
    print(random_code)
    request.session['random_code'] = random_code
    # 这时候用户没有登录，所以可能不会影响到session中存放的cookie信息
    request.session.set_expiry(60)
    send_mail(subject="HAPPYSHEEP论坛验证码",message="你的验证码是"+random_code,from_email="1919376677@qq.com",recipient_list=[mail])
    return HttpResponse("发送成功")

def user(request):
    # cookie 需要登录才能访问的页面需要这个

    info = request.session.get("info")

    if not info:
        return redirect('/login/')
    
    #显示所有文章
    quertinfo = models.article.objects.all()
    return render(request,"user.html",{"username":info ,"qinfo":quertinfo})

def test(request):
    models.user_info.objects.create(name='test',password='123')
    return HttpResponse("连接成功")

def showdate(request):
    now = datetime.datetime.now()
    today_time = datetime.datetime.strptime(now, '%Y-%m-%d')
    print(today_time)
    return HttpResponse("连接成功")

def write(request):
    if request.method =="GET":
        return render(request,"write.html")
    
    title = request.POST.get("title")
    content = request.POST.get("body")
    tags = request.POST.get("tags")
    who = request.session.get("info")
    a = models.user_info.objects.filter(name = who).first()
    author = a
    models.article.objects.create(title=title,content=content,tags=tags,likes = 0,author = author)
    return HttpResponse("success")
    

