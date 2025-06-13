# 编写者：张金垚
# 开发时间 :2025/2/14 15:03
from django.urls import path
from datascreen.views import AttendanceStats

urlpatterns = [
    # 人脸注册端点
    path('Attendance', AttendanceStats.as_view(), name='AttendanceStats'),

]
