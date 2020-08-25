import random
import uuid
from time import sleep

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel, Cart, Order, \
    OrderGoods
from App.tasks import send_mail_asy, send_mail_celery
from App.viewhelper import get_user, send_mail_to, get_user_by_id, get_total_price

ALL_TYPE = "0"

TOTAL_RULE = "0"

PRICE_UP = "1"

PRICE_DOWN = "2"


def home(request):

    # 元信息
    ip = request.META.get('REMOTE_ADDR')

    result = cache.get(ip+'home')

    if result:
        print('从缓存中加载')
        return HttpResponse(result)

    wheels = MainWheel.objects.all()

    navs = MainNav.objects.all()

    mustbuys = MainMustBuy.objects.all()

    shops = MainShop.objects.all()

    shop0 = shops[0:1]

    shop1_3 = shops[1:3]

    shop3_7 = shops[3:7]

    shop7_11 = shops[7:11]

    mainshows = MainShow.objects.all()

    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "shop0": shop0,
        "shop1_3": shop1_3,
        "shop3_7": shop3_7,
        "shop7_11": shop7_11,
        "mainshows": mainshows
    }

    sleep(4)

    # 添加到缓存中
    temp = loader.get_template('home/home.html')
    # 渲染
    result = temp.render(context=data)

    print(result)

    cache.set(ip+'home', result)

    return HttpResponse(result)

    # return render(request, 'home/home.html', context=data)


def market(request):

    return redirect(reverse("axf:marketWithParams", kwargs={"typeid": "104749", "cid":"0", "sort_rule": "0"}))


@cache_page(120)
def marketWithParams(request, typeid, cid, sort_rule):

    # sleep(3)

    foodtypes = FoodType.objects.all()

    if cid == ALL_TYPE:
        goodsList = Goods.objects.filter(categoryid=typeid)
    else:
        goodsList = Goods.objects.filter(categoryid=typeid).filter(childcid=cid)

    """
        全部分类:0#进口水果:110#国产水果:120
        
        全部分类，进口水果，国产水果
        数字是它名字的标识
        
        for in 迭代显示
            可迭代元素
        切割
            # 
        [全部分类:0, 进口水果:110, 国产水果:120]
        
        切割
            :
        [[全部分类, 0], [进口水果, 110], [国产水果, 120]]
    """
    foodtype = FoodType.objects.get(typeid=typeid)

    childtypenames = foodtype.childtypenames

    childtypename_list = childtypenames.split("#")

    child_type_name_list = []

    for childtypename in childtypename_list:
        child_type_name_list.append(childtypename.split(":"))

    print(child_type_name_list)

    """
        综合排序
            就是对筛选结果进行一个order_by
            
        服务器能接收对应的字段 （排序字段）
        客户端发送排序字段
            两端有一个约定
                0 综合排序
                1 价格升序
                2 价格降序
                3 ...
                4 ...
            简历
                和前端定制接口字段
    """
    if sort_rule == TOTAL_RULE:
        pass
    elif sort_rule == PRICE_UP:
        goodsList = goodsList.order_by("price")
    elif sort_rule == PRICE_DOWN:
        goodsList = goodsList.order_by("-price")

    data = {
        "title": "闪购",
        "foodtypes": foodtypes,
        "goodsList": goodsList,
        "typeid": int(typeid),
        "child_type_name_list": child_type_name_list,
        "cid": cid,
        "sort_rule": sort_rule,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):

    user_id = request.session.get('user_id')

    user = get_user_by_id(user_id)

    if not user:
        return redirect(reverse("axf:user_login"))

    # cart_set 外键对应的隐形属性， 本质上也是一个Manager对象
    carts = user.cart_set.all()

    print(carts)

    all_select = True

    if carts.filter(is_select=False).exists():
        all_select = False

    total_price = get_total_price(user_id)

    # for cart_obj in carts:
    #     if cart_obj.is_select:
    #         total_price += cart_obj.c_goods_num * cart_obj.c_goods.price

    data = {
        "title": "购物车",
        "carts": carts,
        "all_select": all_select,
        "total_price":total_price
    }

    return render(request, 'cart/cart.html', context=data)


def mine(request):

    user_id = request.session.get('user_id')

    data = {
        "title": "我的",
        "is_login": False
    }

    if user_id:
        user = UserModel.objects.get(pk=user_id)

        not_payed = user.order_set.filter(o_status=0).count()
        data["not_payed"] = not_payed

        payed = user.order_set.filter(o_status=1).count()
        data["payed"] = payed
        data['is_login'] = True
        data["username"] = user.u_name
        data["icon"] = "/static/upload/" + user.u_icon.url

    return render(request, 'mine/mine.html', context=data)


def add_to_cart(request):

    user_id = request.session.get('user_id')

    user = get_user_by_id(user_id)

    data = {}

    if not user:
        # 重定向
        data['status'] = "902"
        data['msg'] = "not login"
    else:
        goods_id = request.GET.get("goodsid")

        carts = Cart.objects.filter(c_user=user).filter(c_goods_id=goods_id)

        if carts.exists():
            cart_obj = carts.first()
            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
            cart_obj.save()
        else:
            cart_obj = Cart()
            cart_obj.c_goods_id = goods_id
            cart_obj.c_user_id = user_id
            cart_obj.save()

        data['msg'] = 'add success'
        data['status'] = "201"
        data['cart_goods_num'] = cart_obj.c_goods_num

    return JsonResponse(data)


class UserRegisterView(View):

    def get(self, request):

        return render(request, 'user/user_register.html')

    def post(self, request):

        u_username = request.POST.get("u_username")

        u_email = request.POST.get("u_email")

        u_password = request.POST.get("u_password")

        u_icon = request.FILES.get("u_icon")

        user = UserModel()

        user.u_name = u_username

        user.u_password = u_password

        user.u_email = u_email

        user.u_icon = u_icon

        user.save()
        # 生成token  时间 + ip + 随机数
        # uuid
        token = str(uuid.uuid4())

        cache.set(token, user.id, timeout= 60 * 60 * 24)

        active_url = "http://localhost:8002/axf/active/?token=" + token

        send_mail_to(u_username, active_url, u_email)

        # request.session["user_id"] = user.id

        response = redirect(reverse("axf:user_login"))

        return response


class UserLoginView(TemplateView):

    template_name = 'user/user_login.html'

    def get(self, request, *args, **kwargs):

        msg = request.session.get('login_msg')

        data = {}

        if msg:
            data['msg'] = msg
            del request.session['login_msg']

        return render(request, self.template_name, context=data)

    def post(self, request):

        username = request.POST.get("u_username")

        password = request.POST.get("u_password")

        user = get_user(username)

        if user:
            if user.check_password(password):
                # 用户名和密码都对了，跳转到个人中心

                if user.is_active:

                    request.session['user_id'] = user.id
                    return redirect(reverse("axf:mine"))
                else:
                    # 用户未激活的
                    request.session['login_msg'] = "用户未激活"
                    return redirect(reverse("axf:user_login"))
            else:
                # 密码错误
                request.session['login_msg'] = "密码错误"
                return redirect(reverse("axf:user_login"))
        #    用户名不存在
        request.session['login_msg'] = "用户不存在"
        return redirect(reverse("axf:user_login"))


def logout(request):

    # session cookie 一起清除
    request.session.flush()

    return redirect(reverse('axf:mine'))


def check_user(request):
    username = request.GET.get("username")

    user = get_user(username)

    data = {
        "msg": '<span style="color: green">用户名可用</span>'
    }

    if user:
        data["status"] = "901"
        data["msg"] = '<span style="color: red">用户名已存在</span>'
    else:
        data["status"] = "200"
    return JsonResponse(data)


def active(request):

    token = request.GET.get('token')

    user_id = cache.get(token)

    if user_id:

        cache.delete(token)

        user = UserModel.objects.get(pk=user_id)

        user.is_active = True

        user.save()

        return HttpResponse("激活成功")
    else:
        return HttpResponse("激活信息过期，请重新申请激活邮件")


# 如果让你自行添加校验
# 判断用户登录
# 判断购物车是否存在
def change_cart_status(request):

    cart_id = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.is_select = not cart_obj.is_select

    cart_obj.save()

    all_select = True

    if cart_obj.is_select:
        user_id = request.session.get("user_id")
        carts = Cart.objects.filter(c_user_id=user_id).filter(is_select=False)
        if carts.exists():
            all_select = False

    data = {
        "msg": "ok",
        "status": "200",
        "is_select": cart_obj.is_select,
        "all_select": all_select,
        "total_price": get_total_price(request.session.get("user_id"))
    }

    return JsonResponse(data)


def change_cart_list_status(request):

    action = request.GET.get("action")

    cart_list = request.GET.get("cartlist")

    # print(action)
    #
    # print(cart_list)

    carts = cart_list.split("#")

    if action == "select":
        # 选出主键在已有列表的所有元素

        # Cart.objects.filter(pk__in=carts).update({"is_select": True})

        for cart_id in carts:
            cart_obj = Cart.objects.get(pk=cart_id)
            cart_obj.is_select = True
            cart_obj.save()

    elif action == "unselect":
        for cart_id in carts:
            cart_obj = Cart.objects.get(pk=cart_id)
            cart_obj.is_select = False
            cart_obj.save()

    data = {
        "msg": "ok",
        "status": "200",
        "action": action,
        "total_price": get_total_price(request.session.get("user_id"))
    }

    return JsonResponse(data)


def sub_to_cart(request):

    cartid = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        "status": "200",
        "msg": "ok",

    }

    if cart_obj.c_goods_num == 1:
        cart_obj.delete()
        data["c_goods_num"] = 0
    else:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data["c_goods_num"] = cart_obj.c_goods_num

    data["total_price"] = get_total_price(request.session.get("user_id"))

    return JsonResponse(data)


def make_order(request):

    cartlist = request.GET.get("cartlist")

    cart_list = cartlist.split("#")

    order = Order()

    user_id = request.session.get('user_id')

    order.o_user_id = user_id

    order.o_total_price = get_total_price(user_id)

    order.save()

    for cart_id in cart_list:

        ordergoods = OrderGoods()

        cart_obj = Cart.objects.get(pk=cart_id)

        ordergoods.o_goods_num = cart_obj.c_goods_num

        ordergoods.o_order_id = order.id

        ordergoods.o_goods_id = cart_obj.c_goods_id

        ordergoods.save()

        cart_obj.delete()


    data = {
        "msg": "ok",
        "orderid": order.id,
        "status": "200",
    }

    return JsonResponse(data)


#  在企业开发中，对一个数据的合法性和有效性 要添加各种判断
def order_detail(request):

    order_id = request.GET.get("order_id")

    order = Order.objects.get(pk=order_id)

    data = {
        "title": "订单详情",
        "order": order
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list(request):

    user_id = request.session.get('user_id')

    user= get_user_by_id(user_id)

    orders = user.order_set.filter(o_status=0)

    data = {
        "title": "订单列表",
        "orders": orders
    }

    return render(request, 'order/order_list.html', context=data)


def alipay(request):

    # 伪支付
    order_id = request.GET.get("orderid")

    order = Order.objects.get(pk=order_id)
    # 开发中 最好写成常量
    order.o_status = 1

    order.save()

    data = {
        "msg": "ok",
        "status": "200"
    }

    return JsonResponse(data)


def get_phone(request):

    # num = random.randrange(100)
    #
    # if num > 98:
    #     return HttpResponse("恭喜你免费抽到一个小米8")
    # else:
    #     return HttpResponse("正在排队")

    items = []

    for i in range(10):
        items.append(i)

    items.append("10&black=true")

    data = {
        "items": items
    }

    return render(request, 'teach.html', context=data)


def get_article(request):

    resultid = send_mail_celery.delay("rongjiawei1204@163.com")

    return HttpResponse("页面数据" + request.GET.get("page"))