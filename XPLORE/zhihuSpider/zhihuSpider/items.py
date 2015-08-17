# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from djangoWorker.models import ZhihuQuestion, ZhihuUser

class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuSpiderQuestionItem(scrapy.Item):
    '''django定义的知乎question model'''
    page_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    answer = scrapy.Field()
    user_name = scrapy.Field()
    tags = scrapy.Field()
    pinglun_num = scrapy.Field()
    guanzhu_num = scrapy.Field()
    answer_num = scrapy.Field()

class ZhihuSpiderUserItem(DjangoItem):
    '''django定义的知乎question model'''
    django_model = ZhihuUser