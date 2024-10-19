通过django-admin startproject [projectName]来新建项目
## 有关文件
manage.py用于项目管理，启动项目，创建app，数据管理
settings.py用于项目的配置
urls.py用于URL和函数之间的对应关系
asgi.py用于接收网络请求
wsgi.py用于接收网络请求
## 有关APP
不同的应用，一个项目可以拆分成很多功能，每个功能用一个app来编写，实现
不同app之间有独立的函数，html，表结构。互不影响
多个app共同组建出大的项目
* 利用manage.py来创建app:python manage.py startapp [appName]
# app文件下的文件
views.py 用来定义函数
models.py 用来对数据库操作
在settings.py中的installed_apps中注册app
在urls.py中编写URL与函数对应关系
## 启动django项目
* python manage.py runserver [ip：port]
* port 默认8000
## 建立templates文件夹。存放html文件。django默认会在这个文件夹下寻找
*  return render(request,"name.html")
## 最好建立一个static文件夹来存放静态文件：img，css,js,plugins等
## django模板语法
* 后端可以通过render里传给前端数据，例如temp1 = "114514";render(request,"name.html",{"temp2":temp}) 这样子前端就能用{{temp2}}获取该数据
* 若通过索引就是temp2.0 .1 .2 .3 ·····
* 本质上是再html中写一些占位符，由数据对这些占位符进行替换和处理
* 这样做会先读取html文件，然后再django中对特定的内容进行渲染替换，最终返回纯正的html文件
## 关于请求和响应
* request 是一个对象，封装了用户发过来的全部请求相关数据
* request.method获取用户请求方式(get/post)
* 进入网址，会发一个get请求
* request.GET会获取传输的数据
* request.POST在请求体中提交数据
## 关于连接数据库
* import pymysql
* conn = pymysql.connect(host,port,user,password,database··········)
* 这里可以通过pymysql发送sql语句到数据库，也可以利用Django的ORM框架来发送
* ORM框架实际上也会把语句先解析成类似pymysql，再发送到数据库，相当于一个翻译的过程，方便了对数据库的操作
* 可以用第三方模块pymysqlclient
# 关于ORM
* ORM可以创建，修改，删除数据库中的表并操作表中的数据，但是不能创建数据库，所以需要先用mysql自带的工具创建好对应的数据库
# django连接数据库
* 在settings.py中的DATABASES中添加要连接的数据库
# django操作表
* 创建表。在models.py中写一个类，继承models.Model。表的名字就是app名_类名
* 执行 python manage.py makemigrations 和 python manage.py migrate   (app需要先注册，才能把表提交到数据库)
* 类名.objects.create(对应的列名)来添加数据
* 类名.objects.filter(条件).delete(```)
* 类名.objects.filter(条件).update(```)
* data_list = 类名.objects.all()  这里的data_list是QuerySet类型，返回表
* gender_choices可以用来做约束
