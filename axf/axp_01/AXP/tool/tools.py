# _*_coding=utf-8_*_
# ORDER_BY
import hashlib

from AXP.models import AXFUser
from axp_01.settings import EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SERVER_HOST, SERVER_PORT
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

ALL_TOTAL = 0
ORDER_BY_PRICE_UP = 1
ORDER_BY_PRICE_DOWN = 2
ORDER_BY_SALE_DOWN = 3
ORDER_BY_SALE_UP = 4

ORDER = [
    ('综合排序', 0),
    ('价格最低', 1),
    ('价格最高', 2),
    ('销量最高', 3),
    ('销量最低', 4),
]

# HTTP

HTTP_USER_EXIST = 902

HTTP_USER_NOT_EXIST = 200

USER_CAN_USED = 'user can used'

USER_CANT_USED = "user can't used"


# tools functions

# 将加密字段转为hash
def str_hash(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


# 给用户发送激活邮件
def send_email(username, email_add, user_uuid):

    subject = 'AXF Active'
    message = ''
    recipient_list = [email_add, ]
    active_url = 'http://{}:{}/index/do_active/?u_token={}'.format(SERVER_HOST, SERVER_PORT, user_uuid)
    data = {
        'username': username,
        'uuid': user_uuid,
        "active_url": active_url,
    }

    html_message = loader.get_template('user/active_email.html').render(data)

    send_mail(subject=subject, message=message, from_email=EMAIL_FROM, recipient_list=recipient_list,
              auth_user=EMAIL_HOST_USER, auth_password=EMAIL_HOST_PASSWORD,
              html_message=html_message)


def active_confirm(f):
    def wrapper(request, *args, **kwargs):

        user_id = request.session.get('user_id')
        user = AXFUser.objects.get(pk=user_id)

        if not user.is_active:
            if not request.is_ajax():
                return redirect(reverse('index:active'))
            else:
                return JsonResponse(data={'msg': '账户未激活', 'status': HTTP_USER_NOT_EXIST, })

        return f(request, *args, **kwargs)
    return wrapper


def login_confirm(f):
    def wrapper(request, *args, **kwargs):
        is_not_login = not request.session.get('user_id')

        if is_not_login:
            if not request.is_ajax():
                return redirect(reverse('index:login'))
            else:
                return JsonResponse(data={'msg': '未登录', 'status': HTTP_USER_NOT_EXIST, })

        return f(request, *args, **kwargs)
    return wrapper


