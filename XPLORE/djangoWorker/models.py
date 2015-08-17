# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode

# Create your models here.

class ProxyItem(models.Model):
    """Model of zhihu"""
    def __unicode__(self):
        return str(self.ip) + ":" + str(self.port)
    ip = models.CharField(max_length=100,primary_key=True)
    port = models.CharField(max_length=20)
    protocol = models.CharField(max_length=20,default="http")


class ZhihuQuestion(models.Model):
    """Model of zhihu"""
    def __unicode__(self):
        return "[" + smart_unicode(self.url) + "]" + smart_unicode(self.title)

    page_id = models.IntegerField(primary_key=True)        #page id
    url = models.URLField(max_length=200, null=True)       #url
    title = models.CharField(max_length=300)               #标题
    description = models.TextField()                       #抓取问题的描述
    user_name = models.CharField(max_length=200)           #个人用户的名称
    tags = models.TextField()
    pinglun_num = models.PositiveIntegerField(default=0)
    guanzhu_num = models.PositiveIntegerField(default=0)
    answer_num = models.PositiveIntegerField(default=0)
    create_time = models.CharField(max_length=200,default='0')
    last_edit_time = models.CharField(max_length=200,default='0')
    format_create_time = models.PositiveIntegerField(default=0)
    format_last_edit_time = models.PositiveIntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)

class ZhihuAnswer(models.Model):
    """Model of zhihu"""
    def __unicode__(self):
        return "[Answer]" + smart_unicode(self.content)

    question = models.ForeignKey(ZhihuQuestion, related_name='question_answer')
    zan_num = models.PositiveIntegerField(default=0)
    content = models.TextField()
    pinglun_num = models.PositiveIntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)

class ZhihuUser(models.Model):
    """Model of zhihu User"""
    def __unicode__(self):
        return "[" + smart_unicode(self.url) + "]" + smart_unicode(self.username)

    url = models.URLField(max_length=200, null=True)
    username = models.CharField(primary_key=True,max_length=200)
    nickname = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    industry = models.CharField(max_length=300)
    sex = models.CharField(max_length=30)
    jobs = models.TextField()
    educations = models.TextField()
    description = models.TextField()
    sinaweibo = models.CharField(max_length=200)
    tencentweibo = models.CharField(max_length=200)
    followee_num = models.PositiveIntegerField(default=0)
    follower_num = models.PositiveIntegerField(default=0)
    ask_num = models.PositiveIntegerField(default=0)
    answer_num = models.PositiveIntegerField(default=0)
    post_num = models.PositiveIntegerField(default=0)
    collection_num = models.PositiveIntegerField(default=0)
    log_num = models.PositiveIntegerField(default=0)
    agree_num = models.PositiveIntegerField(default=0)
    thank_num = models.PositiveIntegerField(default=0)
    fav_num = models.PositiveIntegerField(default=0)
    share_num = models.PositiveIntegerField(default=0)
    view_num = models.PositiveIntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)