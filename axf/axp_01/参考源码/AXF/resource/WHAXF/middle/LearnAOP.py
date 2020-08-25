import random

import time
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HelloMiddle(MiddlewareMixin):

    def process_request(self, request):

        print(request.path)

        print(request.META.get("REMOTE_ADDR"))

        # 黑白名单简单案例
        # if request.path == "/axf/getphone/":
        #     if request.META.get("REMOTE_ADDR") == "192.168.51.149":
        #         # return HttpResponse("恭喜免费获取到小米8")
        #         num = random.randrange(100)
        #         if num > 50:
        #             return HttpResponse("特殊手段抽取到小米8")


        ip = request.META.get("REMOTE_ADDR")

        black = cache.get('black', [])

        if ip in black:
            return HttpResponse("小爬虫，回家修炼两年再来")

        #  简单的给予 ip的反爬
        # if request.path == "/axf/getphone/":
        #
        #     result = cache.get(ip)
        #
        #     if result:
        #         return HttpResponse("每10秒只能访问一次")
        #     else:
        #         cache.set(ip, "Spider", 10)

        # 给予请求频率的反爬
        # key, value( default )
        history = cache.get(ip, [])

        # history不为空，   获取最后一个元素， 获取最后一次的请求时间   如果和当前时间比 时间差超过60
        while history and history[-1] <= time.time() - 60:
            history.pop()

        if (len(history) <= 10):
            # 可以请求，注意添加记录
            history.insert(0, time.time())
            cache.set(ip, history, 60)

        else:
            # 不可以请求
            return HttpResponse("小爬虫不要爬了，不得频率太高了")

        if request.path == "/axf/getarticle/":
            if request.GET.get("black"):
                black = cache.get('black',[])
                black.append(ip)
                cache.set('black',black, 60*60*24)
                return HttpResponse("小爬虫回家把，这不适合你")