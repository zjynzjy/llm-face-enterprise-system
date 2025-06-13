# 编写者：张金垚
# 开发时间 :2025/3/2 17:29
from rest_framework import serializers
from .models import SysFaceFeature, SysAttendance
from user.models import SysUser
import numpy as np


# 人脸特征序列化器
class FaceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysFaceFeature
        fields = ['feature', 'create_time']
        read_only_fields = ['create_time']

    def validate_feature(self, value):
        """验证特征向量格式"""
        try:
            # 将前端传来的列表转换为numpy数组验证
            arr = np.array(value, dtype=np.float32)
            if arr.shape != (128,):
                raise serializers.ValidationError("特征向量维度必须为128维")
            return arr.tobytes()
        except Exception as e:
            raise serializers.ValidationError(f"无效的特征数据: {str(e)}")


# 考勤记录序列化器
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysAttendance
        fields = '__all__'
        read_only_fields = ['check_time', 'is_valid']


# 人脸注册序列化器
class FaceRegistrationSerializer(serializers.Serializer):
    features = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            min_length=128,
            max_length=128
        ),
        min_length=3,
        max_length=5
    )

    def validate_features(self, value):
        """验证多角度特征样本"""
        try:
            features = [np.array(f, dtype=np.float32) for f in value]
            merged = self.merge_features(features)
            return merged.tobytes()
        except ValueError as e:
            raise serializers.ValidationError(f"特征数据异常: {str(e)}")

    @staticmethod
    def merge_features(features):
        """特征融合算法"""
        weights = [0.3, 0.4, 0.3]  # 不同角度的权重
        merged = np.zeros(128, dtype=np.float32)
        for i, feature in enumerate(features[:3]):
            merged += weights[i] * feature
        return merged / len(features[:3])
