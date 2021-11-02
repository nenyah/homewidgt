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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecordsViewModel

router = DefaultRouter()
router.register('records', RecordsViewModel)
urlpatterns = [
    path('goods/', include(router.urls)),
    # 其他接口
]
