# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentLog', '0002_incidentlog_incident_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentlog',
            name='description',
        ),
        migrations.AlterField(
            model_name='incidentlog',
            name='incident_id',
            field=models.IntegerField(help_text='Incident Id this log is related to', null=True),
        ),
    ]
