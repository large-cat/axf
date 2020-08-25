# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from AXP.tool.tools import *
from AXP.models import MainWheel, MainNav, Mustbuy, Mainshop, Food_type, Goods, AXFUser, Order_cart, Order_record
from axp_01.settings import STATIC_URL_PREFIX
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from json import loads


import uuid


def hello(request):
    return HttpResponse('hello')


# @cache_page(60*2)
def home(request):

    # time.sleep(5)
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    mustbuy = Mustbuy.objects.all()

    main_shop = Mainshop.objects.all()

    data = {
        "main_wheels": main_wheels,
        "main_navs": main_navs,
        "mustbuy": mustbuy,
        "title": "首页",
        "shop_container": main_shop[0],
        "fieldset": main_shop[1:3],
        "main_shop3_7": main_shop[3:7],
        "main_shop7_12": main_shop[7:9],
    }

    print (main_wheels[0].img)

    return render(request, 'axp/home.html', context=data)


# @cache_page(60 * 3)
def market(request, typeid, childtypeid, sort_num):

    # 获取数据
    goods = Goods.objects.all()

    food_types = Food_type.objects.all()

    # 排除空数据
    typeid_no_empty = int(typeid)

    childtypeid_no_empty = int(childtypeid)

    if not typeid_no_empty:
        typeid = food_types[0].typeid

    goods = goods.filter(categoryid=typeid)

    if childtypeid_no_empty:
        goods = goods.filter(childcid=childtypeid)

    # 数据排序
    sort_num = int(sort_num)

    if sort_num == ALL_TOTAL:
        pass

    elif sort_num == ORDER_BY_PRICE_UP:
        goods = goods.order_by('price')

    elif sort_num == ORDER_BY_PRICE_DOWN:
        goods = goods.order_by('-price')

    elif sort_num == ORDER_BY_SALE_DOWN:
        goods = goods.order_by('-productnum')

    elif sort_num == ORDER_BY_SALE_UP:
        goods = goods.order_by('productnum')

    # 商品分类信息整理
    childtypes = [childtype.split(':') for childtype in food_types.filter(typeid=typeid)[0].childtypenames.split("#")]

    data = {
        'food_types': food_types,
        'typeid': int(typeid),
        'goods': goods,
        'title': 'market',
        'childtypes': childtypes,
        'childtypeid': childtypeid,
        'sort_rules': ORDER,
        'sort_num': int(sort_num),
    }

    return render(request, 'axp/market.html', context=data)


@login_confirm
@active_confirm
def cart(request):

    user_id = request.session.get('user_id')

    cart_order_list = Order_cart.objects.filter(user_id=user_id)

    for cart_order in cart_order_list:
        if cart_order.good_num == 0:
            cart_order.delete()

    cart_order_list = Order_cart.objects.filter(user_id=user_id)

    # for good in cart_order_list:
    #     good.good = Goods.objects.get(pk=good.good_id)

    data = {
        'cart_list': cart_order_list,
    }
    return render(request, 'axp/cart.html', context=data)


def mine(request):

    data = {
        'title': "我的",
        'is_login': None,
        'user': None,
    }

    user_id = request.session.get('user_id')

    if not user_id:
        data.update(is_login=False)

    else:
        user = AXFUser.objects.get(pk=user_id)

        if user.u_icon:
            user.u_icon = STATIC_URL_PREFIX + user.u_icon.url

        data.update(is_active=user.is_active)

        data.update(user=user)

        data.update(user_id=user_id)

        data.update(is_login=True)

    return render(request, 'axp/mine.html', context=data)


def register(request):

    if request.method == 'GET':
        data = {
            'title': "注册",
        }

        return render(request, 'user/register.html', context=data)

    elif request.method == 'POST':
        data = {}

        # 判断用户是否存在
        if not AXFUser.objects.filter(u_username=request.POST['name']):
            user = AXFUser()

            user.u_username = request.POST['name']

            # 判断邮箱是否上传
            if request.POST['email_add']:

                # 判断邮箱是否已存在
                if AXFUser.objects.filter(u_email=request.POST['email_add']):
                    data.update(anwser='邮箱已注册')

                    return render(request, 'user/register_error.html', context=data)

                user.u_email = request.POST['email_add']

            user.u_password = make_password(request.POST['password'])

            # 判断是否上传头像
            if request.FILES.get('icon'):
                user.u_icon = request.FILES.get('icon')

            # 注册成功，保持用户信息
            user.save()

            user_id = AXFUser.objects.get(u_username=user.u_username).id

            request.session['user_id'] = user_id

            return redirect(reverse('index:mine'))

        # 注册失败，返回错误信息
        data.update(anwser='用户已存在')

        return render(request, 'user/register_error.html', context=data)


def login(request):

    if request.method == "GET":
        data = {
            'title': "登录",
        }

        return render(request, 'user/login.html', context=data)

    elif request.method == "POST":
        data = {}

        s_user = AXFUser.objects.filter(u_username=request.POST['name'])

        if not s_user:
            data.update(anwser='用户不存在')

            data.update(title='登录错误')

            return render(request, 'user/login_error.html', context=data)

        else:
            if check_password(request.POST['password'], s_user[0].u_password):
                # 登录成功
                user_id = AXFUser.objects.get(u_username=request.POST.get('name')).id

                request.session['user_id'] = user_id

                return redirect(reverse("index:mine"))

            else:
                data.update(anwser='密码错误')

                data.update(title='登录错误')

                return render(request, 'user/login_error.html', context=data)


def check_user(request):

    print (1)

    users = AXFUser.objects.all()

    data = {
        'status': HTTP_USER_EXIST,
        'msg': USER_CANT_USED,
    }

    print (request.GET)

    # 检查输入的用户名是为已存在的用户名或者邮箱
    if request.GET['username']:
        if not users.filter(u_username=str_hash(request.GET['username'])):

            if not users.filter(u_email=request.GET['username']):

                data['status'] = HTTP_USER_NOT_EXIST

                data['msg'] = USER_CAN_USED

    print (data)

    return JsonResponse(data=data)


@login_confirm
def login_out(request):

    request.session.flush()

    response = redirect(reverse('index:mine'))

    response.delete_cookie('sessionid')

    return response


# 转到激活页面
@login_confirm
def active(request):

    user_id = request.session['user_id']
    user = AXFUser.objects.get(pk=user_id)
    username = user.u_username
    data = {
        'username': username,
        'not_have_email': user.u_email is None,
        'msg': None,
    }
    if not user.is_active:
        # 判断是否为提交激活请求
        if request.method == "POST":
            if request.POST.get('email_add'):

                # 将用户上传的邮件地址保存
                email = request.POST.get('email_add')
                if not AXFUser.objects.filter(u_email=email).exists():
                    user.u_email = email
                    user.save()
                else:
                    data['msg'] = '邮箱已存在请重新激活'
                    return render(request, 'user/active.html', context=data)

            user_uuid = uuid.uuid4().hex

            cache.set(user_uuid, user.id, timeout=60*60*24)

            send_email(user.u_username, user.u_email, user_uuid)

            return redirect(reverse('index:do_active'))

        return render(request, 'user/active.html', context=data)
    else:
        return HttpResponse("该账户已激活")


def do_active(request):
    if request.GET:
        user_uuid = request.GET.get('u_token')
        # print (user_uuid)
        user_id = cache.get(user_uuid)
        if user_id:
            # print (user_id)
            user = AXFUser.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            cache.delete(user_uuid)
            return render(request, 'user/active_done.html')
        else:
            return render(request, 'user/active_error.html')
    return render(request, 'user/do_active.html')


@login_confirm
@active_confirm
def order_deal(request):
    data = {
        'status': HTTP_USER_EXIST,
        'msg': 'none',
    }
    user_id = request.session['user_id']
    if request.is_ajax():
        if request.method == 'POST':
            # print (request.POST)

            data_post = json.loads(request.body.decode())

            # print (data_post)

            operation = data_post['operation']

            # print (operation)
            # del comonds['operation']

            if operation == 'add':
                for add_good in data_post['data'].items():
                    # if add_good[1] == 'add':
                    #     continue

                    record_id = add_good[0]
                    num = int(add_good[1])
                    if num < 1:
                        continue
                    order_record = Order_cart.objects.filter(good_id=record_id).filter(user_id=user_id)
                    if order_record.exists():
                        order_record[0].good_num = order_record[0].good_num + num
                        order_record[0].save()
                    else:
                        order_record = Order_cart()
                        order_record.user_id = AXFUser.objects.get(pk=user_id)
                        order_record.good_id = Goods.objects.get(pk=record_id)
                        order_record.good_num = num
                        order_record.save()

                    data['status'] = HTTP_USER_EXIST
                    data['msg'] = 'success'

            elif operation == 'update':
                good = data_post['data'].items()

                record_id = int(good[0][0])

                good_num = int(good[0][1])

                print (record_id)

                print(good_num)

                order_record = Order_cart.objects.filter(pk=record_id).filter(user_id=user_id)

                if order_record.exists():
                    order_record = order_record[0]

                    order_record.good_num = good_num

                    order_record.save()

                    data['msg'] = 'success'

            elif operation == 'delete':
                delete_list_id = [int(record_id) for record_id in data_post['data']]

                if delete_list_id:
                    print(delete_list_id)

                    for record_id in delete_list_id:
                        record = Order_cart.objects.filter(pk=record_id).filter(user_id=user_id)

                        if record.exists():
                            record.delete()

                    data['msg'] = 'success'

        return JsonResponse(data=data)


@login_confirm
@active_confirm
def pay(request):

    data = {'status': HTTP_USER_EXIST, 'msg': 'none'}
    user_id = request.session['user_id']

    # 判断请求方式
    if request.method == "POST":
        if request.is_ajax():

            # 获取数据并将数据反序列化
            data_post = json.loads(request.body.decode())

            operation = data_post['operation']

            if operation == "pay":
                if data_post['data']:
                    order_list = [[int(order_id), int(num)] for order_id, num in data_post['data']]

                    # 将订单转存到订单记录中，并删除购物车的记录
                    order_num = uuid.uuid4().hex
                    for order in order_list:

                        order_id = order[0]
                        good_num = order[1]
                        record = Order_cart.objects.filter(pk=order_id)[0]
                        good_id = record.good_id.id
                        pay_record = Order_record()
                        pay_record.user_id = AXFUser.objects.get(pk=user_id)
                        pay_record.good_id = Goods.objects.get(pk=good_id)
                        pay_record.good_num = good_num
                        pay_record.is_paid = 0
                        pay_record.order_num = order_num
                        pay_record.save()
                        record.delete()

                    # print (order_list)
                    data['msg'] = 'success'
                    data['order_num'] = order_num
                    return JsonResponse(data=data)
                return redirect(reverse('index:cart'))
    if request.method == "GET":
        order_num = request.GET.get('order_num')
        order_list = Order_record.objects.filter(user_id=user_id).filter(order_num=order_num)
        total_sum = 0

        for order_record in order_list:
            total_sum += order_record.good_id.price * order_record.good_num

        data['total_sum'] = total_sum
        data['order_list'] = order_list
        return render(request, 'axp/pay.html', context=data)
    # print(request.POST)
    print ('pay')
    return HttpResponse('pay')


@login_confirm
@active_confirm
def order_inquiry(request):

    user_id = request.session['user_id']
    data = {'status': HTTP_USER_EXIST, 'msg': 'none'}
    if request.method == "GET":
        method = request.GET.get('method')

        if method == 'pending_payment':
            order_num_list = Order_record.objects.filter(user_id=user_id)\
                .values('order_num').distinct().order_by('order_num')

            data['pending_payment_order_list'] = []
            for order_num in order_num_list:
                order_num = list(order_num.values())[0]
                pending_payment_order = [order_num, []]

                order_list = Order_record.objects.filter(order_num=order_num)

                total_sum = 0
                for record in order_list:
                    total_sum += record.good_id.price * record.good_num
                pending_payment_order.append(total_sum)

                for record in order_list[0:3]:
                    good_name = record.good_id
                    pending_payment_order[1].append(good_name)
                data['pending_payment_order_list'].append(pending_payment_order)
                print (data['pending_payment_order_list'])
            return render(request, 'axp/order_inquiry.html', context=data)

        elif method == 'to_be_received':
            pass

    return HttpResponse('success')
