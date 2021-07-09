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
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import WxUser


class JfwTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = 'wx_{0}'.format(user.username)
        return token


class WxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = ['id', 'nick_name', 'avatar_url', 'gender']
