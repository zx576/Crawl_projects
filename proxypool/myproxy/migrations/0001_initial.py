# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=50, verbose_name='IP地址')),
                ('resourse', models.CharField(max_length=50, verbose_name='来源')),
                ('status', models.CharField(choices=[('V', 'VALID'), ('I', 'INVALID')], max_length=10, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
    ]
