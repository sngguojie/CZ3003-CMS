# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-11 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Incident', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='activation_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='incident',
            name='deactivation_time',
            field=models.DateTimeField(),
        ),
    ]
