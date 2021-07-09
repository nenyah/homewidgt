#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   urls.py
@Time    :   2021/7/9 17:10 
@Author  :   Steven Tan
@Version :   1.0
@Contact :   steven.t.y#outlook.com (replace # to @)
@License :   (C)Copyright 2021-2022, Xirui-NLPR-CASIA
@Desc    :   None
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = format_suffix_patterns([
    path('wx_login/', WxLoginView.as_view(), name='wx_login'),
    # 其他接口
])
