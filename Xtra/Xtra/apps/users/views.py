from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
from django.urls import reverse

from django.contrib.auth import login, authenticate, logout
from django.db import DatabaseError
from django_redis import get_redis_connection
from users.models import User
from Xtra.utils.response_code import RETCODE


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        allow = request.POST.get('allow')

        # 校验参数: 前后端的校验需要分开，避免恶意用户越过前端逻辑发送请求，要保证后端安全，前后端的校验逻辑相同
        # 判断参数是否齐全
        # all([列表]):会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, allow]):
            # return '如果缺少必传参数，响应错误提示信息，403'
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个字符
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次输入的密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')

        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 测试展示错误提示信息
        # return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 保存注册数据：是注册业务的核心
        try:
            user = User.objects.create_user(username=username, password=password)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': 'registration failed'})
        # 实现状态保持
        login(request, user)

        # 响应结果：重定向到首页
        response = redirect(reverse('contents:index'))

        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'value', 'expiry')
        response.set_cookie('username', user.username, max_age=3600)
        # 响应结果: 重定向到首页
        return response


class LoginView(View):
    """用户登陆"""

    def get(self, request):
        """提供用户登陆页面"""
        return render(request, 'login.html')

    def post(self, request):
        """实现用户登陆逻辑"""
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数
        if not all([username, password]):
            return http.HttpResponseForbidden('Missing required parameter')

        # 校验用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('Please enter the correct username or mobile phone number')

        # 检验密码
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('Password must be at least 8 digits and maximum 20 digits')
        # 认证用户：使用账号查询用户是否存在，如果用户存在，再检验密码是否正确
        # user = User.objects.get(username=username)
        # user.check_password()
        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': 'Incorrect username or password'})
        # 状态保持
        login(request, user)
        if remembered != 'on':
            # 没有记住登陆： 状态保持在浏览器会话结束后就销毁
            request.session.set_expiry(0)   # 单位是秒
        else:
            # 记住登陆：状态保持周期为两周(默认是两周)
            request.session.set_expiry(3600)

        # 响应结果
        # 先取出next
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            response = redirect(reverse('contents:index'))

        # 为了实现在首页的右上角展示用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'value', 'expiry')
        response.set_cookie('username', user.username, max_age=3600)

        # 响应结果: 重定向到首页
        return response


class LogoutView(View):
    """用户退出登陆"""
    def get(self, request):
        """实现用户退出登陆的逻辑"""
        # 清除状态保持信息
        logout(request)

        # 退出登陆后重定向到首页
        response = redirect(reverse('contents:index'))

        # 删除cookie中的用户名
        response.delete_cookie('username')

        # 响应结果
        return response