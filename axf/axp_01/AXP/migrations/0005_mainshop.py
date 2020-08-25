# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-03-09 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AXP', '0004_mustbuy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mainshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(db_column='img', max_length=255)),
                ('name', models.CharField(db_column='name', max_length=64)),
                ('trackid', models.IntegerField(db_column='trackid', default=1)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]
