# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-12 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentCallReport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentcallreport',
            name='report_id',
        ),
        migrations.AddField(
            model_name='incidentcallreport',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
