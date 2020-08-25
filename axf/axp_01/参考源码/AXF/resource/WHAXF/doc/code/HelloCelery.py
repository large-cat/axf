from time import sleep

from celery import Celery

app = Celery("HelloCelery", broker="redis://localhost:6379/0")


@app.task
def send_mail():

    sleep(5)

    print("邮件发送成功")


if __name__ == '__main__':
    # send_mail()
    send_mail.delay()

    print("双击666")