# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-06 08:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_bpp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pembayaran',
            old_name='tangga_pembayaran',
            new_name='tanggal_pembayaran',
        ),
    ]
