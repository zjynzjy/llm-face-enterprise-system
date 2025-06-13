from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.utils import json
from rest_framework_jwt.settings import api_settings

from menu.models import SysMenu, SysMenuSerializer
from python222_admin2 import settings
from role.models import SysRole, SysUserRole
from user.models import SysUser, SysUserSerializer


class SaveView(View):
    def post(self, request):  # post通常为向服务器提交数据如表单等，而get通常向服务器获取数据。
        data = json.loads(request.body.decode("utf-8"))
        print(data)

        if data['id'] == -1:  # 添加操作
            pass
        else:  # 修改操作
            obj_sysUser = SysUser(
                id=data['id'],
                username=data['username'],
                password=data['password'],
                avatar=data['avatar'],
                email=data['email'],
                phonenumber=data['phonenumber'],
                login_date=data['login_date'],
                status=data['status'],
                create_time=data['create_time'],
                update_time=data['update_time'],
                remark=data['remark']
            )
            obj_sysUser.update_time = datetime.now().date()
            obj_sysUser.save()  # 更新数据库

        return JsonResponse({'code': 200})


class PwdView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']
        obj_user = SysUser.objects.get(id=id)
        if obj_user.password == oldPassword:
            obj_user.password = newPassword
            obj_user.update_time = datetime.now().date()
            obj_user.save()
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'code': 500, 'errorInfo': '原密码错误！'})


class LoginView(View):

    def buildTreeMenu(self, sysMenuList):  # 构造菜单树
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            # 寻找子节点
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, "children"):
                        menu.children = list()
                    menu.children.append(e)
            # 判断父节点，添加到集合
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def post(self, request):
        username = request.GET.get("username")
        password = request.GET.get("password")
        try:
            user = SysUser.objects.get(username=username, password=password)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 将用户对象传递进去，获取到该对象的属性值
            payload = jwt_payload_handler(user)
            # 将属性值编码成jwt格式的字符串
            token = jwt_encode_handler(payload)

            roleList = SysRole.objects.raw(
                "SELECT id ,NAME FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id=" + str(
                    user.id) + ")")
            print(roleList)
            # 当前用户拥有的角色，逗号隔开
            roles = ",".join([role.name for role in roleList])

            menuSet: set[SysMenu] = set()
            for row in roleList:
                print(row.id, row.name)
                menuList = SysMenu.objects.raw(
                    "SELECT * FROM sys_menu WHERE id IN (SELECT menu_id FROM sys_role_menu WHERE role_id=" + str(
                        row.id) + ")")
                for row2 in menuList:
                    print(row2.id, row2.name)
                    menuSet.add(row2)
            print(menuSet)
            menuList: list[SysMenu] = list(menuSet)  # set转list
            sorted_menuList = sorted(menuList)  # 根据order_num排序
            print(sorted_menuList)
            # 构造菜单树前段要求
            sysMenuList: list[SysMenu] = self.buildTreeMenu(sorted_menuList)
            print(sysMenuList)
            serializerMenuList = list()
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'info': '用户名或者密码错误！'})
        return JsonResponse({'code': 200, 'token': token, 'user': SysUserSerializer(user).data, 'info': '登录成功',
                             'roles': roles, 'menuList': serializerMenuList})


# Create your views here.
class TestView(View):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != None and token != '':
            userList_obj = SysUser.objects.all()
            print(userList_obj, type(userList_obj))
            userList_dict = userList_obj.values()  # 转存字典
            print(userList_dict, type(userList_dict))
            userList = list(userList_dict)  # 把外层的容器转存List
            print(userList, type(userList))
            return JsonResponse({'code': 200, 'info': '测试！', 'data': userList})
        else:
            return JsonResponse({'code': 401, 'info': '没有访问权限！'})


class JwtTestView(View):

    def get(self, request):
        user = SysUser.objects.get(username='python222', password='123456')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 将用户对象传递进去，获取到该对象的属性值
        payload = jwt_payload_handler(user)
        # 将属性值编码成jwt格式的字符串
        token = jwt_encode_handler(payload)
        return JsonResponse({'code': 200, 'token': token})


# 前端上传图片，把图片保存在本地userAvatar文件夹
class ImageView(View):

    def post(self, request):
        file = request.FILES.get('avatar')
        print("file:", file)
        if file:
            # 图片文件以二进制传输
            # print("前100字节:", file.read(100))
            # file.seek(0)  # 重置文件指针
            file_name = file.name
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\userAvatar\\" + new_file_name
            print("file_path:", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({'code': 200, 'title': new_file_name})
            except:
                return JsonResponse({'code': 500, 'errorInfo': '上传头像失败'})


# 用户确认更换头像，更新数据库中图片文件名称
class AvatarView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.save()
        return JsonResponse({'code': 200})


class SearchView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小
        query = data['query']  # 查询参数
        print(pageSize, pageNum)
        userListPage = Paginator(SysUser.objects.filter(username__icontains=query), pageSize).page(pageNum)
        print(userListPage)
        obj_users = userListPage.object_list.values()  # 转成字典
        users = list(obj_users)  # 把外层的容器转成List
        for user in users:
            userId = user['id']
            roleList = SysRole.objects.raw(
                "SELECT id,NAME FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id=" + str(
                    userId) + ")")
            roleListDict = []
            for role in roleList:
                roleDict = {}
                roleDict["id"] = role.id
                roleDict["name"] = role.name
                roleListDict.append(roleDict)
            user['roleList'] = roleListDict
        total = SysUser.objects.filter(username__icontains=query).count()
        return JsonResponse({'code': 200, 'userList': users, 'total': total})


# 重置密码
class PasswordView(View):

    def get(self, request):
        id = request.GET.get("id")
        user_object = SysUser.objects.get(id=id)
        user_object.password = "123456"
        user_object.update_time = datetime.now().date()
        user_object.save()
        return JsonResponse({'code': 200})


# 用户状态修改
class StatusView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        status = data['status']
        user_object = SysUser.objects.get(id=id)
        user_object.status = status
        user_object.save()
        return JsonResponse({'code': 200})


# 用户角色授权
class GrantRole(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        user_id = data['id']
        roleIdList = data['roleIds']
        print(user_id, roleIdList)
        SysUserRole.objects.filter(user_id=user_id).delete()  # 删除用户角色关联表中的指定用户数据
        for roleId in roleIdList:
            userRole = SysUserRole(user_id=user_id, role_id=roleId)
            userRole.save()
        return JsonResponse({'code': 200})


class ActionView(View):

    def get(self, request):
        """
        根据id获取用户信息
        :param request:
        :return:
        """
        id = request.GET.get("id")
        user_object = SysUser.objects.get(id=id)
        return JsonResponse({'code': 200, 'user': SysUserSerializer(user_object).data})

    def delete(self, request):
        """
        删除操作
        :param request:
        :return:
        """
        idList = json.loads(request.body.decode("utf-8"))
        SysUserRole.objects.filter(user_id__in=idList).delete()
        SysUser.objects.filter(id__in=idList).delete()
        return JsonResponse({'code': 200})


class CheckView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        print("username=", username)
        if SysUser.objects.filter(username=username).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})
