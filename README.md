# XtrawithDjango
# OS: CentOS7/Python:Python3.5+

# Install Xtrabackup
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.9/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm
yum install -y percona-xtrabackup-24-2.4.9-1.el7.x86_64.rpm

# MySQL Configuration
create database Xtra charset=utf8;
create user Xtra identified by '123456';
grant all on Xtra.* to 'Xtra'@'%';
flush privileges;

# Reids
yum -y install redis

# Intsall
# Prepare Dir
mkdir Xtra
mkdir /tmp/xtra_test/
cd Xtra/
yum -y install git
git clone "https://github.com/wuyangdevops/XtrawithDjango.git"
cd XtrawithDjango/

# Start
mkvirtualenv -p python3 Xtra
pip3 install -r mod.txt
python manage.py makemigrations
python manage.py migrate

# Test
python manage.py runserver 0.0.0.0:80

# Production
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

supervisorctl reload

# Experience
http://47.100.98.161/

https://github.com/wuyangdevops/XtrawithDjango/blob/master/register.png





