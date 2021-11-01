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
from .models import WxUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        print("=" * 30, user)
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
        fields = '__all__'

    def validate(self, attrs):
        print("=" * 30)
        print(attrs)
        return attrs
        # usr = attrs.get('usr')
        # pwd = attrs.get('pwd')
        # 
        # # 多方式登录：各分支处理得到该方式下对应的用户
        # if re.match(r'.+@.+', usr):
        #     user_query = models.User.objects.filter(email=usr)
        # elif re.match(r'1[3-9][0-9]{9}', usr):
        #     user_query = models.User.objects.filter(mobile=usr)
        # else:
        #     user_query = models.User.objects.filter(username=usr)
        # user_obj = user_query.first()
        # 
        # # 签发：得到登录用户，签发token并存储在实例化对象中
        # if user_obj and user_obj.check_password(pwd):
        #     # 签发token，将token存放到 实例化类对象的token 名字中
        #     payload = jwt_payload_handler(user_obj)
        #     token = jwt_encode_handler(payload)
        #     # 将当前用户与签发的token都保存在序列化对象中
        #     self.user = user_obj
        #     self.token = token
        #     return attrs
        # 
        # raise serializers.ValidationError({'data': '数据有误'})


class LoginSerializer(serializers.ModelSerializer):
    # Rewrite username, otherwise an error will be reported
    code = serializers.CharField()

    class Meta:
        model = WxUser
        fields = ['code', ]

    def validate(self, attrs):
        code = attrs.get('code')
        print("validate code:", code)
        # 获取用户信息，此处自己构造
        user = WxUser.objects.get(id=2)
        refresh_token = MyTokenObtainPairSerializer.get_token(user)
        self.token = refresh_token.access_token
        self.refresh_token = refresh_token
        self.user = user
        # Username may be email, mobile phone number and user name
        # username = attrs.get('username')
        # password = attrs.get('password')
        # If it's a cell phone number
        # if re.match('^1[3-9]\d{9}$', username):
        #     # Login with mobile number
        #     user = WxUser.objects.filter(phone=username).first()
        # elif re.match('^.+@.+$', username):
        #     # Log in as mailbox
        #     user = WxUser.objects.filter(email=username).first()
        # else:
        #     # Log in as user name
        #     user = WxUser.objects.filter(username=username).first()
        #     # If user has a value and the password is correct
        # if user and user.check_password(password):
        #     # Login succeeded and a token is generated
        #     # DRF JWT has a method to generate a token through the user object
        #     payload = jwt_payload_handler(user)
        #     token = jwt_encode_handler(payload)
        #     # Token is to be used in the view class. Now we are in the serialization class
        #     # self.context.get('request')
        #     # The context dictionary is used to transfer data between the view class and the serialization class
        #     self.context['token'] = token
        #     self.context['username'] = user.username
        #     # Be sure to return
        #     return attrs
        #
        # else:
        #     raise ValidationError('wrong username or password ')
        return attrs
