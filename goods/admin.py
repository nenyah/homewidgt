from datetime import datetime, date

from django.contrib import admin

# Register your models here.
from goods.models import Goods


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.create_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('name', 'location', 'create_time', 'update_time', 'duration', 'create_by')

    fieldsets = [
        ('基本信息', {'fields': ['name', 'location', 'img', 'remark']}),
        ('有效期', {'classes': ('collapse',), 'fields': ['mfg', 'exp', 'duration']}),
    ]
    ordering = ('exp',)
    readonly_fields = ('duration',)

    @admin.display(description='有效天数', empty_value=None)
    def duration(self, obj):
        if obj.exp:
            return (obj.exp - date.today()).days
        return None
