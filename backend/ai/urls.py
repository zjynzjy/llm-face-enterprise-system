# 编写者：张金垚
# 开发时间 :2025/2/14 15:03
# from django.urls import path
#
# from ai.views import XunfeiView
#
# # 为face应用程序定义URL模式
# urlpatterns = [
#     # 人脸注册端点
#     path('xunfei', XunfeiView.as_view(), name='ai'),
#
# ]
from django.urls import path
from ai.views import ChatView

urlpatterns = [
    path('deepseek', ChatView.as_view(), name='deepseek'),
]
