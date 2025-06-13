from django.db import models
from user.models import SysUser


# Create your models here.

class SysDepartment(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="部门名称")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="纬度"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="经度"
    )
    radius = models.PositiveIntegerField(default=500, verbose_name="有效半径(米)")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        db_table = "sys_department"


# 部门-用户关联表
class SysUserDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SysUser, on_delete=models.PROTECT)
    department = models.ForeignKey(SysDepartment, on_delete=models.PROTECT)

    class Meta:
        db_table = "sys_user_department"
