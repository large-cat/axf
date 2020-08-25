# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-03 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_mainshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=64)),
                ('trackid', models.IntegerField(default=0)),
                ('categoryid', models.IntegerField(default=0)),
                ('brandname', models.CharField(max_length=64)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.IntegerField(default=0)),
                ('productid1', models.IntegerField(default=0)),
                ('longname1', models.CharField(max_length=200)),
                ('price1', models.FloatField(default=0)),
                ('marketprice1', models.FloatField(default=0)),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.IntegerField(default=0)),
                ('productid2', models.IntegerField(default=0)),
                ('longname2', models.CharField(max_length=200)),
                ('price2', models.FloatField(default=0)),
                ('marketprice2', models.FloatField(default=0)),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.IntegerField(default=0)),
                ('productid3', models.IntegerField(default=0)),
                ('longname3', models.CharField(max_length=200)),
                ('price3', models.FloatField(default=0)),
                ('marketprice3', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]
