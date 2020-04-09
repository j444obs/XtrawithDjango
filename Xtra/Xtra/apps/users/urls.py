from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count$', views.UsernameCountView.as_view()),
    # 用户登陆
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户退出
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
