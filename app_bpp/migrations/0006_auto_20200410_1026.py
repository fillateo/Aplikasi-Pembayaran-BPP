# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-10 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bpp', '0005_auto_20200410_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pembayaran',
            name='id_siswa',
            field=models.IntegerField(),
        ),
    ]
