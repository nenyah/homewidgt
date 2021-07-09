from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from wx.models import WxUser


@admin.register(WxUser)
class WxUserAdmin(UserAdmin):
    readonly_fields = (
        'last_login', 'date_joined',
        'nick_name', 'city', 'province', 'country', 'china_district', 'avatar_url'
    )
    search_fields = [
        'username', 'openid', 'email', 'first_name', 'last_name', 'nick_name'
    ]
    fieldsets = (
        (_('基础信息'), {'fields': ('username', 'password', 'openid')}),
        (_('个人信息'), {'fields': (
            'nick_name', 'first_name', 'last_name', 'avatar_url', 'gender', 'date_of_birth', 'desc')}),
        (_('联络信息'), {'fields': ('email',)}),
        (_('地址信息'), {'fields': ('city', 'province', 'country', 'china_district')}),
        (_('登录信息'), {'fields': ('last_login', 'date_joined')}),
    )
