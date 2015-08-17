# -*- coding:utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from zhihuSpider.items import ZhihuSpiderQuestionItem
from djangoWorker.models import ZhihuQuestion,ZhihuUser,ZhihuAnswer

import sys,time

reload(sys)
sys.setdefaultencoding('utf-8')

host='http://www.zhihu.com'

class ZhihuLoginSpider(CrawlSpider):
    name = 'zhihu_ask'
    allowed_domains = ['zhihu.com']
    start_urls = []

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
        users = ZhihuUser.objects.all()
        for user in users:
            num = int(user.ask_num)
            page_num = num/20
            page_num += 1 if num%20 else 0
            for i in xrange(page_num):
                url=host+"/people/"+user.username + '/asks?page=%d' % (i+1)
                yield Request(url, callback=self.parse_ask)


    def parse_ask(self, response):
        selector = Selector(response)
        username = response.url.split('/')[-2]
        try:
            for record in selector.xpath(r"id('zh-profile-ask-list')/div"):
                url = host+record.xpath(r"div/h2/a/@href")[0].extract()
                if not "rf" in url:
                    yield Request(url, callback=self.parse_question)
        except Exception, e:
            open('error_pages/asks' + response.url.split('/')[-2]+'.html', 'w').write(response.body)
            print '='*10 + str(e)

    def format_time(self,the_time):
        '''输入时间格式 2014-06-30 19:28:27'''
        time_array = time.strptime(the_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array))
        return time_stamp


    def parse_question_log(self, response):
        '''问题页面没雨修改时间的信息，我们在log页面获取'''
        problem = Selector(response)
        page_id = int(response.url.split("/")[-2])
        question_obj, created = ZhihuQuestion.objects.update_or_create(page_id=page_id)
        times = problem.xpath('//time/text()').extract()
        if len(times) == 0:
            return
        question_obj.create_time = times[-1]
        question_obj.last_edit_time = times[0]
        question_obj.format_create_time = self.format_time(question_obj.create_time)
        question_obj.format_last_edit_time = self.format_time(question_obj.last_edit_time)
        question_obj.save()

    def parse_question(self, response):
        problem = Selector(response)
        if "rf" in response.url:
            return
        page_id = int(response.url.split("/")[-1])
        question_obj, created = ZhihuQuestion.objects.update_or_create(page_id=page_id)
        question_obj.page_id = response.url.split("/")[-1]
        question_obj.url = response.url
        question_obj.title = ''.join(problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract())
        question_obj.description = ''.join(problem.xpath('//div[@class="zm-editable-content"]/text()').extract())
        tags = problem.xpath('//a[@class="zm-item-tag"]/text()').extract()
        tags = [t.strip() for t in tags]
        question_obj.tags = ";".join(tags)

        question_obj.pinglun_num = 0
        question_obj.guanzhu_num = 0
        question_obj.answer_num = 0

        pinglun = ''.join(problem.xpath(r'//div[@id="zh-question-meta-wrap"]//a[@name="addcomment"]/text()').extract())
        if len(pinglun.split(" ")) == 2:
            question_obj.pinglun_num = int(pinglun.split(" ")[0])

        guanzhu_num = ''.join(problem.xpath('//div[@class="zh-question-followers-sidebar"]//strong/text()').extract())
        if len(guanzhu_num) > 0:
            question_obj.guanzhu_num = int(guanzhu_num)

        answer_n = ''.join(problem.xpath('//h3[@id="zh-question-answer-num"]/text()').extract())
        if len(answer_n.split(" ")) == 2:
             question_obj.answer_num = int(answer_n.split(" ")[0])
        question_obj.save()

        log_url = response.url + "/log"
        yield Request(log_url, callback=self.parse_question_log)

        #deal with answer
        for answer in problem.xpath(r"//div[@class='zm-item-answer ']"):
            ans_obj = ZhihuAnswer.objects.create(question=question_obj)
            ans_obj.zan_num = 0
            ans_obj.pinglun_num = 0

            zans = answer.xpath("./div[@class='zm-votebar']/button[1]/span[2]/text()").extract()
            pingluns = answer.xpath(r"./div[4]/div/a[1]/text()").extract()

            if len(zans) > 0:
                zan_count = zans[0]
                if zan_count[-1] == 'K':
                    zan_count = int(zan_count[:-1]) * 1000
                else:
                    zan_count = int(zan_count)
                ans_obj.zan_num = zan_count
            if len(pingluns) > 2:
                ans_obj.pinglun_num = int(pingluns[1].split()[0])

            ans_obj.content = answer.xpath(r"./div[3]/div").extract()[0]
            ans_obj.save()

        # except:
        #     print '[Error] when parsing :' + response.url

