# 编写者：张金垚
# 开发时间 :2025/2/14 15:03
from django.urls import path
from .views import FaceRegisterView, FaceVerifyView

# 为face应用程序定义URL模式
urlpatterns = [
    # 人脸注册端点
    path('register', FaceRegisterView.as_view(), name='face-register'),
    path('verify', FaceVerifyView.as_view(), name='face-verify'),
]
