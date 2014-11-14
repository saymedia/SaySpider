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
    'saymedia.middleware.ErrorConverterMiddleware': 1,
    # 'saymedia.middleware.MysqlDownloaderMiddleware': 1,
    'saymedia.middleware.OriginHostMiddleware': 2,
    'saymedia.middleware.TimerDownloaderMiddleware': 998,
}

SPIDER_REPORTS = {
    'xml': 'saymedia.reports.XmlReport',
    'firebase': 'saymedia.reports.FirebaseReport',
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
    'USER': 'YOUR_DATABASE_USER',
    'PASS': 'YOUR_DATABASE_PASS',
}

FIREBASE_URL = "YOUR_FIREBASE_URL"

try:
    # Only used in development environments
    from .local_settings import *
except ImportError:
    pass