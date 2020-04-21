from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # 首页
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 数据库列表
    url(r'^databases/$', views.DatabaseView.as_view(), name='databases'),
    # 更新用户数据库标题
    url(r'^databases/(?P<database_id>\d+)/title/$', views.UpdateTitleDatabaseView.as_view()),
    # 备份页面
    url(r'^backup/$', views.BackupView.as_view(), name='backup'),
    # 增量备份页面
    url(r'^incre/$', views.IncreView.as_view(), name='incre'),
    # 更新和删除用户数据库
    url(r'^databases/(?P<database_id>\d+)/$', views.UpdateDestroyDatabaseView.as_view()),
    # 新增用户地址
    url(r'^databases/create/$', views.DatabaseCreateView.as_view()),
    # 查询用户数据库
    url(r'^userdatabases/$', views.UserDatabaseView.as_view()),
    # 查询用户备份
    url(r'^userbackups/$', views.UserFileView.as_view()),
]
