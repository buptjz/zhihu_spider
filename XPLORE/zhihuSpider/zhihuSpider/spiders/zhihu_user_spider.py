# -*- coding:utf-8 -*-

import urllib
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from djangoWorker.models import ZhihuQuestion,ZhihuUser,ZhihuAnswer

import json
from urllib import urlencode
from datetime import datetime
from django.utils import timezone
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

host='http://www.zhihu.com'

class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihu_user'
    allowed_domains = ['zhihu.com']
    #使用rule时候，不要定义parse方法
    rules = (
    )

    def __init__(self,  *a,  **kwargs):
        super(ZhihuLoginSpider, self).__init__(*a, **kwargs)
        # self.user_names = []

    def start_requests(self):
        email = "88888888a@qq.com" #raw_input("email>")
        password = "88888888a" #raw_input("password>")
        return [FormRequest(
            "http://www.zhihu.com/login",
            formdata = {'email':email,
                        'password':password
            },
            callback = self.after_login
        )]

    def after_login(self, response):
        users = ZhihuUser.objects.order_by('-follower_num')
        print "Total feeds users :" ,len(users)
        self.all_user_names = [u.username for u in users]
        self.feed_user_names = [u.username for u in users[:10]]

        for user in users[:10]:
            print "===========[Base] user:" + user.nickname

            url = host + "/people/" + user.username + "/about"
            # print url
            yield Request(url,callback=self.parse_user)

    def parse_item(self, response):
        selector = Selector(response)
        for link in selector.xpath('//div[@id="suggest-list-wrap"]/ul/li/div/a/@href').extract():
            #link  ===> /people/javachen
            yield Request(host+link+"/about", callback=self.parse_user)

    def parse_user(self, response):
        selector = Selector(response)
        # user_obj = ZhihuSpiderUserItem()
        name = response.url.split('/')[-2]

        if name in self.all_user_names and name not in self.feed_user_names:
            return

        if name not in self.all_user_names:
            self.all_user_names.append(name)

        user_obj, created = ZhihuUser.objects.update_or_create(username=name)
        user_obj.update_time = timezone.now()
        user_obj.url= response.url
        user_obj.nickname = ''.join(selector.xpath("//div[@class='title-section ellipsis']/a[@class='name']/text()").extract())
        user_obj.location = ''.join(selector.xpath("//span[@class='location item']/@title").extract())
        user_obj.industry = ''.join(selector.xpath("//span[@class='business item']/@title").extract())
        user_obj.sex = ''.join(selector.xpath('//div[@class="item editable-group"]/span/span[@class="item"]/i/@class').extract()).replace("zg-icon gender ","")
        user_obj.description = ''.join(selector.xpath("//span[@class='description unfold-item']/span/text()").extract()).strip().replace("\n",'')
        user_obj.view_num = int(''.join(selector.xpath("//span[@class='zg-gray-normal']/strong/text()").extract()))
        # print(user_obj.update_time)


        user_obj.jobs = ""
        job_nodes = selector.xpath('//div[@class="zm-profile-module zg-clear"][1]/div/ul[@class="zm-profile-details-items"]/li')
        for node in job_nodes:
            company = ''.join(node.xpath('@data-title').extract())
            title = ''.join(node.xpath('@data-sub-title').extract())
            user_obj.jobs += company + ":" + title + "|"

        user_obj.educations = ""
        edu_nodes = selector.xpath('//div[@class="zm-profile-module zg-clear"][3]/div/ul[@class="zm-profile-details-items"]/li')
        for node in edu_nodes:
            school = ''.join(node.xpath('@data-title').extract())
            major = ''.join(node.xpath('@data-sub-title').extract())
            user_obj.educations += school + ":" + major + "|"

        user_obj.sinaweibo =''
        user_obj.tencentweibo =''
        for node in selector.xpath("//a[@class='zm-profile-header-user-weibo']/@href").extract():
            if node.startswith('http://weibo.com'):
                user_obj.sinaweibo = node
            elif node.startswith('http://t.qq.com'):
                user_obj.tencentweibo = node

        statistics = selector.xpath("//a[@class='item']/strong/text()").extract()
        statistics = [int(i) for i in statistics]
        followee_num =user_obj.followee_num = statistics[0]
        follower_num = user_obj.follower_num= statistics[1]

        statistics = selector.xpath("//div[@class='zm-profile-module-desc']/span/strong/text()").extract()
        if len(statistics) ==4:
            user_obj.agree_num = statistics[0]
            user_obj.thank_num = statistics[1]
            user_obj.fav_num = statistics[2]
            user_obj.share_num = statistics[3]

        statistics = selector.xpath("//div[@class='profile-navbar clearfix']/a/span/text()").extract()
        if len(statistics) ==6:
            user_obj.ask_num = statistics[1]
            user_obj.answer_num = statistics[2]
            user_obj.post_num = statistics[3]
            user_obj.collection_num = statistics[4]
            user_obj.log_num = statistics[5]

        _xsrf = ''.join(selector.xpath('//input[@name="_xsrf"]/@value').extract())
        hash_id = ''.join(selector.xpath('//div[@class="zm-profile-header-op-btns clearfix"]/button/@data-id').extract())

        user_obj.save()
        # yield user_obj
        # self.user_names.append(user_obj.username)
        print 'NEW:%s' % user_obj.username

        #只抓取种子用户的相关用户
        if name in self.feed_user_names:
            num = int(followee_num) if followee_num else 0
            page_num = num/20
            page_num += 1 if num%20 else 0
            for i in xrange(page_num):
                params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":i*20})
                payload = {"method":"next", "params": params, "_xsrf":_xsrf}
                yield Request("http://www.zhihu.com/node/ProfileFolloweesListV2?"+urlencode(payload), callback=self.parse_follow_url)

            num = int(follower_num) if follower_num else 0
            page_num = num/20
            page_num += 1 if num%20 else 0
            for i in xrange(page_num):
                params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":i*20})
                payload = {"method":"next", "params": params, "_xsrf":_xsrf}
                yield Request("http://www.zhihu.com/node/ProfileFollowersListV2?"+urlencode(payload), callback=self.parse_follow_url)

    def parse_follow_url(self, response):
        selector = Selector(response)

        for link in selector.xpath('//div[@class="zm-list-content-medium"]/h2/a/@href').extract():
            #link  ===> http://www.zhihu.com/people/peng-leslie-97
            username_tmp = link.split('/')[-1]
            # if username_tmp in self.user_names:
            #     print 'GET:' + '%s' % username_tmp
            #     continue

            yield Request(link+"/about", callback=self.parse_user)