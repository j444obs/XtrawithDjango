from django.utils import timezone

from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
import re, json, logging
import subprocess

from contents.models import BackupInfo, DatabaseInfo
from users.models import User
from Xtra.utils.views import LoginRequiredJSONMixin
from Xtra.utils.response_code import RETCODE
from contents import constants

# Create your views here.


# 创建日志输出器
logger = logging.getLogger('django')


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


class DatabaseView(LoginRequiredMixin, View):
    """用户数据库"""

    def get(self, request):
        """查询并展示用户数据库信息"""

        # 获取当前登陆用户对象
        login_user = request.user
        # 使用当前登陆用户和is_deleted=False作为条件查询地址数据
        databaseinfos = DatabaseInfo.objects.filter(user=login_user, is_deleted=False)

        # 将用户数据库模型列表转字典列表：因为Vue.js不认识模型列表，只有Django和Jinja2模板引擎认识
        database_list = []
        for databaseinfo in databaseinfos:
            database_dict = {
                "id": databaseinfo.id,
                "title": databaseinfo.title,
                'host_ip': databaseinfo.host_ip,
                'dbuser': databaseinfo.dbuser,
                'dbpassword': databaseinfo.dbpassword,
                'dbport': databaseinfo.dbport
            }
            database_list.append(database_dict)

        # 构造上下文
        context = {

            'userdatabases': database_list,
        }

        return render(request, 'user_center_site.html', context)


class UpdateTitleDatabaseView(LoginRequiredJSONMixin, View):
    """更新地址标题"""

    def put(self, request, database_id):
        """实现更新地址标题逻辑"""
        # 接收参数：title
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        # 校验参数
        if not title:
            return http.HttpResponseForbidden('缺少title')

        try:
            # 查询当前要更新标题的地址信息
            databaseinfo = DatabaseInfo.objects.get(id=database_id)
            # 将新的地址标题覆盖地址标题
            databaseinfo.title = title
            databaseinfo.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新标题失败'})
            # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新标题成功'})


class UpdateDestroyDatabaseView(LoginRequiredJSONMixin, View):
    """更新和删除用户数据库"""

    def put(self, request, database_id):
        """修改用户数据库"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        host_ip = json_dict.get('host_ip')
        dbuser = json_dict.get('dbuser')
        dbpassword = json_dict.get('dbpassword')
        dbport = json_dict.get('dbport')


        # 校验参数
        if not all([host_ip, dbuser, dbpassword, dbport]):
            return http.HttpResponseForbidden('缺少必传参数')
        # if not re.match(r'^1[3-9]\d{9}$', mobile):
        #     return http.HttpResponseForbidden('参数mobile有误')

        # 使用最新的用户数据库信息覆盖旧信息
        try:
            DatabaseInfo.objects.filter(id=database_id).update(
                user=request.user,
                host_ip=host_ip,
                dbuser=dbuser,
                dbpassword=dbpassword,
                dbport=dbport,
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改用户数据库失败'})

        # 响应新的地址信息给前端渲染
        databaseinfo = DatabaseInfo.objects.get(id=database_id)
        database_dict = {
            "id": databaseinfo.id,
            "title": databaseinfo.title,
            "host_ip": databaseinfo.host_ip,
            "dbuser": databaseinfo.dbuser,
            "dbpassword": databaseinfo.dbpassword,
            "dbport": databaseinfo.dbport,
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改数据库成功', 'database': database_dict})

    def delete(self, request, database_id):
        """删除用户数据库"""
        # 实现指定地址的逻辑删除：is_delete=True
        try:
            databaseinfo = DatabaseInfo.objects.get(id=database_id)
            databaseinfo.is_deleted = True
            databaseinfo.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除用户数据库失败'})
        # 响应结果：code, errmsg
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除用户数据库成功'})


class DatabaseCreateView(LoginRequiredJSONMixin, View):
    """新增用户数据库"""

    def post(self, request):
        """实现新增用户数据库逻辑"""

        # 判断用户数据库数量是否超过上限：查询当前登陆用户的用户数据库数量
        # count = Address.objects.filter(user=request.user).count()
        # 语法1： 一对应的模型类对象.多对应的模型类名小写_set
        count = request.user.databaseinfo_set.filter(is_deleted=False).count()
        # count = request.user.addresses.count()  # 语法2：一查多，使用related_name查询

        if count > constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg':
                                      '超出用户数据库的上限'})

        # 接收参数
        json_dict = json.loads(request.body.decode())
        host_ip = json_dict.get('host_ip')
        dbuser = json_dict.get('dbuser')
        dbpassword = json_dict.get('dbpassword')
        dbport = json_dict.get('dbport')

        # 校验参数
        if not all([host_ip, dbuser, dbpassword, dbport]):
            return http.HttpResponseForbidden('缺少必传参数')
        # if not re.match(r'^1[3-9]\d{9}$', mobile):
        #     return http.HttpResponseForbidden('参数mobile有误')

        # 保存用户传入的数据库信息
        try:
            databaseinfo = DatabaseInfo.objects.create(
                user=request.user,
                host_ip=host_ip,   # 标题默认就是IP
                dbuser=dbuser,
                dbpassword=dbpassword,
                dbport=dbport,
            )

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增用户数据库失败'})

        # 响应新增地址结果：需要将新增的地址返回给前端渲染
        database_dict = {
            "id": databaseinfo.id,
            "host_ip": databaseinfo.host_ip,
            "dbuser": databaseinfo.dbuser,
            "dbpassword": databaseinfo.dbpassword,
            "dbport": databaseinfo.dbport
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增数据库成功', 'database': database_dict})


class BackupView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, "backup.html")

    def post(self, request):
        """实现用户注册业务逻辑"""
        # 接收参数
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        userdb = request.POST.get('userdb')
        db = DatabaseInfo.objects.get(title=userdb, user=user)
        # HostIP = request.POST.get('HostIP')
        HostIP = db.host_ip
        # dbuser = request.POST.get('username')
        dbuser = db.dbuser
        # password = request.POST.get('password')
        password = db.dbpassword
        # port = request.POST.get('port')
        port = db.dbport
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
        (retcode, res) = subprocess.getstatusoutput(command)
        command1 = 'ls -t /tmp/xtra_test/|head -n1'
        (retcode1, res1) = subprocess.getstatusoutput(command1)
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        try:

            backup = BackupInfo.objects.create(order_id=order_id,
                                               user=user,
                                               db=db,
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
        # username = request.COOKIES.get('username')
        # user = User.objects.get(username=username)
        # HostIP = request.POST.get('HostIP')
        # dbuser = request.POST.get('username')
        # password = request.POST.get('password')
        # port = request.POST.get('port')
        # allow = request.POST.get('allow')
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        userdb = request.POST.get('userdb')
        db = DatabaseInfo.objects.get(title=userdb)
        # HostIP = request.POST.get('HostIP')
        HostIP = db.host_ip
        # dbuser = request.POST.get('username')
        dbuser = db.dbuser
        # password = request.POST.get('password')
        password = db.dbpassword
        # port = request.POST.get('port')
        port = db.dbport
        allow = request.POST.get('allow')
        filename = request.POST.get('userbk')


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
        (retcode, res) = subprocess.getstatusoutput(command)
        command1 = 'ls -t /tmp/xtra_test/|head -n1'
        (retcode1, res1) = subprocess.getstatusoutput(command1)
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        try:
            # backup = BackupInfo.objects.create(order_id=order_id,
            #                                    user=user,
            #                                    host_ip=HostIP,
            #                                    dbuser=dbuser,
            #                                    dbport=port,
            #                                    dbpassword=password,
            #                                    status=retcode,
            #                                    filename=res1)
            backup = BackupInfo.objects.create(order_id=order_id,
                                               user=user,
                                               db=db,
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


class UserDatabaseView(LoginRequiredMixin, View):
    """用户数据库"""

    def get(self, request):
        """查询并展示用户数据库信息"""

        # 获取当前登陆用户对象
        login_user = request.user
        databaseinfos = DatabaseInfo.objects.filter(user=login_user, is_deleted=False)

        # 将用户数据库模型列表转字典列表：因为Vue.js不认识模型列表，只有Django和Jinja2模板引擎认识
        database_list = []
        for databaseinfo in databaseinfos:
            database_dict = {
                # "id": databaseinfo.id,
                "title": databaseinfo.title,
                # 'host_ip': databaseinfo.host_ip,
                # 'dbuser': databaseinfo.dbuser,
                # 'dbpassword': databaseinfo.dbpassword,
                # 'dbport': databaseinfo.dbport
            }
            database_list.append(database_dict)

        # 构造上下文
        # context = {
        #
        #     'userdatabases': database_list,
        # }

        # return render(request, 'user_center_site.html', context)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '查询成功', 'userdatabases': database_list})


class UserFileView(LoginRequiredMixin, View):
    """用户备份"""

    def get(self, request):
        """查询并展示用户备份信息"""

        # 获取当前登陆用户对象
        login_user = request.user
        backupinfos = BackupInfo.objects.filter(user=login_user)

        file_list = []
        for backupinfo in backupinfos:
            file_dict = {
                "filename": backupinfo.filename,
            }
            file_list.append(file_dict)

        # return render(request, 'user_center_site.html', context)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '查询成功', 'userbackupinfos': file_list})