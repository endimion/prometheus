# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 11:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20151215_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='department_addressed',
        ),
    ]
