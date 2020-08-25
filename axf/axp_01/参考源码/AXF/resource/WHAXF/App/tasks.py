from time import sleep

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_asy(email):

    sleep(3)

    print("send mail", email)

    return "Hello"


@shared_task
def send_mail_celery(email):

    send_mail("Test", "Hello", "rongjiawei1204@163.com", [email])

