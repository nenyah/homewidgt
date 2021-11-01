import json
import logging

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError

from homewidgt import settings
from .models import WxUser
from .serializers import MyTokenObtainPairSerializer

logger = logging.getLogger('django')


class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义得到token username: 账号或者密码 password: 密码或者验证码
    """
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenViewBase):
    """
    自定义刷新token refresh: 刷新token的元素
    """
    serializer_class = TokenRefreshSerializer


def create_or_update_user_info(openid, user_info):
    """
    创建或者更新用户信息
    :param openid: 微信 openid
    :param user_info: 微信用户信息
    :return: 返回用户对象
    """
    if openid:
        if user_info:
            user, created = WxUser.objects.update_or_create(openid=openid, defaults=user_info)
        else:
            user, created = WxUser.objects.get_or_create(openid=openid)
        return user
    return None


class WxLoginView(APIView):
    """
    post:
    微信登录接口
    """
    authentication_classes = []
    permission_classes = []
    fields = {
        'nick_name': 'nickName',
        'gender': 'gender',
        'language': 'language',
        'city': 'city',
        'province': 'province',
        'country': 'country',
        'avatar_url': 'avatarUrl',
    }

    def post(self, request):
        user_info = dict()
        # 1. 获取参数信息
        code = request.data.get('code')
        logger.info("Code: {0}".format(code))
        user_info_raw = request.data.get('user_info', {})
        if isinstance(user_info_raw, str):
            user_info_raw = json.loads(user_info_raw)
        if not isinstance(user_info_raw, dict):
            user_info_raw = {}
        logger.info("user_info: {0}".format(user_info_raw))
        # 提前判断 没有 code 就返回错误信息
        if not code:
            return Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        # 2. 用 code 和腾讯服务器验证信息
        api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
        try:
            session_info = api.exchange_code_for_session_key(code=code)
        except OAuth2AuthExchangeError:
            session_info = None
        if not session_info:
            return Response({"error": "WeChat server return error, please try again later"})
        openid = session_info.get('openid', None)
        if not openid:
            return Response({"error": "WeChat server doesn't return openid"})
        if user_info_raw:
            for k, v in self.fields.items():
                user_info[k] = user_info_raw.get(v)
        # 3. 根据用户信息创建或更新用户
        user = create_or_update_user_info(openid, user_info)
        if not user:
            return Response({"error": "Internal error when create or update User"})
        # 4. 创建 JWT
        token = MyTokenObtainPairSerializer.get_token(user).access_token
        return Response(
            {
                'token': str(token),
                'user': model_to_dict(
                    user,
                    fields=[
                        'company', 'restaurant', 'current_role',
                        'is_owner', 'is_client', 'is_manager'
                    ])
            },
            status=HTTP_200_OK)


class WxLoginFakeView(APIView):
    """
    post:
    微信登录接口
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_info = dict()
        # 1. 获取参数信息
        username = request.data.get('username')
        password = request.data.get('password')
        logger.info("username: {0}".format(username))
        logger.info("password: {0}".format(password))
        # 提前判断 没有 code 就返回错误信息
        if not username:
            return Response({"username": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        # 3. 根据用户信息查找或创建
        user = WxUser.objects.filter(username=username).first()
        logger.info(f"user {user}")
        if not user:
            user = WxUser()
            user.username = username
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                return Response({"errmsg": "Invalid password"})
        # 4. 创建 JWT
        token = MyTokenObtainPairSerializer.get_token(user).access_token
        return Response(
            {
                'token': str(token),
                'user': model_to_dict(
                    user,
                    fields=[
                        'company', 'restaurant', 'current_role',
                        'is_owner', 'is_client', 'is_manager'
                    ])
            },
            status=HTTP_200_OK)
