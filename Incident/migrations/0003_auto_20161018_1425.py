# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Incident', '0002_auto_20161011_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='incident_type',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='activation_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='deactivation_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
