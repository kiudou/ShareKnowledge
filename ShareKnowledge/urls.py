#coding: utf-8
"""ShareKnowledge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from books import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'), #主页

    path('upload/', views.upload, name='upload'), #上传

    path('submit_form/', views.submit_form, name='submit_form'), #提交表单

    # path('uploadFile/', views.upload_file, name='uploadFile'), #查找标签



    path('upload/part/', views.upload_part, name='upload_part'), #分片

    path('upload/success/', views.upload_success, name='upload_success'), #上传成功
    



    path('search_title/', views.search_title, name='search_title'), #查找书名

    path('search_tag/', views.search_tag, name='search_tag'), #查找标签

    path('book/<str:book_title>/', views.title, name='book_title'), #书籍的展示

    path('<str:book_tag>/', views.tags, name='tags'), #该类标签的书籍展示






]
