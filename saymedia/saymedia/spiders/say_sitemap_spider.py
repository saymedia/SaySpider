import re
from datetime import datetime

from scrapy.contrib.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy import log

from saymedia.requests import PageRequest

class SaySitemapSpider(SitemapSpider):

    sitemap_modified_since = False

    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.body):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                log.msg(format="Ignoring invalid sitemap: %(response)s",
                        level=log.WARNING, spider=self, response=response)
                return

            s = Sitemap(body)
            if s.type == 'sitemapindex':
                for loc in iterloc(s, alt=self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                for loc in iterloc(s, since=self.sitemap_modified_since):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield PageRequest(loc, callback=c)
                            break


def iterloc(it, alt=False, since=False):
    for d in it:
        if is_newer(d, since):
            yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d and is_newer(d, since):
            for l in d['alternate']:
                yield l

def is_newer(d, since=False):
    if since == False:
        return True

    if 'lastmod' not in d:
        return False

    if type(since) is not datetime:
        raise TypeError(
            "SitemapSpider.sitemap_modified_since must be a valid datetime.datetime object")

    # The lastmod date should be in W3C format: http://www.sitemaps.org/protocol.html
    # 19 charaters represents: YYYY-MM-DDThh:mm:ss
    if len(d['lastmod']) > 19 and d['lastmod'][19] != '.': # We have timezone info
        format = "%Y-%m-%dT%H:%M:%S%z" if d['lastmod'][19] in ('+', '-',) else \
            "%Y-%m-%dT%H:%M:%S%Z"
        lastmod_date = datetime.strptime(d['lastmod'], format)
        return (lastmod_date >= since)
    else:
        # Just do a simple string comparison of the dates to avoid the complex
        # parsing into a datetime object with a variable length date
        since_str = since.strftime("%Y-%m-%dT%H:%M:%S")
        lastmod_str = d['lastmod'][:19]
        return (lastmod_str >= since_str[:len(lastmod_str)])
