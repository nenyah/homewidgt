#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   serializers.py
@Time    :   2021/7/9 17:07 
@Author  :   Steven Tan
@Version :   1.0
@Contact :   steven.t.y#outlook.com (replace # to @)
@License :   (C)Copyright 2021-2022, Xirui-NLPR-CASIA
@Desc    :   None
"""
import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError

from homewidgt import settings
from .models import WxUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = 'wx_{0}'.format(user.username)
        return token

    def validate(self, attrs):
        """token验证
        """
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username  # 这个是你的自定义返回的
        data['user_id'] = self.user.id  # 这个是你的自定义返回的

        return data


class WxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        exclude = ('password',)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=32, error_messages={
        'required': '没有获取到,系统错误请退出重试',
    })

    def validate_code(self, code):
        """验证code
        """
        #  用 code 和腾讯服务器验证信息
        api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
        try:
            session_info = api.exchange_code_for_session_key(code=code)
        except OAuth2AuthExchangeError:
            raise ValidationError({"error": "WeChat server return error, please try again later"})
        openid = session_info.get('openid', None)
        return openid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = ('username', 'password')

    def validate_password(self, password):
        user = WxUser.objects.filter(username=self.initial_data['username']).first()
        if not user:
            if user.check_password(password):
                return

        raise serializers.ValidationError('密码错误')
