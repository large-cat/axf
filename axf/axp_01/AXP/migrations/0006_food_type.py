# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-03-10 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AXP', '0005_mainshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.IntegerField(default=0)),
                ('typename', models.CharField(max_length=16)),
                ('childtypenames', models.CharField(max_length=128)),
                ('typesort', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'axf_foodtypes',
            },
        ),
    ]
