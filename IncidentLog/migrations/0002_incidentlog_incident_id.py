# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-08 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Incident', '__first__'),
        ('IncidentLog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentlog',
            name='incident_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incident.Incident'),
        ),
    ]
