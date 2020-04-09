from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    # 图形验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    # 校验图形验证码
    url(r'^check_image_codes/(?P<mobile>1[3-9]\d{9})/$', views.CheckImageCodeView.as_view()),
]
