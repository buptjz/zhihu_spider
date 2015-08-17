# -*- coding: utf-8 -*-

# Scrapy settings for zhihuSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

ITEM_PIPELINES = {
    #'zhihu.pipelines.DoNothingPipeline': 300,
    #'zhihu.pipelines.JsonWithEncodingPipeline': 300,
    # 'zhihuSpider.pipelines.DjangoPipeline': 300,

    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    # 'zhihuSpider.middlewares.ProxyMiddleware': 100,
}

BOT_NAME = 'zhihuSpider'

SPIDER_MODULES = ['zhihuSpider.spiders']
NEWSPIDER_MODULE = 'zhihuSpider.spiders'

CONCURRENT_REQUESTS=64

# DOWNLOAD_DELAY = 0.005

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuSpider (+http://www.yourdomain.com)'



#融合 django
import sys
sys.path.append('../../XPLORE')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'XPLORE.settings'