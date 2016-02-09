# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20160206_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ansible_lsb', models.CharField(max_length=200)),
                ('ansible_memtotal_mb', models.PositiveIntegerField(default=None)),
                ('ansible_disktotal_size', models.PositiveIntegerField(default=None)),
                ('ansible_ipv4_address', models.GenericIPAddressField(default=None)),
                ('ansible_arch', models.CharField(max_length=200)),
                ('ansible_processor_cores', models.PositiveSmallIntegerField(default=None)),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.Host')),
            ],
            options={
                'verbose_name': 'Facts',
                'verbose_name_plural': 'Facts',
            },
        ),
    ]
