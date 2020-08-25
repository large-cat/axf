# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=255, db_column='img')
    name = models.CharField(max_length=64, db_column='name')
    trackid = models.IntegerField(default=1, db_column='trackid')

    class Meta:
        abstract = True


class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'


class Mustbuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'


class Mainshop(Main):
    class Meta:
        db_table = 'axf_shop'


class Food_type(models.Model):
    """
        insert into axf_foodtypes(typeid,typename,childtypenames,typesort)
    """
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=16)
    childtypenames = models.CharField(max_length=128)
    typesort = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    """
        insert into axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,
    price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
    values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","",
    "乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);

    """
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=256)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=50)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=16)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=16)
    dealerid = models.CharField(max_length=10)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'
        # indexes = [
        #     models.Index(fields=['marketprice']),
        #     models.Index(fields=['childcid']),
        # ]


class AXFUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True, null=True)
    u_icon = models.ImageField(upload_to='icons/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'AXFUser'


class Order(models.Model):
    good_id = models.ForeignKey(Goods)
    user_id = models.ForeignKey(AXFUser)
    good_num = models.IntegerField(default=1)

    class Meta:
        abstract = True


class Order_cart(Order):
    pass

    class Meta:
        unique_together = ('good_id', 'user_id')
        db_table = 'Order_cart'


class Order_record(Order):
    is_paid = models.BooleanField(default=False)

    order_num = models.CharField(max_length=128)

    creat_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('good_id', 'user_id', 'order_num')
        db_table = 'Order_record'


