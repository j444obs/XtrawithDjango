from django.utils import timezone

from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
import re
import subprocess

from contents.models import BackupInfo
from users.models import User

# Create your views here.


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        """
        展示首页
        :param request:
        :return:
        """
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        backups = BackupInfo.objects.filter(user=user)
        backup_list = []
        for backup in backups:
            backup_list.append(backup)
        # 构造上下文
        context = {
            'backups': backup_list,
        }

        return render(request, "index.html", context)


class BackupView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, "backup.html")

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        HostIP = request.POST.get('HostIP')
        dbuser = request.POST.get('username')
        password = request.POST.get('password')
        port = request.POST.get('port')
        allow = request.POST.get('allow')

        # 校验参数: 前后端的校验需要分开，避免恶意用户越过前端逻辑发送请求，要保证后端安全，前后端的校验逻辑相同
        # 判断参数是否齐全
        # all([列表]):会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([HostIP, dbuser, password, port, allow]):
            # return '如果缺少必传参数，响应错误提示信息，403'
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断IP
        if not re.match(r'^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$', HostIP):
            return http.HttpResponseForbidden('Please enter the correct IP')
        # 判断DB user
        if dbuser == "":
            return http.HttpResponseForbidden('please enter DB username')
        # 判断DB password
        if password == "":
            return http.HttpResponseForbidden('please enter DB password')

        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('please tick the agreement')

        command = "/usr/bin/innobackupex --user=" + dbuser \
                  + " --password=" + password\
                  + " --host=" + HostIP\
                  + " --port=" + port\
                  + " /tmp/xtra_test/"
        command1 = 'ls -t /tmp/xtra_test/|head -n1'
        (retcode1, res1) = subprocess.getstatusoutput(command1)
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        try:
            (retcode, res) = subprocess.getstatusoutput(command)
            backup = BackupInfo.objects.create(order_id=order_id,
                                               user=user,
                                               host_ip=HostIP,
                                               dbuser=dbuser,
                                               dbport=port,
                                               dbpassword=password,
                                               status=retcode,
                                               filename=res1)

            # backup.save()
        except DatabaseError as e:
            print(e)
            return render(request, 'backup.html', {'backup_errmsg': 'backup record failed'})

        if retcode != 0:
            return render(request, 'backup.html', {'backup_errmsg': 'backup failed'})

        # 响应结果：重定向到首页
        response = redirect(reverse('contents:index'))

        return response


class IncreView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, "Incre.html")

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        HostIP = request.POST.get('HostIP')
        dbuser = request.POST.get('username')
        password = request.POST.get('password')
        port = request.POST.get('port')
        allow = request.POST.get('allow')
        filename = request.POST.get('filename')

        # 校验参数: 前后端的校验需要分开，避免恶意用户越过前端逻辑发送请求，要保证后端安全，前后端的校验逻辑相同
        # 判断参数是否齐全
        # all([列表]):会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([HostIP, dbuser, password, port, allow, filename]):
            # return '如果缺少必传参数，响应错误提示信息，403'
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断IP
        if not re.match(r'^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$', HostIP):
            return http.HttpResponseForbidden('Please enter the correct IP')
        # 判断DB user
        if dbuser == "":
            return http.HttpResponseForbidden('please enter DB username')
        # 判断DB password
        if password == "":
            return http.HttpResponseForbidden('please enter DB password')

        # 判断增量原始文件
        if not re.match(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', filename):
            return http.HttpResponseForbidden('Please enter the correct Filename')

        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('please tick the agreement')

        command = "/usr/bin/innobackupex --user=" + dbuser \
                  + " --password=" + password \
                  + " --host=" + HostIP \
                  + " --port=" + port \
                  + " --incremental /tmp/xtra_test/" \
                  + " --incremental-basedir=/tmp/xtra_test/" \
                  + filename + "/"
        command1 = 'ls -t /tmp/xtra_test/|head -n1'
        (retcode1, res1) = subprocess.getstatusoutput(command1)
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        try:
            (retcode, res) = subprocess.getstatusoutput(command)
            backup = BackupInfo.objects.create(order_id=order_id,
                                               user=user,
                                               host_ip=HostIP,
                                               dbuser=dbuser,
                                               dbport=port,
                                               dbpassword=password,
                                               status=retcode,
                                               filename=res1)

            # backup.save()
        except DatabaseError as e:
            print(e)
            return render(request, 'Incre.html', {'backup_errmsg': 'Incre backup record failed'})

        if retcode != 0:
            return render(request, 'Incre.html', {'backup_errmsg': 'Incre backup failed'})

        # 响应结果：重定向到首页
        response = redirect(reverse('contents:index'))

        return response