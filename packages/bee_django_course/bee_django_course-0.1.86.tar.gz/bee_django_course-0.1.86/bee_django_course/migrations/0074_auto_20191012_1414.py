# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-10-12 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_course', '0073_auto_20190918_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='punch_duration',
            field=models.IntegerField(blank=True, help_text='\u7528\u4e8e\u8bfe\u7a0b\u6253\u5361\uff0c\u5982\u4e0d\u9700\u8981\u53ef\u4e0d\u586b\u5199', null=True, verbose_name='\u65f6\u957f'),
        ),
        migrations.AddField(
            model_name='course',
            name='punch_period',
            field=models.IntegerField(blank=True, choices=[(0, '\u65e0'), (1, '\u5929')], help_text='\u7528\u4e8e\u8bfe\u7a0b\u6253\u5361\uff0c\u5982\u4e0d\u9700\u8981\u53ef\u4e0d\u586b\u5199', null=True, verbose_name='\u5468\u671f'),
        ),
    ]
