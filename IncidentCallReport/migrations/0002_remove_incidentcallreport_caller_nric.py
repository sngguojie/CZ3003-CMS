# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-02 08:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentCallReport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentcallreport',
            name='caller_nric',
        ),
    ]