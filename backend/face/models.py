from django.db import models
from user.models import SysUser


# 人脸特征表
class SysFaceFeature(models.Model):
    id = models.AutoField(primary_key=True)  # Django会自动为每个模型生成一个主键字段，名为id。
    user = models.OneToOneField(
        SysUser,
        on_delete=models.CASCADE,
        related_name='face_feature',
    )
    feature = models.BinaryField(verbose_name="人脸特征向量")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "sys_face_feature"


# 考勤记录表
class SysAttendance(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        SysUser,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        # ：related_name='attendance_records'这表示从 SysUser 实例反向访问其关联的 SysAttendance 记录时，可以使用 attendance_records 作为属性名。
        # 例如，如果你有一个 SysUser 实例 user_instance，你可以通过 user_instance.attendance_records.all() 获取该用户的所有考勤记录。

    )
    check_time = models.DateTimeField(auto_now_add=True, verbose_name="打卡时间")
    location = models.CharField(max_length=100, verbose_name="经纬度坐标")
    accuracy = models.FloatField(verbose_name="定位精度(米)")
    is_valid = models.BooleanField(default=False, verbose_name="是否有效")
    face_match_score = models.FloatField(verbose_name="人脸匹配度")
    device_info = models.JSONField(default=dict, verbose_name="设备信息")

    class Meta:
        db_table = "sys_attendance"
        indexes = [
            models.Index(fields=['user', 'check_time']),
        ]


# 公司位置表
class SysCompanyLocation(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="位置名称")
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
        db_table = "sys_company_location"


# 安全日志表
class SysSecurityLog(models.Model):
    EVENT_CHOICES = (
        ('FACE_REG_SUCCESS', '人脸注册成功'),
        ('FACE_VERIFY_FAIL', '人脸验证失败'),  # 打卡失败
        ('LOCATION_MISMATCH', '位置异常'),
        ('MULTI_DEVICE_LOGIN', '多设备登录'),
        ('ACCOUNT_LOCKED', '账户锁定'),
    )

    user = models.ForeignKey(
        SysUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="关联用户"
    )
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES, verbose_name="事件类型")
    event_data = models.JSONField(default=dict, verbose_name="事件数据")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="发生时间")

    class Meta:
        db_table = "sys_security_log"
        verbose_name = "安全日志"
        verbose_name_plural = verbose_name
        ordering = ['-timestamp']
