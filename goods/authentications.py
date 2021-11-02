# !/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   authentications.py
@Time    :   2021/11/2 9:10
@Author  :   Steven Tan
@Version :   1.0
@Contact :   steven.t.y#outlook.com (replace # to @)
@License :   (C)Copyright 2021-2022, Xirui-NLPR-CASIA
@Desc    :   custom authentications
"""
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    对象级权限仅允许对象的所有者对其进行编辑
    假设模型实例具有`create_by`属性。
    """

    def has_object_permission(self, request, view, obj):
        # 示例必须要有一个名为`create_by`的属性
        return obj.create_by == request.user
