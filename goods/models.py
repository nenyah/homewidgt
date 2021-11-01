from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from wx.models import WxUser


class Goods(models.Model):
    # 基本信息
    name = models.CharField(max_length=255, verbose_name=_('物品名称'), help_text=_('物品名称'))
    # address = models.CharField(max_length=255, verbose_name=_('储藏地址'), help_text=_('储藏地址'), default='')
    # floor = models.CharField(max_length=255, verbose_name=_('储藏楼层'), help_text=_('储藏楼层'), default='')
    # room = models.CharField(max_length=255, verbose_name=_('储藏房间'), help_text=_('储藏房间'), default='')
    location = models.CharField(max_length=255, verbose_name=_('储藏位置'), help_text=_('填写格式： 二楼-衣柜，方便后期优化'))
    img = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name=_('图片'), help_text=_('图片'))
    remark = models.TextField(verbose_name=_('备注'), help_text=_('备注'), max_length=500, null=True, blank=True)

    # 有效期
    mfg = models.DateField(verbose_name=_('生产日期'), help_text=_('生产日期'), null=True, blank=True)
    exp = models.DateField(verbose_name=_('有效期'), help_text=_('有效期'), null=True, blank=True)

    # 创建信息
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'), help_text=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'), help_text=_('更新时间'))
    create_by = models.ForeignKey(WxUser, on_delete=models.CASCADE, verbose_name=_('创建人'), help_text=_('创建人'),
                                  default=1)

    class Meta:
        verbose_name = '物品'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.name
