# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 14:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IncidentCallReport', '0002_incidentcallreport_incident_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentcallreport',
            name='Incident_type',
        ),
    ]