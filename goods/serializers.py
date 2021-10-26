from rest_framework import serializers
from .models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    create_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Goods
        fields = ['id', 'name', 'location', 'img', 'remark', 'mfg', 'exp', 'create_time', 'update_time', 'create_by']
        read_only = ['create_time', 'update_time']
