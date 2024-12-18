from django.shortcuts import render,HttpResponse,redirect
from app_forum import models
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.cache import cache
from django.views.decorators.cache import cache_page
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
            print("correctcode")
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


# 以这种方式能大大减少加载时间 ,但是出现问题，
# 由于页面是预加载的，所以似乎并不能正确获取cookie，用户名称会显示错误
# 并且这样子就让登录失去了意义
# 我暂时还不知道怎么解决这个问题
@cache_page(300)
def user(request):
    # cookie 需要登录才能访问的页面需要这个
    if request.method == "GET":


        # 压测暂时关掉登录
        info = request.session.get("info")
        print(info)
        if not info:
            return redirect('/login/')
        #info = "压测"


        #显示所有文章
        ##quertinfo = models.article.objects.all()

        ##显示分页后的文章
        page = int(request.GET.get('page',1))

        #pagec = str(request.GET.get('page',1))
        #key_page = 'quertinfo'+pagec # 设置键对名称

        numofpage = 200
        start = (page-1)* numofpage
        end = page * numofpage

        #cacheq = cache.get(key_page)
        #print(cacheq)
        #cnum = cache.get('num')
        #print(cnum)
        #if cacheq is not None:
        #    print("use cache")
        #    pagenum = int((cnum/numofpage)+1)
        #    pages = list(range(1, pagenum))
        #    return render(request,"user.html",{"username":info ,"qinfo":cacheq,"pages":pages})
        quertinfo = models.article.objects.all()[start:end]
        num = models.article.objects.all().count()
        #cache.set(key_page,quertinfo,timeout=300)
        #cache.set('num',num)
        pagenum = int((num/numofpage)+1)
        pages = list(range(1, pagenum))
        return render(request,"user.html",{"username":info ,"qinfo":quertinfo,"pages":pages})
    #检索
    info = request.session.get("info")
    if not info:
        return redirect('/login/')
    search = request.POST.get("searchdata")
    page = int(request.GET.get('page',1))
    numofpage = 200
    start = (page-1)* numofpage
    end = page * numofpage
    result = models.article.objects.filter(content__contains=search)[start:end]
    num = models.article.objects.filter(content__contains=search).count()
    pagenum = int((num/numofpage)+1)
    pages = list(range(1, pagenum))
    if result:
        return render(request,"user.html",{"username":info ,"qinfo":result,"pages":pages})
    else:
        return HttpResponse("什么也没有搜索到")


def test(request):
    return render(request,"test.html")

def showdate(request): #测试是否正常显示系统时间
    now = datetime.datetime.now()
    today_time = datetime.datetime.strptime(now, '%Y-%m-%d')
    print(today_time)
    return HttpResponse("连接成功")

def write(request):
    if request.method =="GET":
        info = request.session.get("info") # 查找cookie和用户信息
        return render(request,"write.html",{"username":info})
    title = request.POST.get("title")
    content = request.POST.get("body")
    tags = request.POST.get("tags")
    who = request.session.get("info")
    a = models.user_info.objects.filter(name = who).first()
    author = a
    models.article.objects.create(title=title,content=content,tags=tags,likes = 0,author = author)
    return redirect("/user/") 

def show_article(request,article_id): 
    if request.method =="GET":
        info = request.session.get("info") # 查找cookie和用户信息
        aid =  models.article.objects.get(id = article_id)
        comment =  models.Comment.objects.filter(comment_article = aid)
        return render(request,"show_article.html",{"aid":aid,"username":info,"comment":comment})
    info = request.session.get("info")
    uinfo = models.user_info.objects.get(name = info)
    aid =  models.article.objects.get(id = article_id)
    commentbody = request.POST.get("commentbody")
    models.Comment.objects.create(comment_article = aid,comment_content = commentbody,comment_author = uinfo)
    comment =  models.Comment.objects.filter(comment_article = aid)
    return render(request,"show_article.html",{"aid":aid,"username":info,"comment":comment})

def profile(request): 
    if request.method =="GET":
        info = request.session.get("info") # 查找cookie和用户信息
        if not info:
            return redirect('/login/')
        uinfo = models.user_info.objects.get(name = info)

        
        page = int(request.GET.get('page',1))
        numofpage = 20
        start = (page-1)* numofpage
        end = page * numofpage
        ua = models.article.objects.filter(author = uinfo)[start:end]
        ca = models.collection.objects.filter(user = uinfo).select_related("article")
        num = models.article.objects.all().count()
        pagenum = int((num/numofpage)+1)
        pages = list(range(1, pagenum))
        #获取点赞数量,收藏数量
        likes = models.article.objects.filter(author = uinfo)
        ulikes = 0
        ucollections = 0
        for i in likes:
            ulikes += i.likes
            ucollections += i.collections
        uimg = models.img.objects.filter(user = uinfo).first()
        if uimg:
            userimg = uimg.theimg
            return render(request,"profile.html",{"username":info,"uinfo":uinfo,"ua":ua,"ca":ca,"pages":pages,"ulikes":ulikes,'ucollections':ucollections,"userimg":userimg})
        return render(request,"profile.html",{"username":info,"uinfo":uinfo,"ua":ua,"ca":ca,"pages":pages,"ulikes":ulikes,'ucollections':ucollections})
    print(request.FILES)
    info = request.session.get("info")
    uinfo = models.user_info.objects.get(name = info)
    file = request.FILES.get("myfile")
    #filename = str(uinfo.id)
    #f = open("/media/" + filename + ".png", mode='wb')
    #for chunk in file.chunks():
    #    f.write(chunk)
    #f.close
    models.img.objects.create(theimg = file, user = uinfo)
    return redirect("/user/profile/")

def update(request,article_id): 
    if request.method =="GET":
        info = request.session.get("info") # 查找cookie和用户信息
        uinfo = models.user_info.objects.get(name = info)
        ainfo = models.article.objects.get(id = article_id)
        ua = models.article.objects.filter(author = uinfo)
        return render(request,"update.html",{"username":info,"uinfo":uinfo,"ua":ua,"ainfo":ainfo})
    title = request.POST.get("title")
    content = request.POST.get("body")
    tags = request.POST.get("tags")
    who = request.session.get("info")
    a = models.user_info.objects.filter(name = who).first()
    models.article.objects.filter(id = article_id).update(title=title,content=content,tags=tags)
    return redirect("/user/profile/")

def delete(request,article_id): 
    if request.method =="GET":
        models.article.objects.filter(id = article_id).delete()
        return redirect("/user/profile/")

@csrf_exempt
def collect(request):
    aid = request.POST.get("article_id")
    info = request.session.get("info")
    aqueryset = models.article.objects.filter(id = aid).first()
    uqueryset = models.user_info.objects.filter(name = info).first()
    models.collection.objects.create(user = uqueryset , article = aqueryset)
    a = models.article.objects.filter(id = aid).first()
    acollect = a.collections + 1
    models.article.objects.filter(id = aid).update(collections = acollect)
    return HttpResponse("收藏成功")

@csrf_exempt
def like(request):
    aid = request.POST.get("article_id")
    a = models.article.objects.filter(id = aid).first()
    new_likes = a.likes + 1
    models.article.objects.filter(id = aid).update(likes = new_likes)
    return HttpResponse("点赞成功")

def delete_col(request,article_id): 
    if request.method =="GET":
        ainfo = models.article.objects.get(id = article_id)
        models.collection.objects.filter(article = ainfo).delete()
        return redirect("/user/profile/")
    

def t(request): 
    if request.method =="GET":
        models.user_info.objects.create(name="test" ,password = "test123" ,email ="test@qq.com")
        return HttpResponse("succ")
