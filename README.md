# XtrawithDjango
# -----------MySQL Configuration----------------
create database Xtra charset=utf8;
create user Xtra identified by '123456';
grant all on Xtra.* to 'Xtra'@'%';
flush privileges;

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
