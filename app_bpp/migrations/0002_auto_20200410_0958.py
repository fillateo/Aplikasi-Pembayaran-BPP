# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-10 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_bpp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pembayaran',
            name='jurusan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_bpp.Jurusan'),
        ),
        migrations.AlterField(
            model_name='pembayaran',
            name='kelas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_bpp.Kelas'),
        ),
    ]
