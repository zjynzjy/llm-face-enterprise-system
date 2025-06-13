"""
URL configuration for python222_admin2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from python222_admin2 import settings

urlpatterns = [
    path('user/', include('user.urls')),  # 用户模块
    path('role/', include('role.urls')),  # 角色模块
    path('menu/', include('menu.urls')),  # 权限模块
    path('face/', include('face.urls')),
    path('ai/', include('ai.urls')),
    path('datascreen/', include('datascreen.urls')),
    # 配置媒体文件的路由地址
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT},
            name='media')
]
