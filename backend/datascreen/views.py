from time import timezone

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from user.models import SysUser  # 替换为你的实际模型
from face.models import SysAttendance, SysSecurityLog
from datascreen.models import SysUserDepartment, SysDepartment
from django.db.models import Count


class AttendanceStats(APIView):

    # 安全表：统计异常打卡失败用户。
    # 打卡记录表+用户部门关联表：统计各部门打卡用户。
    #
    def get(self, request):

        user_all_count = SysUser.objects.count()
        print(f"用户员工总数: {user_all_count}")

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        print("today_start", today_start)
        print("today_end", today_end)

        # 查询当天打卡人数
        user_daka_count = SysAttendance.objects.filter(
            check_time__gte=today_start,  # 是一个 Django ORM 查询条件，表示 check_time 字段的值必须大于或等于 today_start
            check_time__lt=today_end  # lt 是 "less than" 的缩写
        ).values('user_id').distinct().count()

        print("今日打卡人数总数：", user_daka_count)

        # abnormal_count = SysSecurityLog.objects.filter(
        #     timestamp__gte=today_start,
        #     timestamp__lt=today_end
        # ).values('user_id').distinct().count()
        # 实际应根据数据库查询实现
        # 异常日志信息
        abnormal_log = SysSecurityLog.objects.filter(
            timestamp__gte=today_start,
            timestamp__lt=today_end
        ).values('user_id', 'timestamp', 'event_type').distinct()
        # print("abnormal_info:", abnormal_log)
        # 异常信息
        abnormal_info = []
        for log in abnormal_log:

            user_id = log['user_id']
            timestamp = log['timestamp']

            # 获取用户姓名
            user = SysUser.objects.get(id=user_id)
            user_name = user.username  # 假设SysUser表有name字段

            # 获取用户部门,select_related直接也访问Sysdepartment表,department是这个模型的外键。
            user_department = SysUserDepartment.objects.filter(user_id=user).select_related('department').first()
            # print("user_department:", user_department)
            department_name = user_department.department.name if user_department else "未知部门"

            # 计算迟到分钟数
            late_minutes = max(0, (timestamp.hour - 10) * 60 + timestamp.minute)
            if log['event_type'] == 'FACE_VERIFY_FAIL':
                # 拼接信息
                abnormal_info.append({
                    "time": timestamp.strftime("%H:%M"),
                    "department": department_name,
                    "message": f"{user_name}迟到{late_minutes}分钟"
                })
            else:
                # 拼接信息
                abnormal_info.append({
                    "time": timestamp.strftime("%H:%M"),
                    "department": department_name,
                    "message": f"{user_name}打卡位置异常"
                })
        # 异常人数
        abnormal_count = len(abnormal_log)
        # #研发部总人数统计
        #         yanfa_count = SysUserDepartment.objects.filter(
        #             department=1
        #         ).values('user').count()
        #         print("研发部人数：", yanfa_count)
        # #研发部今日打卡总人数统计
        #         yanfa_daka_count=SysAttendance.

        user_all_count = SysUser.objects.count()

        department_rate = []
        for dp_id in range(1, 5):
            # 获取研发部的所有用户ID
            department_user_ids = SysUserDepartment.objects.filter(department=dp_id).values_list('user_id', flat=True)
            # print("yanfa_user_ids:", department_user_ids)
            # 统计今日打卡的研发部用户数量
            department_attendance_count = SysAttendance.objects.filter(
                user_id__in=department_user_ids,
                check_time__gte=today_start,
                check_time__lt=today_end
            ).values('user_id').distinct().count()

            department_rate.append({
                "name": SysDepartment.objects.get(id=dp_id).name,
                "rate": round((department_attendance_count / len(department_user_ids)) * 100, 2) if len(
                    department_user_ids) else 0
            })
        print("department_rate:", department_rate)
        data = {
            "attendance_rate": user_daka_count / user_all_count * 100,  # 今日打卡用户/占公司总人数的比例.
            "abnormal_count": abnormal_count,  # 今日安全表中打卡失败用户人数+今日未打卡的员工
            # "departments": [
            #     {"name": "研发部", "rate": 96},  # 研发部用户今日打卡/研发部总人数
            #     {"name": "市场部", "rate": 89},
            #     {"name": "财务部", "rate": 93},
            #     {"name": "人事部", "rate": 97}
            # ],
            "departments": department_rate,
            # "trend_data": [
            #     {"date": (timezone.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            #      "rate": 90 + i % 5}
            #     for i in range(30, 0, -1)
            # ],
            "trend_data": [
                {
                    "date": (today_start - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "rate": round(
                        SysAttendance.objects.filter(
                            check_time__range=[
                                today_start - timedelta(days=i),
                                today_start - timedelta(days=i - 1)
                            ]
                        ).values('user_id').distinct().count() / user_all_count * 100,
                        2
                    ) if user_all_count else 0
                }
                for i in range(30, 0, -1)
            ],
            # "alerts": [
            #     {"time": "09:05", "department": "研发部", "message": "张三迟到15分钟"},
            #     {"time": "10:20", "department": "市场部", "message": "李四未打卡"}
            # ]
            "alerts": abnormal_info
        }
        return Response(data)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
# from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
# from datetime import timedelta
# from datascreen.models import SysDepartment
# from face.models import SysAttendance, SysSecurityLog
#
#
# class AttendanceStats(APIView):
#
#     def get(self, request):
#         # 获取当前时间及当天时间范围
#         now = timezone.now()
#         today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
#
#         # 1. 获取部门列表
#         departments = SysDepartment.objects.filter(is_active=True)
#
#         # 2. 计算整体在岗率
#         total_users = request.user.department.users.count()  # 假设用户关联了部门
#         attended_users = SysAttendance.objects.filter(
#             check_time__gte=today_start,
#             is_valid=True
#         ).values('user').distinct().count()
#         attendance_rate = round((attended_users / total_users) * 100, 2) if total_users else 0
#
#         # 3. 异常考勤统计
#         abnormal_count = SysSecurityLog.objects.filter(
#             event_type='FACE_VERIFY_FAIL',
#             timestamp__gte=today_start
#         ).count()
#
#         # 4. 部门出勤率计算
#         department_data = []
#         for dept in departments:
#             dept_users = dept.users.count()
#             attended = SysAttendance.objects.filter(
#                 user__sysuserdepartment__department=dept,
#                 check_time__gte=today_start,
#                 is_valid=True
#             ).values('user').distinct().count()
#             department_data.append({
#                 "name": dept.name,
#                 "rate": round((attended / dept_users) * 100, 2) if dept_users else 0
#             })
#
#         # 5. 趋势数据（最近30天）
#         trend_data = []
#         for i in range(30, 0, -1):
#             date = now - timedelta(days=i)
#             day_start = date.replace(hour=0, minute=0, second=0)
#             day_end = day_start + timedelta(days=1)
#
#             daily_attended = SysAttendance.objects.filter(
#                 check_time__range=(day_start, day_end),
#                 is_valid=True
#             ).values('user').distinct().count()
#
#             trend_data.append({
#                 "date": date.strftime("%Y-%m-%d"),
#                 "rate": round((daily_attended / total_users) * 100, 2) if total_users else 0
#             })
#
#         # 6. 实时预警信息
#         alerts = SysSecurityLog.objects.filter(
#             event_type__in=['FACE_VERIFY_FAIL', 'LOCATION_MISMATCH'],
#             timestamp__gte=today_start
#         ).order_by('-timestamp')[:10].values(
#             'timestamp',
#             'user__sysuserdepartment__department__name',
#             'event_type'
#         )
#
#         formatted_alerts = [{
#             "time": alert['timestamp'].strftime("%H:%M"),
#             "department": alert['user__sysuserdepartment__department__name'] or "未知部门",
#             "message": self.get_alert_message(alert['event_type'])
#         } for alert in alerts]
#
#         return Response({
#             "attendance_rate": attendance_rate,
#             "abnormal_count": abnormal_count,
#             "departments": department_data,
#             "trend_data": trend_data,
#             "alerts": formatted_alerts
#         })
#
#     def get_alert_message(self, event_type):
#         messages = {
#             'FACE_VERIFY_FAIL': '人脸验证失败',
#             'LOCATION_MISMATCH': '考勤位置异常'
#         }
#         return messages.get(event_type, '未知异常')
