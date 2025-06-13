# 开发时间 :2025/2/17 16:07
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class JwtAuthenticationMiddleware(MiddlewareMixin):
    # process_request 方法是 Django 中间件的一个钩子方法，在每个请求到达视图之前被调用。它接收一个 request 参数，表示当前的 HTTP 请求对象。
    def process_request(self, request):
        white_list = ["/user/login", "/face/verify", "/datascreen/Attendance", "/user/search", "/ai/deepseek"]  # 请求白名单
        path = request.path
        if path not in white_list and not path.startswith("/media"):
            # print("要进行token验证")
            token = request.META.get('HTTP_AUTHORIZATION')
            # print("token:", token)
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                print("Token过期，请重新登录！")
                return HttpResponse('Token过期，请重新登录！')

            except InvalidTokenError:
                print('Token验证失败！')
                return HttpResponse('Token验证失败！')

            except PyJWTError:
                print('Token验证异常！')
                return HttpResponse('Token验证异常！')


        else:
            print("不验证验证")
            return None
