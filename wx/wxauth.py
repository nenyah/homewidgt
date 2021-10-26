# !/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   wxauth.py
@Time    :   2021/9/15 10:42
@Author  :   Steven Tan
@Version :   1.0
@Contact :   steven.t.y#outlook.com (replace # to @)
@License :   (C)Copyright 2021-2022, Xirui-NLPR-CASIA
@Desc    :   wechat authentication
"""
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import WxUser


class WechatOpenidAuth:
    """微信openid认证登录
    """

    def get_user(self, id_):
        try:
            return WxUser.objects.get(pk=id_)
        except WxUser.DoesNotExist:
            return None

    def authenticate(self, openid=None):
        try:
            user = WxUser.objects.get(openid=openid)
            if user is not None:
                return user
            return None
        except WxUser.DoesNotExist:
            return None


class JwtAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        # token = request.META.get('HTTP_Authorization'.upper())
        print(validated_token)
        # try:
        #     payload = jwt_decode_handler(token)
        # except jwt.ExpiredSignature:
        #     raise AuthenticationFailed('expired ')
        # except jwt.DecodeError:
        #     raise AuthenticationFailed('decoding error ')
        # except jwt.InvalidTokenError:
        #     raise AuthenticationFailed('illegal token ')
        # # The obtained user object should be the user object of its own user table
        # print(payload)
        # # user=MyUser.objects.get(id=payload['user_ ID ']) it's not good to write this. I will check the database every time
        # User = payload  # do not check the database every time
