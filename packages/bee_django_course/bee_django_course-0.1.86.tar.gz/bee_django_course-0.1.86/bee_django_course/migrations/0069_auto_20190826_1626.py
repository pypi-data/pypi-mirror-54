# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-08-26 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_course', '0068_course_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='template',
            field=models.CharField(blank=True, help_text='\u5728\u9879\u76ee\u4e2dcustom_user\u4e0b\u65b0\u5efa\u6a21\u7248\u6587\u4ef6custom_user_course_section_list_[template].html', max_length=180, null=True, verbose_name='\u6a21\u7248'),
        ),
    ]
