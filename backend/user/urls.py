# 编写者：张金垚
# 开发时间 :2025/2/14 15:03
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from django.urls import path
from user.views import TestView, JwtTestView, LoginView, SaveView, PwdView, ImageView, AvatarView, SearchView
from user.views import TestView, JwtTestView, LoginView, SaveView, PwdView, ImageView, AvatarView, SearchView, \
    ActionView, CheckView, PasswordView, StatusView, GrantRole

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),  # 登录
    path('test', TestView.as_view(), name='test'),  # 测试
    path('jwt_test', JwtTestView.as_view(), name='jwt_test'),  # jwt测试
    path('save', SaveView.as_view(), name='save'),  # 用户信息修改
    path('updateUserPwd', PwdView.as_view(), name='updateUserPwd'),  # 修改密码
    path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 头像上传
    path('updateAvatar', AvatarView.as_view(), name='updateAvatar'),  # 更新头像
    path('search', SearchView.as_view(), name='search'),  # 用户信息分页查询
    path('action', ActionView.as_view(), name='action'),  # 用户信息操作
    path('check', CheckView.as_view(), name='check'),  # 用户名查重
    path('resetPassword', PasswordView.as_view(), name='resetPassword'),  # 重置密码
    path('status', StatusView.as_view(), name='status'),  # 状态修改
    path('grantRole', GrantRole.as_view(), name='grant'),  # 角色授权

]
