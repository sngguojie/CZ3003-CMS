# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-02 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentCallReport', '0002_remove_incidentcallreport_caller_nric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentcallreport',
            name='dateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]