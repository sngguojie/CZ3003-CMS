# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentCallReport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentcallreport',
            name='incident_id',
            field=models.IntegerField(default=0, help_text='Incident Id to link to'),
            preserve_default=False,
        ),
    ]