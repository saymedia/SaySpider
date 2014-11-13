# -*- coding: utf-8 -*-
from urlparse import urlparse
from datetime import datetime
import hashlib

from scrapy import log
from scrapy.http import HtmlResponse
from scrapy.contrib.spidermiddleware.httperror import HttpError
from scrapy.shell import inspect_response
from scrapy.contrib.linkextractors import LinkExtractor

from seolinter import lint_html

from saymedia.spiders.say_sitemap_spider import SaySitemapSpider
from saymedia.items import Page, Asset
from saymedia.requests import PageRequest, AssetRequest
from saymedia.links import AssetLink, PageLink
from saymedia.linkextractors import SayLinkExtractor

class SaySpider(SaySitemapSpider):
    name = "say_spider"
    sitemap_modified_since = False

    valid_link_tags = ('a', 'script', 'phx-script', 'img', 'link',)
    valid_link_attrs = ('href', 'src',)

    def __init__(self, **kwargs):
        super(SaySpider, self).__init__(**kwargs)
        url = kwargs.get('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s' % url
        if not url.endswith('/robots.txt'):
            url = '%s/robots.txt' % url
        self.url = url
        self.origin_host = kwargs.get('origin_host')
        self.sitemap_urls = [url]

        # Only process pages modified since date
        self.sitemap_modified_since = kwargs.get('since', False)

        self.link_extractor = SayLinkExtractor(tags=self.valid_link_tags,
            attrs=self.valid_link_attrs, deny_extensions=())


    def parse(self, response):
        # Primarily for debugging. 
        if response.url.endswith('/robots.txt'):
            return self._parse_sitemap(response)

        res = [self._get_details(response)]
        if response.request.method != 'HEAD':
            requests = self._extract_requests(response)
            res[0]['links'] = [r.url for r in requests]
            res.extend(requests)

        # inspect_response(response, self)
        # log.msg(response, level=log.DEBUG, spider=self)
        return res

    def handle_error_response(self, error):
        if hasattr(error.value, 'response'):
            self.parse(error.value.response)


    def get_origin_host(self):
        return self.origin_host

    def _get_details(self, response):
        if isinstance(response.request, AssetRequest):
            return self._get_asset_details(response)
        else:
            return self._get_page_details(response)

    def _get_page_details(self, response):
        page = Page.from_response(response)

        if isinstance(response, HtmlResponse) and \
            response.request.method != 'HEAD':

            if isinstance(response, HtmlResponse):
                res = lint_html(response.body)
                # log.msg('keys: %s' % ", ".join(res.keys()))

        return page

    def _get_asset_details(self, response):
        return Asset.from_response(response)

    def _extract_requests(self, response):
        res = []
        if isinstance(response, HtmlResponse):
            links = self.link_extractor.extract_links(response)
            for link in links:
                if isinstance(link, PageLink):
                    method = 'HEAD' if self.sitemap_modified_since != False or \
                        self._is_external(link.url) else 'GET'
                    res.append(PageRequest(link.url, callback=self.parse, method=method, errback=self.handle_error_response,
                        meta={'external': self._is_external(link.url), 'source_url': response.url}))
                elif isinstance(link, AssetLink):
                    res.append(AssetRequest(link.url, callback=self.parse, errback=self.handle_error_response,
                        meta={'external': self._is_external(link.url), 'source_url': response.url}))

        return res


    def _is_external(self, url):
        url_parts = urlparse(url)
        return ".".join(url_parts.hostname.split('.')[-2:]) != \
            ".".join(urlparse(self.url).hostname.split('.')[-2:])

