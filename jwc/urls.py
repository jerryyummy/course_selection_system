"""jwc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from myWEB import views

urlpatterns = [
    path('', views.home),  # 首页
    path('admin/', admin.site.urls),  # admin

    path('login_view/', views.login_view),  # 填写完信息后提交登陆验证
    path('logout_view/', views.logout_view),  # 退出登陆

    path('index/', views.index),  # 教务系统首页
    path('index/info/', views.show_info),  # 个人信息展示
    path('index/select_course/', views.select_course),  # 学生选课
    path('index/drop_course/', views.drop_course),  # 学生退课
    path('index/query_score/', views.query_score),  # 学生成绩查询
    path('index/query_course/', views.query_course),  # 学生课程查询

    path('index/setup_course/', views.setup_course),  # 教师开课
    path('index/cancel_course/', views.cancel_course),  # 教师取消开课
    path('index/publish_score/', views.publish_score),  # 教师发布成绩
]
