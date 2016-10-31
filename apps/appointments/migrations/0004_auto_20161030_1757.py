# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20161030_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('DONE', 'DONE'), ('PENDING', 'PENDING'), ('MISSED', 'MISSED')], default='PENDING', max_length=7),
        ),
    ]
