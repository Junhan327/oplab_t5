"""
URL configuration for hs_forum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from app_forum import views
urlpatterns = [
    path('test/', views.test),
    path('t/', views.t),
    path('login/', views.login),
    path('register/', views.register),
    path('user/', views.user),
    path('user/logout/', views.logout),
    path('sentcode/', views.sentcode),
    path('login_e/', views.login_e),
    path('showdate/', views.showdate),
    path('user/write', views.write),
    path('user/show_article/<int:article_id>/', views.show_article),
    path('user/profile/', views.profile),
    path('user/update_article/<int:article_id>/', views.update),
    path('user/delete_article/<int:article_id>/', views.delete),
    path('user/delete_col/<int:article_id>/', views.delete_col),
    path('collect/', views.collect), # 用于创建收藏关系
    path('like/',views.like),
    

    # path('user/article', views.aricle),
]
