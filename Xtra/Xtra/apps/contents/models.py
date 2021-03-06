from django.db import models

from users.models import User
from Xtra.utils.models import BaseModel

# Create your models here.


class DatabaseInfo(BaseModel):
    """数据库信息 - 一"""

    # db_id = models.CharField(max_length=64, primary_key=True, verbose_name="数据库编号")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="数据库用户")
    title = models.CharField(max_length=64, verbose_name="用户数据库名称")
    host_ip = models.CharField(max_length=64, verbose_name="服务器IP")
    dbuser = models.CharField(max_length=64, verbose_name="数据库用户")
    dbpassword = models.CharField(max_length=64, verbose_name="数据库用户密码")
    dbport = models.CharField(max_length=64, verbose_name="数据库端口")
    # status = models.SmallIntegerField(default=0, verbose_name="备份状态")
    # filename = models.CharField(max_length=64, verbose_name="备份目录名称")
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = "tb_database_info"
        verbose_name = '用户数据库基本信息'
        verbose_name_plural = verbose_name


class BackupInfo(BaseModel):
    """订单信息 - 一"""

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="订单用户")
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="备份号")
    db = models.ForeignKey(DatabaseInfo, on_delete=models.PROTECT, verbose_name="数据库编号")
    status = models.SmallIntegerField(default=0, verbose_name="备份状态")
    filename = models.CharField(max_length=64, verbose_name="备份目录名称")

    class Meta:
        db_table = "tb_backup_info"
        verbose_name = '备份基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


