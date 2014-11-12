"""
Link extractor based on lxml.html
"""

import re
from urlparse import urlparse, urljoin

import lxml.etree as etree

from scrapy.selector import Selector
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import unique as unique_list, str_to_unicode
from scrapy.linkextractor import FilteringLinkExtractor
from scrapy.utils.response import get_base_url

from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor, LxmlParserLinkExtractor

from scrapy import log

from saymedia.links import AssetLink, PageLink

_collect_string_content = etree.XPath("string()")

class SayParserLinkExtractor(LxmlParserLinkExtractor):

    def _extract_links(self, selector, response_url, response_encoding, base_url):
        links = []
        # hacky way to get the underlying lxml parsed document
        for el, attr, attr_val in self._iter_links(selector._root):

            if not self._is_valid_link(el, attr, attr_val):
                continue

            attr_val = urljoin(base_url, attr_val)
            url = self.process_attr(attr_val)

            if url is None:
                continue
            if isinstance(url, unicode):
                url = url.encode(response_encoding)
            # to fix relative links after process_value
            url = urljoin(response_url, url)
            if el.tag != 'a':
                link = AssetLink(url, _collect_string_content(el) or u'',
                    nofollow=True if el.get('rel') == 'nofollow' else False)
            else:
                link = PageLink(url, _collect_string_content(el) or u'',
                    nofollow=True if el.get('rel') == 'nofollow' else False)
            links.append(link)

        return unique_list(links, key=lambda link: link.url) \
                if self.unique else links        


    def _is_valid_link(self, el, attr, attr_val):
        if el.tag == 'link':
            if el.get('rel') in ('dns-prefetch', 'canonical', 'publisher',):
                return False
        return True


class SayLinkExtractor(FilteringLinkExtractor):

    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
                 tags=('a', 'area', 'script', 'link'), attrs=('href', 'src'), canonicalize=True,
                 unique=True, process_value=None, deny_extensions=None):
        log.msg(", ".join(tags), level=log.DEBUG)
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        tag_func = lambda x: x in tags
        attr_func = lambda x: x in attrs
        lx = SayParserLinkExtractor(tag=tag_func, attr=attr_func,
            unique=unique, process=process_value)

        super(SayLinkExtractor, self).__init__(lx, allow, deny,
            allow_domains, deny_domains, restrict_xpaths, canonicalize,
            deny_extensions)

    def extract_links(self, response):
        html = Selector(response)
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [subdoc
                    for x in self.restrict_xpaths
                    for subdoc in html.xpath(x)]
        else:
            docs = [html]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return unique_list(all_links)
