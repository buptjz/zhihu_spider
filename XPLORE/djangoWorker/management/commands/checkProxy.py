#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from multiprocessing.dummy import Pool as ThreadPool
# import sys,os
# sys.path.append('../XPLORE')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'XPLORE.settings'
from djangoWorker.models import ProxyItem
import urllib2
import time


class Command(BaseCommand):
    "注册成为django一个命令，用python manage.py checkProxy 就可以执行，这个命令是检验抓取到的proxy是否有效，删除掉失效的proxy"
    def __test_one_proxy(self, ip, port='80', protocol='http', url="www.baidu.com"):
        proxy_url = protocol + '://' + ip + ':' + port
        proxy_support = urllib2.ProxyHandler({'http':proxy_url})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        request = urllib2.Request(url)
        request.add_header("Accept-Language", "zh-cn")
        request.add_header("Content-Type", "text/html; charset=gb2312")
        request.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")
        trycount = 1
        while trycount <= 2:
            try:
                f = opener.open(request, timeout=3.0)
                data = f.read()

                write_f = open(proxy_url + "write.html","w+")
                write_f.write(data)
                write_f.write("\n\n\n")
                write_f.close()
                if 'center' in data:
                    break
                else:
                    return False
            except:
                time.sleep(3)
                trycount = trycount + 1

        if trycount > 2:
            return False

        return True
    def __single_test(self,proxy):
        url = 'http://www.cpu.edu.cn/onlinecomment/survey/surveyOfOne.jsp?siteId=1&pageId=120&channelId=1'
        if self.__test_one_proxy(proxy.ip,proxy.port, proxy.protocol, url):
            print "%s:%s y" % (proxy.ip, proxy.port)
        else:
            print "%s:%s n" % (proxy.ip, proxy.port)
            proxy.delete()

    def handle(self, *args, **options):
        proxies = ProxyItem.objects.all()
        proxies[0].delete()
        pool = ThreadPool(100)
        results = pool.map(self.__single_test, proxies)
        pool.close()
        pool.join()
        # self.stdout.write('Successfully closed poll "%s"' % poll_id)