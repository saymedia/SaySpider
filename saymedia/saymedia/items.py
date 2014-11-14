# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from urlparse import urlparse
import hashlib
import scrapy
import json

from seolinter import lint_html

from scrapy.http import HtmlResponse
from scrapy import log

from saymedia.utils import url_hash

class Location(scrapy.Item):
    level = scrapy.Field()
    origin_host = scrapy.Field()
    origin_hash = scrapy.Field()
    url_hash = scrapy.Field()
    url = scrapy.Field()
    host = scrapy.Field()
    path = scrapy.Field()
    external = scrapy.Field()
    status_code = scrapy.Field()
    size = scrapy.Field()
    address_length = scrapy.Field()
    encoding = scrapy.Field()
    content_type = scrapy.Field()
    response_time = scrapy.Field()
    redirect_uri = scrapy.Field()
    timestamp = scrapy.Field()

    def __init__(self, response=None, **kwargs):
        if response:
            url_parts = urlparse(response.url)
            kwargs['external'] = response.request.meta.get('external', False)
            kwargs['level'] = response.request.meta.get('depth')
            kwargs['origin_host'] = response.request.meta.get('origin_host')
            kwargs['origin_hash'] = url_hash(kwargs['origin_host'])
            kwargs['url_hash'] = url_hash(response.url)
            kwargs['url'] = response.url
            kwargs['host'] = url_parts.hostname,
            kwargs['path'] = url_parts.path
            kwargs['status_code'] = response.status
            kwargs['encoding'] = response.encoding if hasattr(response, 'encoding') else None
            kwargs['content_type'] = response.headers.get('Content-Type')
            kwargs['address_length'] = len(response.url)
            kwargs['response_time'] = response.meta.get('response_time')
            kwargs['size'] = response.headers.get('Content-Length')
            super(Location, self).__init__(**kwargs)
        else:
            super(Location, self).__init__(**kwargs)



class Page(Location):
    canonical = scrapy.Field()
    content_hash = scrapy.Field()
    body = scrapy.Field()
    page_title = scrapy.Field()
    page_title_length = scrapy.Field()
    page_title_occurences = scrapy.Field()
    meta_description = scrapy.Field()
    meta_description_length = scrapy.Field()
    meta_description_occurrences = scrapy.Field()
    content_item_id = scrapy.Field()
    content_node_id = scrapy.Field()
    object_type = scrapy.Field()
    h1_1 = scrapy.Field()
    h1_length_1 = scrapy.Field()
    h1_2 = scrapy.Field()
    h1_length_2 = scrapy.Field()
    h1_count = scrapy.Field()
    meta_robots = scrapy.Field()
    rel_next = scrapy.Field()
    rel_prev = scrapy.Field()
    lint_critical = scrapy.Field()
    lint_error = scrapy.Field()
    lint_warn = scrapy.Field()
    lint_info = scrapy.Field()
    lint_results = scrapy.Field()
    links = scrapy.Field()

    @classmethod
    def from_response(cls, response):
        page = cls(response)
        if response.request.method != 'HEAD':
            # page['content_hash'] = hashlib.sha256(
            #     response.body.encode('ascii', 'ignore')).hexdigest()
            page['body'] = response.body

            title = response.xpath('//title/text()').extract()
            title = title[0] if len(title) > 0 else ''
            page['page_title'] = title
            page['page_title_length'] = len(title)

            description = response.xpath('//meta[@name="description"]/@content').extract()
            description = description[0] if len(description) > 0 else ''
            page['meta_description'] = description
            page['meta_description_length'] = len(description)

            h1s = response.xpath('//h1/text()').extract()
            page['h1_count'] = len(h1s)
            if len(h1s) > 0:
                page['h1_1'] = h1s[0]
                page['h1_length_1'] = len(h1s[0])
            if len(h1s) > 1:
                page['h1_2'] = h1s[1]
                page['h1_length_2'] = len(h1s[1])

            robots = response.xpath('//meta[@name="robots"]/@content').extract()
            robots = robots[0] if len(robots) > 0 else None
            page['meta_robots'] = robots

            rel_next = response.xpath('//link[@rel="next"]/@href')
            rel_next = rel_next[0] if len(rel_next) > 0 else None
            page['rel_next'] = rel_next

            rel_prev = response.xpath('//link[@rel="prev"]/@href')
            rel_prev = rel_prev[0] if len(rel_prev) > 0 else None
            page['rel_prev'] = rel_prev

            content_item_id = response.xpath('//meta[@name="phx:content-item-id"]/@content').extract()
            content_item_id = content_item_id[0] if len(content_item_id) > 0 else None
            page['content_item_id'] = content_item_id

            content_node_id = response.xpath('//meta[@name="phx:content-node-id"]/@content').extract()
            content_node_id = content_node_id[0] if len(content_node_id) > 0 else None
            page['content_node_id'] = content_node_id

            object_type = response.xpath('//meta[@name="phx:object-type"]/@content').extract()
            object_type = object_type[0] if len(object_type) > 0 else None
            page['object_type'] = object_type

            if isinstance(response, HtmlResponse) and \
                response.request.method != 'HEAD':

                if isinstance(response, HtmlResponse):
                    res = lint_html(response.body)
                    lint_keys = res.keys()
                    page['lint_critical'] = len([l for l in lint_keys if l[0] == 'C'])
                    page['lint_error'] = len([l for l in lint_keys if l[0] == 'E'])
                    page['lint_warn'] = len([l for l in lint_keys if l[0] == 'W'])
                    page['lint_info'] = len([l for l in lint_keys if l[0] == 'I'])
                    page['lint_results'] = json.dumps(res)


        return page


class Asset(Location):
    asset_type = scrapy.Field()

    @classmethod
    def from_response(cls, response):
        asset = cls(response)

        t = response.headers.get('Content-Type')
        if t:
            if 'javascript' in t:
                asset['asset_type'] = 'script'
            elif 'css' in t:
                asset['asset_type'] = 'stylesheet'
            elif 'image' in t:
                asset['asset_type'] = 'image'

        return asset
