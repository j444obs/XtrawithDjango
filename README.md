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

# Experience
http://47.100.98.161/







