from django.db import models

from users.models import User
from Xtra.utils.models import BaseModel

# Create your models here.


class BackupInfo(BaseModel):
    """订单信息 - 一"""
    BACKUP_STATUS_ENUM = {
        "SUCCESS": 0,
        "FAIL": 1
    }

    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="备份号")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="下单用户")
    host_name = models.CharField(max_length=64, default=None, verbose_name="服务器主机名")
    host_ip = models.CharField(max_length=64, verbose_name="服务器IP")
    dbuser = models.CharField(max_length=64, verbose_name="数据库用户")
    dbpassword = models.CharField(max_length=64, verbose_name="数据库用户密码")
    dir_name = models.CharField(max_length=64, verbose_name="备份目录名")
    status = models.SmallIntegerField(choices=BACKUP_STATUS_ENUM, default=0, verbose_name="备份状态")

    class Meta:
        db_table = "tb_backup_info"
        verbose_name = '备份基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id