# Generated by Django 3.2.5 on 2021-08-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='物品名称', max_length=255, verbose_name='物品名称')),
                ('location', models.CharField(help_text='储藏位置', max_length=255, verbose_name='储藏位置')),
                ('img', models.ImageField(help_text='图片', upload_to='', verbose_name='图片')),
                ('remark', models.TextField(blank=True, help_text='备注', max_length=500, null=True, verbose_name='备注')),
                ('mfg', models.DateField(blank=True, help_text='生产日期', null=True, verbose_name='生产日期')),
                ('exp', models.DateField(blank=True, help_text='有效期', null=True, verbose_name='有效期')),
                ('duration', models.IntegerField(blank=True, help_text='有效天数', null=True, verbose_name='有效天数')),
                ('create_time', models.DateTimeField(auto_now=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, help_text='更新时间', verbose_name='更新时间')),
            ],
        ),
    ]
