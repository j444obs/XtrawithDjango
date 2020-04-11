from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # 首页
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 备份页面
    url(r'^backup/$', views.BackupView.as_view(), name='backup'),
    # 增量备份页面
    url(r'^incre/$', views.IncreView.as_view(), name='incre'),
]
