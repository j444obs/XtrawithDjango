# XtrawithDjango项目简介

一款基于Django Web框架开发的可视化数据库备份工具。通过开源数据库备份工具Xtrabackup实现图形化数据库的全量和增量备份。

### 项目结构


```
XtrawithDjango/                 # 仓库目录
├── nginx.conf                  # nginx配置文件
├── README.md
├── Xtra                        # 项目目录
│   ├── db.sqlite3
│   ├── logs                    # 日志目录
│   │   └── xtra.log
│   ├── manage.py               
│   ├── wsgi.ini                # uwsgi配置文件
│   └── Xtra                    # 工程目录
│       ├── apps                # 应用目录
│       │   ├── contents        # 备份和展示应用
│       │   ├── users                   # 用户管理应用
│       │   └── verifications           # 认证应用
│       ├── db.sqlite3
│       ├── __init__.py
│       ├── settings            # 工程配置目录
│       │   ├── dev.py
│       │   ├── __init__.py
│       │   ├── prod.py
│       ├── static              # 工程静态文件目录
│       │   ├── css
│       │   ├── images
│       │   └── js
│       ├── templates           # 工程模板目录
│       ├── urls.py
│       ├── utils	          # 工程工具目录
│       └── wsgi.py
└── Xtra.ini            # Xtra项目的supervisord管理配置文件

```

### 环境配置
OS: CentOS7
</br>Python:Python3.5+
</br>Python模块：

</br>mod.txt
```
Django==1.11.11
django-redis==4.11.0
Jinja2==2.11.1
Pillow==7.1.1
PyMySQL==0.9.3
```

## 安装步骤
### 1. 安装Xtrabackup

```
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.9/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm
yum install -y percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm
```
### 2. 配置MySQL(安装略)


```
create database Xtra charset=utf8;
create user Xtra identified by '123456';
grant all on Xtra.* to 'Xtra'@'%';
flush privileges;
```

### 3. 安装Redis

```
yum -y install redis
```

### 4. 开始搭建XtrawithDjango项目
#### (1) 准备项目目录拉取代码


```
mkdir Xtra
mkdir /tmp/xtra_test/
cd Xtra/
yum -y install git
git clone "https://github.com/wuyangdevops/XtrawithDjango.git"
cd XtrawithDjango/
```

#### (2) 安装虚拟环境（略）迁移数据表

```
mkvirtualenv -p python3 Xtra
pip3 install -r mod.txt
python manage.py makemigrations
python manage.py migrate
```

#### (3) 测试Django能否正常运行

```
python manage.py runserver 0.0.0.0:80
```

### 5. 生产环境搭建XtrawithDjango项目
#### (1) 安装supervisor

```
yum -y install python3-devel
yum install epel-release
yum install -y supervisor
systemctl enable supervisord
systemctl start supervisord
```
#### (2) 安装Nginx

```
yum -y install nginx
systemctl enable nginx
systemctl start nginx
```
#### (3) 配置Nginx
请修改/etc/nginx/nginx.conf配置文件中如下内容

```
user root;
...
        location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:8000;
        }
        location /static {
         alias /root/Xtra/XtrawithDjango/Xtra/Xtra/static;
       }
```
然后重启Nginx

```
systemctl restart nginx
```
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/nginx.png)


#### (4) 配置uwsgi托管Django


```
pip3 install uwsgi
```
该工程中wsgi.ini配置信息如下：

```
"""
WSGI config for WebXtra project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
[uwsgi]
socket=127.0.0.1:8000
chdir=/root/Xtra/XtrawithDjango/Xtra
wsgi-file=Xtra/wsgi.py
processes=4
threads=2
master=True
pidfile=uwsgi.pid
daemonize=uwsgi.log
virtualenv=/root/.virtualenvs/Xtra/
```

使用supervisord来管理uwsgi进程
</br>将Xtra.ini配置文件放入/etc/supervisord.d/目录
</br>重载supervisord

```
supervisorctl reload
```

![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/uwsgi.png)

## 体验
http://47.100.98.161/
</br>线上代码只可备份本机数据库，需要尝试体验请与作者联系获取本机数据库测试账号密码

```
        command = "/usr/bin/innobackupex --user=" + dbuser \
                  + " --password=" + password \
                  + " --host=" + "127.0.0.1" \
                  + " --port=" + port \
                  + " --incremental /tmp/xtra_test/" \
                  + " --incremental-basedir=/tmp/xtra_test/" \

```

## 页面展示

### 1. 注册
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/register.png)
### 2. 登录
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/login.png)
### 3. 首页介绍
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/desc.png)
### 4. 全量备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/fullbackup.png)
### 5. 查询备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/show.png)
### 6. 增量备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/incre.png)

## 作者联系方式
Email：wuyangdevops@163.com



