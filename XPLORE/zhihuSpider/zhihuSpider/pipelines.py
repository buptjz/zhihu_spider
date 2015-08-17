# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import ZhihuSpiderQuestionItem, ZhihuSpiderUserItem
from djangoWorker.models import ZhihuQuestion

class ZhihuspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DjangoPipeline(object):
    def __init__(self):
        pass
        # self.db = connection["zhihu"]
        # self.zh_user_col = self.db["zh_user"]
        # self.zh_ask_col = self.db["zh_ask"]
        # self.zh_answer_col = self.db["zh_answer"]
        # self.zh_followee_col = self.db["zh_followee"]
        # self.zh_follower_col = self.db["zh_follower"]
        #
        # self.gh_user_col = self.db["gh_user"]
        # self.gh_repo_col = self.db["gh_repo"]


    def process_item(self, item, spider):
        pass
        # if isinstance(item, ZhihuSpiderQuestionItem):
        #     obj, created = ZhihuQuestion.objects.update_or_create(page_id=item['page_id'])
        #     obj.page_id = item['page_id']
        #     obj.url = item['url']
        #     obj.title = item['title']
        #     obj.description = item['description']
        #     obj.tags = item['tags']
        #     obj.pinglun_num = int(item['pinglun_num'])
        #     obj.guanzhu_num = int(item['guanzhu_num'])
        #     obj.answer_num = int(item['answer_num'])
        #     obj.save()

        # elif isinstance(item, ZhihuSpiderQuestionItem):
        #     self.saveOrUpdate(self.zh_question_col,item,spider)

        return item