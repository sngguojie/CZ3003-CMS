# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-23 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMSStatus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmsstatus',
            name='last_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
