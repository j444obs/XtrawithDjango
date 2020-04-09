# XtrawithDjango
# -----------MySQL Configuration----------------
create database Xtra charset=utf8;
create user Xtra identified by '123456';
grant all on Xtra.* to 'Xtra'@'%';
flush privileges;
