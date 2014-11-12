# -*- coding: utf-8 -*-

# Scrapy settings for saymedia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'saymedia'

SPIDER_MODULES = ['saymedia.spiders']
NEWSPIDER_MODULE = 'saymedia.spiders'
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'saymedia.middleware.MysqlDownloaderMiddleware': 1,
    'saymedia.middleware.TimerDownloaderMiddleware': 999,
    # 'saymedia.middleware.ErrorConverterMiddleware': 999,
}

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': None,
}

ITEM_PIPELINES = {
    'saymedia.pipelines.DatabaseWriterPipeline': 0,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'SEO Spider (+http://www.saymedia.com)'

DATABASE = {
    'USER': 'seo',
    'PASS': 'oes',
}

FIREBASE_URL = "https://incandescent-torch-9049.firebaseio.com"