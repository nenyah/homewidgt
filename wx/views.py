import json
import logging

from django.forms import model_to_dict
from rest_framework import viewsets, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from .models import WxUser
from .serializers import MyTokenObtainPairSerializer, WxUserSerializer, CodeSerializer

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
    if not openid:
        raise Exception("invalid openid")
    if user_info:
        user, created = WxUser.objects.update_or_create(openid=openid, defaults=user_info)
    else:
        user, created = WxUser.objects.get_or_create(openid=openid, username=openid)
    return user


class WxLoginViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """微信登录
    """
    serializer_class = CodeSerializer
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

    def create(self, request, *args, **kwargs):
        user_info = dict()
        user_info_raw = request.data.get('user_info', {})
        if isinstance(user_info_raw, str):
            user_info_raw = json.loads(user_info_raw)
        if not isinstance(user_info_raw, dict):
            user_info_raw = {}
        if user_info_raw:
            for k, v in self.fields.items():
                user_info[k] = user_info_raw.get(v)

        logger.info("user_info: {0}".format(user_info_raw))
        # 1. 校验参数
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # # validated_data 经过验证的数据
        openid = serializer.validated_data['code']

        # 3. 根据用户信息创建或更新用户
        user = WxUser.objects.filter(openid=openid).first()
        if not user:
            try:
                user = create_or_update_user_info(openid, user_info)
            except Exception as ex:
                return Response({"error": ex})
        # 4. 创建 JWT
        token = MyTokenObtainPairSerializer.get_token(user).access_token
        return Response(
            {
                'token': str(token),
                'user': model_to_dict(
                    user,
                    fields=[
                        'username', 'openid', 'avatar_url', 'nick_name',
                    ])
            },
            status=HTTP_200_OK)


class FakeLoginViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """测试登录
    """
    serializer_class = CodeSerializer
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

    def create(self, request, *args, **kwargs):
        user_info = dict()
        user_info_raw = request.data.get('user_info', {})
        if isinstance(user_info_raw, str):
            user_info_raw = json.loads(user_info_raw)
        if not isinstance(user_info_raw, dict):
            user_info_raw = {}
        if user_info_raw:
            for k, v in self.fields.items():
                user_info[k] = user_info_raw.get(v)

        # 1. 不校验参数
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # # validated_data 经过验证的数据
        # openid = serializer.validated_data['code']
        # 模拟获取 openid
        openid = request.data.get('code', '123456789')
        # 3. 根据用户信息创建或更新用户
        try:
            user = create_or_update_user_info(openid, user_info)
        except Exception as ex:
            return Response({"error": ex})
        # 4. 创建 JWT
        token = MyTokenObtainPairSerializer().get_token(user).access_token
        return Response(
            {
                'token': str(token),
                'user': model_to_dict(
                    user,
                    fields=[
                        'username', 'openid', 'avatar_url', 'nick_name',
                    ])
            },
            status=HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WxUser.objects.all()
    serializer_class = WxUserSerializer
    permission_classes = (permissions.IsAdminUser,)
