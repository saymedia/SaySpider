from datetime import datetime

from scrapy import log
from scrapy.http import Response

class MysqlDownloaderMiddleware(object):

    def __init__(self, db):
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        # Create a database connection
        settings = crawler.settings

        return cls({})

    def process_request(self, request, spider):
        pass


class TimerDownloaderMiddleware(object):

    def process_request(self, request, spider):
        request.meta['request_start'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f UTC")
        return

    def process_response(self, request, response, spider):
        end = datetime.utcnow()
        start = datetime.strptime(request.meta.get('request_start'), "%Y-%m-%dT%H:%M:%S.%f %Z")
        request.meta['response_time'] = (end - start).total_seconds()
        return response


class OriginHostMiddleware(object):

    def process_request(self, request, spider):
        if hasattr(spider, 'get_origin_host'):
            request.meta['origin_host'] = spider.get_origin_host()

class ErrorConverterMiddleware(object):

    def process_exception(self, request, exception, spider):
        return Response(request.url, status=400)
