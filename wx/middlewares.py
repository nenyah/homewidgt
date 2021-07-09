#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   middlewares.py
@Time    :   2021/7/9 17:10 
@Author  :   Steven Tan
@Version :   1.0
@Contact :   steven.t.y#outlook.com (replace # to @)
@License :   (C)Copyright 2021-2022, Xirui-NLPR-CASIA
@Desc    :   None
"""
from django.utils.deprecation import MiddlewareMixin


class MiddlewareHead(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        if request:
            response['Access-Control-Allow-Origin'] = '*'
        return response
