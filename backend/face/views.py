from django.utils import timezone
from django.utils.timezone import now, localtime
from rest_framework.decorators import api_view
import numpy as np
import pickle
import logging
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import math
from user.models import SysUser
from .models import SysFaceFeature, SysAttendance, SysSecurityLog

from datascreen.models import SysDepartment
from datascreen.models import SysUserDepartment
import datetime
import pytz

# 配置日志
logger = logging.getLogger(__name__)


class FaceRegisterView(APIView):
    """
    人脸注册API - 使用当前登录用户并确保数据正确保存
    """

    def post(self, request):
        # print("hhhhh")
        """
        处理人脸注册请求
        从Token获取用户，从请求体获取人脸特征向量
        """
        # 详细记录请求信息
        # print(request)
        logger.info(f"收到人脸注册请求 - 用户: {request.user.username}")
        logger.info(f"请求内容: {request.data}")

        # 获取特征数据
        feature_vector = request.data.get('feature')

        # 获取用户信息（实际应从token获取，此处演示前端传参方式）
        user_data = request.data.get('user', {})
        id = user_data.get('user')  # 注意字段名冲突
        username = user_data.get('name')  # 注意字段名冲突

        # print(feature_vector)
        # print(id)
        # print(username)

        try:
            # 获取当前用户
            user = user_data
            logger.info(f"处理用户: {username}, ID: {id}")

            # # 验证特征数据
            # if 'feature' not in request.data:
            #     logger.error("缺少特征数据")
            #     return Response({
            #         'code': 400,
            #         'message': '缺少人脸特征数据'
            #     }, status=status.HTTP_400_BAD_REQUEST)

            # 获取特征向量
            feature_vector = request.data['feature']
            logger.info(f"特征向量长度: {len(feature_vector) if isinstance(feature_vector, list) else 'unknown'}")

            # 验证特征向量格式
            if not isinstance(feature_vector, list):
                logger.error(f"特征向量格式错误: {type(feature_vector)}")
                return Response({
                    'code': 400,
                    'message': f'特征向量格式错误: {type(feature_vector)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 检查用户是否已注册人脸
            existing_feature = SysFaceFeature.objects.filter(user=id).first()
            if existing_feature:
                logger.warning(f"用户 {username} 已注册人脸信息")
                return Response({
                    'code': 400,
                    'message': '该用户已注册人脸信息，请联系管理员'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 将特征向量转换为二进制格式存储
            try:
                feature_np = np.array(feature_vector, dtype=np.float32)
                feature_binary = pickle.dumps(feature_np)
                logger.info(f"特征向量已转换为二进制, 大小: {len(feature_binary)} 字节")
            except Exception as e:
                logger.exception(f"特征向量转换失败: {str(e)}")
                return Response({
                    'code': 400,
                    'message': f'特征向量格式转换失败: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 创建User实例
            try:
                user = SysUser.objects.get(id=id)
                logger.info(f"处理用户: {username}, ID: {id}")
            except SysUser.DoesNotExist:
                logger.error(f"用户 {id} 不存在")
                return Response({
                    'code': 400,
                    'message': f'用户 {id} 不存在'
                }, status=status.HTTP_400_BAD_REQUEST)
            # 使用事务确保数据正确保存
            with transaction.atomic():
                # 创建人脸特征记录
                face_feature = SysFaceFeature(
                    user=user,
                    feature=feature_binary
                )
                face_feature.save()

                # 验证数据已保存
                saved_feature = SysFaceFeature.objects.filter(user=user).first()
                if not saved_feature:
                    logger.error("数据看似已保存，但无法从数据库检索")
                    raise Exception("数据保存验证失败")

                logger.info(f"成功为用户 {username} 保存人脸特征，ID: {saved_feature.id}")

            # 返回成功响应
            return Response({
                'code': 200,
                'message': '人脸信息录入成功',
                'feature_id': saved_feature.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"人脸注册过程中发生错误: {str(e)}")
            return Response({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 人脸验证逻辑
class FaceVerifyView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # 获取中国时区
        china_timezone = pytz.timezone('Asia/Shanghai')

        # 获取当前中国时间
        china_time = datetime.datetime.now(china_timezone)

        # 格式化为MySQL datetime格式
        mysql_datetime_str = china_time.strftime("%Y-%m-%d %H:%M:%S")
        print("mysql_datetime_str:", mysql_datetime_str)
        """
        人脸验证接口
        1. 获取当前用户已注册的人脸特征
        2. 与传入特征进行相似度比对
        3. 记录考勤日志
        """
        try:
            # 获取请求数据
            current_feature = request.data.get('feature')
            location = request.data.get('location', '')  # 格式："经度,纬度"
            accuracy = request.data.get('accuracy', 0)  # 地理位置的精确度。单位：米
            device_info = request.data.get('device_info', {})
            user = request.data.get('user')

            # user = request.user
            # try:
            #     sys_user = SysUser.objects.get(id=user.id)  # 获取 SysUser 实例
            # except SysUser.DoesNotExist:
            #     return Response({
            #         'code': 400,
            #         'message': '用户信息不存在'
            #     }, status=400)

            # 获取当前用户
            # print(user)

            # 查询已注册的人脸特征
            try:
                stored_feature = SysFaceFeature.objects.get(user=user).feature
                stored_vector = pickle.loads(stored_feature)
                # print("反序列化后的python对象人脸特征：", stored_vector)
            except SysFaceFeature.DoesNotExist:
                return Response({
                    'code': 400,
                    'message': '请先完成人脸注册'
                }, status=400)
            # print("current：", current_feature)
            # # 转换当前特征
            current_vector = np.array(current_feature, dtype=np.float32)
            # print("当前特征：", current_vector)

            # 计算余弦相似度
            similarity = self.cosine_similarity(stored_vector, current_vector)
            match_threshold = 0.95  # 相似度阈值

            print("用户的location:", location)
            # 验证位置有效性

            is_location_valid = self.check_location(location, user)
            print("is_location_valid:", is_location_valid)
            # print("Django 服务器当前时间 (UTC):", now())  # 可能是 UTC 时间
            # print("Django 本地时间:", localtime(now()))  # 用到再转为北京时间
            sys_user = SysUser.objects.get(id=user)
            if similarity >= match_threshold and is_location_valid:
                # 创建考勤记录

                with transaction.atomic():  # 使用事务确保数据正确保存
                    attendance = SysAttendance.objects.create(
                        user=sys_user,
                        location=location,
                        accuracy=accuracy,
                        face_match_score=similarity,
                        device_info=device_info,
                        is_valid=similarity >= match_threshold and is_location_valid,  # 返回布尔值存在tinyint类型字段为0或1.
                        check_time=timezone.now()  # # 显式设置检查时间，存的是UTc时时间
                    )
                return Response({
                    'code': 200,
                    'success': attendance.is_valid,
                    'similarity': similarity,
                    'attendance_id': attendance.id
                })
            else:
                # 记录安全日志
                if similarity < match_threshold:
                    SysSecurityLog.objects.create(
                        user=sys_user,
                        event_type='FACE_MATCH_FAIL',
                        timestamp=mysql_datetime_str
                        # event_data={'similarity': similarity}
                    )
                    return Response({
                        'code': 400,
                        'success': False,
                        'similarity': similarity,
                        'location': is_location_valid,
                    })
                else:
                    SysSecurityLog.objects.create(
                        user=sys_user,
                        event_type='LOCATION_MISMATCH',
                        timestamp=mysql_datetime_str
                        # event_data={'location': location}
                    )
                    return Response({
                        'code': 400,
                        'success': False,
                        'similarity': similarity,
                        'location': is_location_valid,
                    })



        except Exception as e:
            logger.error(f"人脸验证失败: {str(e)}")
            return Response({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=500)

    #           余弦相似度计算，点积除模积
    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def check_location(self, coordinates, departmentid):
        dept = SysDepartment.objects.get(id=departmentid)
        # 实现位置校验逻辑（对比公司预设位置）
        lat1 = dept.latitude

        lon1 = dept.longitude
        radius = dept.radius

        lat2, lon2 = map(float, coordinates.split(','))

        # 计算距离
        distance = self.haversine(lat1, lon1, lat2, lon2)
        if distance <= radius:
            return 1
        else:
            return 0

    def haversine(self, lat1, lon1, lat2, lon2):
        # 地球半径，单位为公里
        R = 6371.0

        # 将经纬度从度数转换为弧度
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # 计算差值
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        # Haversine公式
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # 计算距离，单位为公里
        distance_km = R * c

        # 转换为米
        distance_m = distance_km * 1000
        print("distance_m:", distance_m)
        return distance_m
