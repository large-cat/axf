import hashlib

from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=0)

    class Meta:
        abstract = True


"""
 axf_wheel(img,name,trackid)
"""
class MainWheel(Main):

    class Meta:
        db_table = "axf_wheel"

"""
axf_nav(img,name,trackid)
"""
class MainNav(Main):

    class Meta:
        db_table = 'axf_nav'


"""
axf_mustbuy(img,name,trackid)
"""
class MainMustBuy(Main):

    class Meta:
        db_table = "axf_mustbuy"


"""
axf_shop(img,name,trackid)
"""
class MainShop(Main):

    class Meta:
        db_table = "axf_shop"

"""
 axf_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,marketprice1,
 img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3)
  values("21782","优选水果","http://img01.bqstatic.com//upload/activity/2017031018205492.jpg@90Q.jpg","103532",
  "爱鲜蜂","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164159_996462.jpg@200w_200h_90Q","103533",
  "118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8","http://img01.bqstatic.com/upload/goods/201/611/1617/20161116173544_219028.jpg@200w_200h_90Q",
  "103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q",
  "103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");

"""
class MainShow(Main):

    categoryid = models.IntegerField(default=0)
    brandname = models.CharField(max_length=64)

    img1 = models.CharField(max_length=200)
    childcid1 = models.IntegerField(default=0)
    productid1 = models.IntegerField(default=0)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.IntegerField(default=0)
    productid2 = models.IntegerField(default=0)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.IntegerField(default=0)
    productid3 = models.IntegerField(default=0)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = "axf_mainshow"


"""
 axf_foodtypes(typeid,typename,childtypenames,typesort)
"""
class FoodType(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=16)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_foodtypes"


"""
insert into axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,
categoryid,childcid,childcidname,dealerid,storenums,productnum) values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q",
"","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
"""
class Goods(models.Model):
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=False)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_goods"


class UserModel(models.Model):

    u_name = models.CharField(max_length=32, unique=True)

    _password = models.CharField(max_length=256, null=True,db_column='u_password')

    u_email = models.CharField(max_length=64, unique=True)

    u_icon = models.ImageField(upload_to='icons')

    is_active = models.BooleanField(default=False)

    is_delete = models.BooleanField(default=False)

    @property
    def u_password(self):
        return self._password

    @u_password.setter
    def u_password(self, pwd):
        self._password = make_password(pwd)

    def check_password(self, pwd):

        return check_password(pwd, self._password)

    # def set_password(self, password):
    #
    #     # md5 = hashlib.md5()
    #     #
    #     # md5.update(password.encode("utf-8"))
    #     #
    #     # password = md5.hexdigest()
    #
    #     password = make_password(password)
    #
    #     self.u_password = password
    #
    # def check_password(self, password):
    #     # md5 = hashlib.md5()
    #     #
    #     # md5.update(password.encode("utf-8"))
    #     #
    #     # password = md5.hexdigest()
    #
    #     # return self.u_password == password
    #     return check_password(password, self.u_password)


    class Meta:

        db_table = "axf_user"


class Cart(models.Model):

    c_goods = models.ForeignKey(Goods)

    c_user = models.ForeignKey(UserModel)

    is_select = models.BooleanField(default=True)

    c_goods_num = models.IntegerField(default=1)

    # 修改打印时的显示  python2 unicode
    # def __str__(self):
    #     return str(self.c_goods_num)

    class Meta:
        db_table = 'axf_cart'


class Order(models.Model):

    o_user = models.ForeignKey(UserModel)

    o_total_price = models.FloatField(default=0)
    """
        需要建立映射
            0 代表已下单未付款
            1 已下单已付款未发货
            2 已下单已付款已发货未收货
            3 ...
    """
    o_status = models.IntegerField(default=0)

    o_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "axf_order"


class OrderGoods(models.Model):

    o_order = models.ForeignKey(Order)

    o_goods = models.ForeignKey(Goods)

    o_goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_ordergoods"
