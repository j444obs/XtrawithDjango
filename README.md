# XtrawithDjango
# 项目结构
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


# OS: CentOS7/Python:Python3.5+

# 1. Install Xtrabackup
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.9/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm
yum install -y percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm

# 2. MySQL Configuration
create database Xtra charset=utf8;
create user Xtra identified by '123456';
grant all on Xtra.* to 'Xtra'@'%';
flush privileges;

# 3. Reids
yum -y install redis

# 4. Intsall Xtra
# (1) Prepare Dir
mkdir Xtra
mkdir /tmp/xtra_test/
cd Xtra/
yum -y install git
git clone "https://github.com/wuyangdevops/XtrawithDjango.git"
cd XtrawithDjango/

# (2) Start
mkvirtualenv -p python3 Xtra
pip3 install -r mod.txt

cat mod.txt
Django==1.11.11
django-redis==4.11.0
Jinja2==2.11.1
Pillow==7.1.1
PyMySQL==0.9.3

python manage.py makemigrations
python manage.py migrate

# (3) Test
python manage.py runserver 0.0.0.0:80

# (4) Production
# Install supervisord
yum -y install python3-devel
yum install epel-release
yum install -y supervisor
systemctl enable supervisord
systemctl start supervisord

# Install Nginx 
yum -y install nginx
systemctl enable nginx
systemctl start nginx

# configure Nginx
user root;
vim /etc/nginx/nginx.conf
        location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:8000;
        }
        location /static {
         alias /root/Xtra/XtrawithDjango/Xtra/Xtra/static;
       }

systemctl restart nginx
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/nginx.png)

# configure uwsgi
pip3 install uwsgi
cd /etc/supervisord.d/
vim Xtra.ini

"""
WSGI config for meiduo_mall project.

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

# reload supervisord
supervisorctl reload
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/uwsgi.png)

# Experience
http://47.100.98.161/

# 1. 注册
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/register.png)
# 2. 登录
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/login.png)
# 3. 首页介绍
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/desc.png)
# 4. 全量备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/fullbackup.png)
# 5. 查询备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/show.png)
# 6. 增量备份
![image](https://github.com/wuyangdevops/XtrawithDjango/blob/master/Pic/incre.png)



